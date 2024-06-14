import datetime
import time
from flask import (Flask,
                    session, 
                    render_template, 
                    request, 
                    url_for,
                    redirect)
from markupsafe import Markup
from werkzeug.utils import secure_filename
from entities import *

app = Flask(__name__)

# if not 'cart' in session:
#     session['cart'] = {}

mgs_ = {
    "success":"",
    "failed":"",
    "errors":{}
}
nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]

app.config.from_pyfile("../config.py")

# -----------------------------------------home shopper
@app.route("/")
def home_shopper_fact_1():
    if not 'cart' in session:
        session['cart'] = {'produits':{},'not_solde':False,'nbr':0,'total':0.0,'total_format':''}
    return home_shopper()

@app.route("/home")
def home_shopper_fact_2():
    # session.pop('cart')
    if not 'cart' in session:
        session['cart'] = {'produits':{},'not_solde':False,'nbr':0,'total':0.0,'total_format':''}
    return home_shopper()

def home_shopper():
    session["id_shopper"] = 1
    msg_succes = mgs_["success"]
    mgs_["success"] = ''
    produits = PRODUIT().discovert()
    return render_template("all/index.html",produits=produits,msg_succes=msg_succes)
# -----------------------------------------end

# -----------------------------------------shop shopper
@app.route("/shop/all/",methods=["GET","POST"])
def shop_all_shopper():
    session["id_shopper"] = 3
    msg_error= ''
    msg_succes = mgs_['success']
    mgs_['success'] = ''
    produits = []
    for prod in PRODUIT().select_with():
        prod['prix'] = '{:,}'.format(int(prod['prix']))
        produits.append(prod)
    types = []
    for prod in produits:
        tpe = TYPE_PRODUIT().select_id(prod['type_produit'])
        if not tpe in types:
            types.append(tpe)
            
    catgs = PRODUIT().select_count_categori(True)
    if request.method == "GET":
        if "type" in request.args:
            tpe = int(request.args.get("type"))
            produits = [prod for prod in produits if prod['type_produit']==tpe]
        elif 'categori' in request.args:
            categorie = request.args.get('categori').lower()
            prods_categorie = [prod for prod in produits if prod['categorie'].lower()==categorie]
            if len(prods_categorie)>0:
                produits = prods_categorie
            else:
                msg_error = 'Produits indisponible pour cette categorie'
            
    return render_template("shop/shop.html",msg_succes=msg_succes,msg_error=msg_error,produits=produits,types=types,catgs=catgs)


@app.route("/shop/single/<id>/<nom>")
def shop_single_shopper(id:int,nom:str):
    session["id_shopper"] = 3
    msg_error = mgs_["errors"]
    msg_succes = mgs_["success"]
    mgs_["success"] = ""
    mgs_["errors"] = ""
    # 
    id = int(id) // 8923
    prod = PRODUIT().select_id(id)
    return render_template("shop/shop.single.html",prod=prod,msg_succes=msg_succes,msg_error=msg_error)
# -----------------------------------------end

@app.route("/about")
def about_shopper():
    session["id_shopper"] = 2
    return render_template("all/about.html")

@app.route("/contact", methods=['GET','POST'])
def contact_shopper():
    session["id_shopper"] = 4
    errors = {}
    msg_error = ''
    if request.method == "POST":
        if request.form['nom'].strip() == "":
            errors['nom'] = "Le nom est obligatoire"
        if request.form['prenom'].strip() == "":
            errors['prenom'] = "Le prenom est obligatoire"
        if request.form['mail'].strip() == "":
            errors['mail'] = "L'email est obligatoire"
        if request.form['sujet'].strip() == "":
            errors['sujet'] = "Le sujet est obligatoire"
        
        if errors == {}:
            if request.form['message'].strip() != '':
                NOTIFICATION().insert(
                    {
                        'message':request.form['message'].strip(),
                        'type':1,
                        'nom':request.form['nom'].strip(),
                        'prenom':request.form['prenom'].strip(),
                        'mail':request.form['mail'].strip(),
                        'sujet':request.form['sujet'].strip(),
                        'etat':2
                    }
                )
                mgs_["success"] = 'Votre message a ete envoyer avec success'
                return redirect("/home")
            else:
                msg_error = 'Veuiller renseigner un message'
    return render_template("all/contact.html",msg_error=msg_error,errors=errors)


# -----------------------------------------cart
@app.route("/cart")
def cart_shopper():
    session["id_shopper"] = 6
    # 
    msg_error = mgs_["errors"]
    msg_succes = mgs_["success"]
    mgs_["success"] = ""
    mgs_["errors"] = ""
    # 
    return render_template("cart/cart.html",msg_succes=msg_succes,msg_error=msg_error)

@app.route("/cart/add", methods=["POST"])
def cart_new_prod_shopper():
    session["id_shopper"] = 6
    qte = int(request.form["qte_cmd"])
    
    prod = PRODUIT().select_id(int(request.form["prod_id"]))
    msg_error = ""
    msg_succes = ""
    if qte < 1:
        msg_error = "La Quantite n'est pas valable"
    elif qte > (prod["qte_stock"]-prod["qte_cmde"]) :
        msg_error = "Stock insuffisant "
    else:
        if f'{prod["id"]}' in session["cart"]['produits']:
            session["cart"]['produits'][f'{prod["id"]}']["qte"]+=qte
            session["cart"]['produits'][f'{prod["id"]}']["montant"] += qte*prod["prix"]
            session["cart"]["total"] += qte*prod["prix"]
            session["cart"]['produits'][f'{prod["id"]}']["montant_format"] = '{:,}'.format(int(session["cart"]['produits'][f'{prod["id"]}']["montant"]))
        else:
            session["cart"]['produits'][f'{prod["id"]}'] = {"produit":prod, "qte":qte, "montant":qte*prod["prix"],"montant_format":'{:,}'.format(int(qte*prod["prix"]))}
            # session["cart"]['produits'][f'{prod["id"]}']["produit"] = prod
            session["cart"]["nbr"] += 1
            session["cart"]["total"] += session["cart"]['produits'][f'{prod["id"]}']["montant"]
        session['cart']['total_format'] = "{:,}".format(session["cart"]["total"])
            
        PRODUIT().update(
            prod['id'],
            f"id={prod['id']}",
            "qte_cmde=%s",
            (prod["qte_cmde"]+qte,)
        )
        
        msg_succes = "Produit ajouter avec success"
        mgs_["success"] = msg_succes
        return redirect("/cart")
    
    mgs_["errors"] = msg_error
    return redirect(f"/shop/single/{prod['id']*8923}/{prod['libelle']}")

@app.route("/cart/<id_prod>/del", methods=["GET"])
def cart_del_prod_shopper(id_prod:int):
    session["id_shopper"] = 6
    
    msg_succes = ""
    msg_error = ""
    
    id_prod = int(id_prod) // 87632
    
    prod= PRODUIT().select_id(id_prod)
    
    try:
        PRODUIT().update(
            id_prod,
            f"id={id_prod}",
            "qte_cmde=%s",
            (prod["qte_cmde"]- session["cart"]['produits'][f'{prod["id"]}']["qte"],)
        )
        session["cart"]["total"] -= session["cart"]['produits'][f'{prod["id"]}']["montant"]
        session['cart']['total_format'] = "{:,}".format(session["cart"]["total"])
        session['cart']['produits'].pop(f'{prod["id"]}')
        session['cart']['nbr']-=1
        
        msg_succes = "Produit retirer du panier avec success"
    except:
        msg_error = "Erreur lors du retrait du produit"
    
    mgs_["success"] = msg_succes
    mgs_["errors"] = msg_error
    return redirect(f"/cart")

@app.route("/cart/checkout", methods=["POST","GET"])
def checkout():
    errors = {}
    if request.method == "POST":
        return valider()
    return render_template("cart/checkout.html",errors=errors)

def valider():
    user = None
    errors = {}
    msg_error = ''
    if 'user_connected' in session:
        user = session['user_connected']
    else:
        if request.form['nom'].strip() == "":
            errors['nom'] = "Le nom est obligatoire"
        if request.form['prenom'].strip() == "":
            errors['prenom'] = "Le prenom est obligatoire"
        if request.form['mail'].strip() == "":
            errors['mail'] = "L'email est obligatoire"
        if request.form['adresse'].strip() == "":
            errors['adresse'] = "L'adresse est obligatoire"
        if request.form['contact'].strip() == "":
            errors['contact'] = "Le contact est obligatoire"
        if errors == {}:
            user_mail = USER().select_by("mail=%s", (request.form["mail"],), False)
            if user_mail == None:
                user = {fild.strip():request.form[fild] for fild in request.form}
                user['profil'] = 'img/user_default.png'
                user['role'] = 2
                user['password'] = "Gnny@Passer"
                user['etat'] = 0
                USER().insert(user)
                user = USER().select_id(USER().select_max_id())
            else:
                user = user_mail
        
        
    if user != None:
        
        try:
            COMMANDE().insert(
                {
                    'date':datetime.date.today(),
                    'montant':int(session['cart']['total']),
                    'heure':(int(time.strftime("%H"))*60)+int(time.strftime("%M")),
                    'montant_paye':int(session['cart']['total']),
                    'client':user['id'],
                    'etat':2
                }
            )
            
            cmd_id = COMMANDE().select_max_id()
            for prod in session['cart']['produits']:
                UNECOMMANDEPRODUIT().insert(
                    {
                        'montant':session['cart']['produits'][prod]['montant'],
                        'produit':session['cart']['produits'][prod]['produit']['id'],
                        'commande':cmd_id,
                        'qte':session['cart']['produits'][prod]['qte'],
                        'etat':1
                    }
                )
                
            COMMANDE().update(cmd_id,'id=%s',f"ref = 'CMD{cmd_id:05}'",(cmd_id,))
            
            NOTIFICATION().insert(
                {
                    'type':2,
                    'action':f"/commandes/details/CMD{cmd_id:05}",
                    'nom': user['nom'],
                    'prenom': user['prenom'],
                    'contact': user['contact'],
                    'mail': user['mail'],
                    'adresse': user['adresse'],
                    'etat':2
                }
            )
            
            session['cart'] = {'produits':{},'not_solde':False,'nbr':0,'total':0.0,'total_format':''}
            mgs_['success'] = 'Commande effectuee avec success'
            return redirect('/shop/all')
        except:
            msg_error = "Erreur survenu lors de l'enregistrement"
    
    return render_template("cart/checkout.html",msg_error=msg_error,errors=errors)
# -----------------------------------------end
# -----------------------------------------profil
@app.route("/profil/logout")
def logout_profiler():
    if 'user_connected' in session:
        session.pop('user_connected')
    return redirect('/home')

@app.route("/profil", methods=["GET"])
def dashboard_profiler():
    errors = mgs_["errors"]
    msg_succes = mgs_["success"]
    msg_error = mgs_["failed"]
    mgs_["errors"] = {}
    mgs_["success"] = ''
    mgs_["failed"] = ''
    
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    return render_template("profil.html", nbr_notifications=nbr_notifications,errors=errors,msg_succes=msg_succes,msg_error=msg_error)

@app.route("/profil", methods=["POST"])
def save_change():
    errors = {}
    msg_succes = ''
    msg_error = ''
    if request.method == 'POST':
        nom = request.form["nom"].strip()
        prenom = request.form["prenom"].strip()
        adresse = request.form["adresse"].strip()
        contact = request.form["contact"].strip()
        mail = request.form["mail"].strip()
        password = request.form["password"].strip()
        profil = request.files['profil']
        
        sql_suplements= ""
        values = []
        
        if nom == "":
            errors["nom"] = "le nom est obligatoire"
        else:
            sql_suplements+="nom=%s"
            values.append(nom)
        
        if prenom == "":
            errors["prenom"] = "le prenom est obligatoire"
        else:
            values.append(prenom)
            sql_suplements+=",prenom=%s"
        
        if adresse == "":
            errors["adresse"] = "l'adresse est obligatoire"
        else:
            values.append(adresse)
            sql_suplements+=",adresse=%s"
        
        if contact == "":
            errors["contact"] = "le contact est obligatoire"
        else:
            values.append(contact)
            sql_suplements+=",contact=%s"
        
        if mail == "":
            errors["mail"] = "l'email est obligatoire"
        else:
            values.append(mail)
            sql_suplements+=",mail=%s"
        if password == "":
            errors["password"] = "le mot de passe est obligatoire"
        elif len(password)<8:
            errors["password"] = "le mot de passe doit avoir au moins 8 caracteres"
        else:
            values.append(password)
            sql_suplements+=",password=%s"
        
        name = app.config['UPLOAD_FOLDER']+'/'+".".join([contact,profil.content_type.split('/')[-1]])
        
        if errors == {}:
            if profil.filename != '':
                if not 'user_default' in session["user_connected"]["profil"] and os.path.exists('/'.join(['src','static', session["user_connected"]["profil"]])):
                    os.remove('/'.join(['src','static', session["user_connected"]["profil"]]))
                    
                profil.save('/'.join(['src','static', name]),1000)
                sql_suplements += ",profil=%s"
                values.append(name)
                
            user_saved = USER().update(
                session.get("user_connected")['id'],
                f"id={session.get("user_connected")['id']}",
                sql_suplements,
                values
            )
            
            if user_saved!=0:
                msg_succes = "Donnees mis a jour avec success"
                session["user_connected"] = USER().select_by("id = %s",(session["user_connected"]['id'],),all=False)
        mgs_["errors"] = errors
        mgs_["success"] = msg_succes
        mgs_["failed"] = msg_error
    return redirect("/profil")


# -----------------------------------------end
# -----------------------------------------client
@app.route("/client/liste", methods=["POST", "GET"])
def client_liste():
    session["id_dispo_"] = 2
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    clients = user_by_role(2)
    if request.method=="GET":
        if 'filter' in request.args and request.args['filter']!='2':
            clients = [cl for cl in clients if cl['etat']==int(request.args['filter'])]
    else:
        clients = [cl for cl in clients if request.form['nom'].lower() in f"{cl['prenom']} {cl['nom']}".lower()]
    return render_template("client/client.tableau.html",clients=clients,nbr_notifications=nbr_notifications)

@app.route("/client/grille")
def client_grille():
    session["id_dispo_"] = 1
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    clients = user_by_role(2)
    return render_template("client/client.grille.html",clients=clients,nbr_notifications=nbr_notifications)

# -----------------------------------------end
# -----------------------------------------gestionnaire
@app.route("/gestionaire/liste", methods=['GET','POST'])
def gest_liste():
    msg=mgs_["success"]
    mgs_["success"] = ""
    session["id_dispo_"] = 2
    if request.method.lower() == "post":
        all_gest = USER().select_by(f"role=1 and (nom LIKE '%{request.form["nom"]}%' or prenom LIKE '%{request.form["nom"]}%')")
    else:
        all_gest = user_by_role(1)
        if "filter" in request.args:
            if int(request.args.get("filter")) != 2:
                all_gest = [gest for gest in all_gest if gest["etat"]==int(request.args.get("filter"))]
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    return render_template("gestionnaire/gestionnaire.tableau.html",nbr_notifications=nbr_notifications,msg_succes=msg, gests=all_gest)

@app.route("/gestionaire/grille")
def gest_grille():
    session["id_dispo_"] = 1
    msg=mgs_["success"]
    mgs_["success"] = ""
    all_gest = user_by_role(1)
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    return render_template("gestionnaire/gestionnaire.grille.html",nbr_notifications=nbr_notifications,msg_succes=msg, gests=all_gest)

@app.route("/gestionaire/<path>/<state>")
def update_state(path:str, state:int):
    state = int(state)
    session["id_dispo_"] = 1
    msg = ''
    gest_updated = USER().update(
        request.args.get('id'),
        f"id={request.args.get('id')}",
        "etat=%s",
        (state,)
    )
    if gest_updated!=None:
        msg = f'Gestionaire {["bloquer","Activer"][state]} avec success'
    mgs_["success"]=msg
    return redirect(f"/gestionaire/{path}")

def user_by_role(role:int):
    return USER().select_by(f"role = {role}")

@app.route("/gestionaire/new", methods=["GET"])
def gest_new():
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    
    return render_template("gestionnaire/new.gestionnaire.html",nbr_notifications=nbr_notifications,errors=mgs_["errors"],msg_succes=mgs_["success"])

@app.route("/gestionaire/new", methods=["POST"])
def gest_save():
    errors = {}
    msg_succes = ''
    if request.method == 'POST':
        nom = request.form["nom"].strip()
        prenom = request.form["prenom"].strip()
        adresse = request.form["adresse"].strip()
        contact = request.form["contact"].strip()
        mail = request.form["mail"].strip()
        password = 'passer123'
        
        sql_suplements= ""
        values = []
        
        if nom == "":
            errors["nom"] = "le nom est obligatoire"
        else:
            sql_suplements+="nom=%s"
            values.append(nom)
        
        if prenom == "":
            errors["prenom"] = "le prenom est obligatoire"
        else:
            values.append(prenom)
            sql_suplements+=",prenom=%s"
        
        if adresse == "":
            errors["adresse"] = "l'adresse est obligatoire"
        else:
            values.append(adresse)
            sql_suplements+=",adresse=%s"
        
        if contact == "":
            errors["contact"] = "le contact est obligatoire"
        elif USER().select_count_contact(contact)>0:
            errors["contact"] = "le contact n'est pas valide"
        else:
            values.append(contact)
            sql_suplements+=",contact=%s"
        
        # print('\n\ncontact:',USER().select_count_contact(contact),'\n\n')
        # print('\n\nmail:',USER().select_count_mail(mail),'\n\n')
        if mail == "":
            errors["mail"] = "l'email est obligatoire"
        elif USER().select_count_mail(mail)>0:
            errors["mail"] = "l'email n'est pas valide"
        else:
            values.append(mail)
            sql_suplements+=",mail=%s"
            
        if password == "":
            errors["password"] = "le mot de passe est obligatoire"
        elif len(password)<8:
            errors["password"] = "le mot de passe doit avoir au moins 8 caracteres"
        else:
            values.append(password)
            sql_suplements+=",password=%s"
        
        if errors == {}:
            user_saved = USER().insert(
                {'nom':nom,'prenom':prenom,'adresse':adresse,'contact':contact,'mail':mail,'profil':"/".join(["img", "user_default.png"]),'role':1,'password':"Gnny@Password","etat":1}
            )
            
            if user_saved!=None:
                msg_succes = "Gestionnaire creer avec success"
                mgs_["success"] = msg_succes
                return redirect("/gestionaire/grille")
    mgs_["errors"] = errors
    mgs_["success"] = msg_succes
    return redirect("/gestionaire/new")
# -----------------------------------------end
# -----------------------------------------produits
@app.route("/produits/liste", methods=["GET", "POST"])
def prod_liste():
    session["id_dispo_"] = 2
    msg_succes = mgs_["success"]
    msg_error=mgs_["failed"]
    
    mgs_["success"] = ""
    mgs_["failed"] = ""
    print("\n\nsucces:",msg_succes,"\nerror:",msg_error,"\n\n")
    produits =PRODUIT().select_with(el=1)
    if request.method == "GET":
        if "filter" in request.args:
            if request.args.get("filter").lower() != "all":
                produits = [prodtuit for prodtuit in produits if prodtuit["categorie"]==request.args.get("filter")]
    else:
        produits = [produit for produit in produits if request.form.get("libelle").lower() in produit["libelle"].lower()]
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    return render_template("produit/produit.tableau.html",nbr_notifications=nbr_notifications,msg_error=msg_error, msg_succes=msg_succes, produits=produits)

@app.route("/produits/grille")
def prod_grille():
    session["id_dispo_"] = 1
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    return render_template("produit/produit.grille.html", nbr_notifications=nbr_notifications,produits=PRODUIT().select())

@app.route("/produits/new", methods=["GET", "POST"])
def prod_new():
    errors = ''
    msg_succes = ''
    msg_error = ''
    type_id = ""
    
    if request.method == "POST":
        analyse_produt()
        errors = mgs_["errors"]
        msg_succes = mgs_["success"]
        msg_error = mgs_["failed"]
        
        if errors == {}:
            return redirect("/produits/liste")
        mgs_["errors"] = {}
        mgs_["success"] = ""
        mgs_["failed"] = ""
        if "type_id" in mgs_:
            type_id = mgs_["type_id"]
            mgs_.pop("type_id")
            
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    return render_template("produit/new.produit.html", nbr_notifications=nbr_notifications, type_id=type_id,errors=errors,msg_error=msg_error,msg_succes=msg_succes,types=TYPE_PRODUIT().select())

def analyse_produt(prod_type:str="new",prod=None):
    errors = {}
    msg_error = ''
    libelle = request.form["libelle"].strip()
    qte_stock = request.form["qte_stock"].strip()
    prix = request.form["prix"].strip()
    description = request.form["desc"].strip()
    
    categorie = request.form["categorie"].strip()
    type_id = request.form["type_prod"]
    taille = request.form["taille"].strip()
    image = request.files['image']
    
    if libelle == "":
        errors["libelle"] = "le libelle est obligatoire"
    
    if qte_stock == "":
        errors["qte_stock"] = "le quantite est obligatoire"
    elif not qte_stock.replace(" ","").isdigit() or int(qte_stock.replace(" ","")) == 0:
        errors["qte_stock"] = "le quantite est invalide"
    
    if prix == "":
        errors["prix"] = "le prix est obligatoire"
    elif not prix.replace(",","",1).replace(".","",1).replace(" ","").isdigit() :
        errors["prix"] = "le prix est invalide"
    elif float(prix.replace(".","",1).replace(",",".",1).replace(" ","")) < 1000:
        errors["prix"] = "le prix minimun est 1 000"
    
    if prod_type == 'new':
        if categorie == "":
            errors["categorie"] = "la categorie est obligatoire"
        
        if type_id.lower() in ["","selectionner"]:
            errors["type_id"] = "le type est obligatoire"
        else:
            type_id = int(type_id)
    
    if image.filename != '' :
        if prod!=None and os.path.exists('/'.join(['src','static', prod["img"]])):
            os.remove('/'.join(['src','static', prod["img"]]))
        name = PRODIUT_UPLOAD_FOLDER+'/'+".".join([f"{'produit@' if prod_type=='new' else f'prod{prod["id"]:010}' }",image.content_type.split('/')[-1]])
        image.save('/'.join(['src','static', name]),1000)
    else:
        if prod_type == "new":
            errors["image"] = "Veuiller choisir une image pour le produit"
        else:
            name = prod["img"]
    
    if errors == {}:
        try:
            if prod_type == "new":
                prod_saved = PRODUIT().insert(
                    {
                        'img':"img",
                        'libelle':libelle,
                        'qte_stock':qte_stock,
                        'qte_cmde':0,
                        'categorie':categorie,
                        'type_produit':type_id,
                        'prix':float(prix.replace(".","",1).replace(",","",1).replace(" ","")),
                        "taille":taille,
                        "description":description,
                        "etat":1
                    }
                )
                
                name = name.replace("img", "src/static/img")
                os.rename(name,name.replace("produit@", f"prod{prod_saved:010}"))
                name = name.replace("src/static/img","img")
                if PRODUIT().update(prod_saved,f"id={prod_saved}",f"img=%s",(name.replace("produit@", f"prod{prod_saved:010}"),))!=False:
                    msg_succes = "Produit ajouter avec success"
                    mgs_["success"] = msg_succes
            else:
                print("\n\nimage:",name,"\n\n")
                updated = PRODUIT().update(prod['id'],
                                           f"id={prod['id']}",
                                           "img=%s, libelle=%s, qte_stock=%s, prix=%s, categorie=%s, type_produit=%s, taille=%s, description=%s",
                                           (name, libelle, int(qte_stock), float(prix), categorie, int(type_id), taille, description))
                
                print("\n\nhere\n\n",updated, errors)
                if updated!=0:
                    msg_succes = "Produit modifier avec success"
                    mgs_["success"] = msg_succes
        except:
            msg_error = f"Erreur survenu lors de {'l\'ajout' if prod_type=="new" else 'la modification'} du produit"
   
    mgs_["errors"] = errors
    mgs_["failed"] = msg_error
    mgs_["type_id"] = type_id

@app.route("/produits/details/<id_>/<name>", methods=["GET","POST"])
def prod_details(id_:int,name:str):
    errors={}
    msg_succes=""
    msg_error=''

    prod = PRODUIT().select_id(int(id_)//3425)
    type_id = prod["type_produit"]
    types = TYPE_PRODUIT().select()
    if request.method == "POST":
        analyse_produt("upd",prod)
        
        errors = mgs_["errors"]
        msg_succes = mgs_["success"]
        msg_error = mgs_["failed"] 
        # if errors != {}:
        #     return redirect("/produits/liste")
        mgs_["errors"] = {}
        mgs_["success"] = ""
        mgs_["failed"] = ""
        if "type_id" in mgs_:
            type_id = mgs_["type_id"]
            mgs_.pop("type_id")
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    return render_template("produit/produit.details.html", nbr_notifications=nbr_notifications, msg_succes=msg_succes, msg_error=msg_error, type_id=type_id, errors=errors,types=types, name=name,prod=prod)

@app.route("/produits/liste/<id_>/del", methods=["GET","POST"])
def del_prod(id_:int):
    msg_succes = ''
    msg_error = ''
    id_ = int(id_)//3102
    if request.method == "POST":
        try:
            for cmd in COMMANDE().query(f'SELECT cm.* FROM commande cm, unecommandeproduit ucm, produit p WHERE cm.etat=2 and ucm.commande=cm.id and ucm.produit=p.id and p.id={id_} group by cm.id'):
                COMMANDE().update(cmd[0],"id=%s", "etat=0",(cmd[0],))
                
            PRODUIT().update(id_,"id=%s","etat=0",(id_,))
            msg_succes = "Produit supprimer avec success"
        except:
            msg_error = 'Erreur lors de la suppression du produit'
        mgs_["failed"] = msg_error
        mgs_["success"] = msg_succes
    else:
        return redirect(f"/produits/liste/{id_*3102}/del/confirm")
    return redirect("/produits/liste")

@app.route("/produits/liste/<id_>/del/confirm", methods=["GET"])
def confirm_del_prod(id_:int):
    path = f"/produits/liste/{id_}/del"
    a_path = "/produits/liste"
    id_ = int(id_)//3102
    html_info = Markup(f"Vous allez supprimer ce produit. Il ne sera plus visible dans la liste des produits. <br><strong>N.B: Les commandes liees a ce produits seront annules! </strong>")
    produits = PRODUIT().select_with()
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    return render_template("produit/produit.tableau.html",
                           nbr_notifications=nbr_notifications,
                           ask        =True,
                           path       =path,
                           a_path     =a_path,
                           infos      =html_info,
                           produits   =produits,
                           msg_succes ='',
                           msg_error  ='')

# -----------------------------------------end

@app.route("/dashboard")
def dashboard_home():
    prod_nbr = '{:,}'.format(PRODUIT().count_("id","etat=1")[0])
    client_nbr = '{:,}'.format(USER().count_("id","role=2 and etat=1")[0])
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    commandes_en_cours = []
    cmds_liste = COMMANDE().select_by("etat=%s", (2,))
    for cmd in cmds_liste:
        cmd["montant_format"] = "{:,}".format(cmd['montant'])
        commandes_en_cours.append(cmd)
    
    if session['user_connected']['role'] == 2:
        commandes_en_cours = [cmd for cmd in commandes_en_cours if cmd['client']==session['user_connected']['id']]
    
    return render_template("all/index.dashbord.html",nbr=len(commandes_en_cours),commandes=commandes_en_cours,nbr_notifications=nbr_notifications,prod_nbr=prod_nbr,client_nbr=client_nbr)

# -----------------------------------------type produit
@app.route("/type/produit", methods=["GET","POST"])
def type_produit_liste():
    msg_succes = mgs_["success"]
    msg_error = mgs_["failed"]
    
    mgs_["success"] = ""
    mgs_["failed"] = ""
    
    if request.method == "POST":
        libelle = request.form["libelle"]
        if libelle == "":
            msg_error = "le libelle est obligatoire"
        elif len(TYPE_PRODUIT().select_by(f"libelle = '{libelle.lower()}'"))>0:
            msg_error = "Deja existant"
            
        if msg_error == '':
            id_=TYPE_PRODUIT().select_max_id()
            id_ = 0 if id_==None else id_
            type_saved = TYPE_PRODUIT().insert(
                {'libelle':libelle.lower(),'ref':'None',"etat":1}
            )
            if type_saved!=False:
                TYPE_PRODUIT().update(type_saved,
                    f"id={type_saved}",
                    "ref=%s",
                    (f"TYPE{type_saved:05}",)
                )
                msg_succes = "Ajouter avec success"
            else:
                msg_error = "Erreur survenu lors de l'ajout"
    all_type_prods = TYPE_PRODUIT().select_with()
    
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    return render_template("type.produit.html", nbr_notifications=nbr_notifications, prods=all_type_prods, msg_succes=msg_succes,msg_error=msg_error)

@app.route("/type/produit/<id_>/del", methods=["GET","POST"])
def del_type_prod(id_:int):
    msg_succes = ''
    msg_error = ''
    id_ = int(id_)//100
    if request.method == "POST":
        try:
            print("\n\nprods:",PRODUIT().select_by("type_produit=%s",(id_,)),"\n\n")
            for prod in PRODUIT().select_by("type_produit=%s",(id_,)):
                PRODUIT().update(prod["id"],"id=%s","etat=0",(prod["id"],))
            if TYPE_PRODUIT().delete(id_)==0:
                msg_succes = "Type supprimer avec success"
            else:
                int("erreur")
        except:
            msg_error = 'Erreur lors de la suppression du type'
        mgs_["failed"] = msg_error
        mgs_["success"] = msg_succes
    else:
        return redirect(f"/type/produit/{id_*100}/del/confirm")
    return redirect("/type/produit")

@app.route("/type/produit/<id_>/del/confirm", methods=["GET"])
def confirm_del_type_prod(id_:int):
    path = f"/type/produit/{id_}/del"
    a_path = "/type/produit"
    id_ = int(id_)//100
    html_info = Markup("Si vous supprimer ce type, vous devrez modifier le type des produits associes. <br><strong>N.B: ces produits seront desactives tant qu'ils n'auront pas un nouveau type! </strong>")
    all_type_prods = TYPE_PRODUIT().select_with()
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    return render_template("type.produit.html",
                           nbr_notifications=nbr_notifications,
                           ask        =True,
                           path       = path,
                           a_path     =a_path,
                           infos      =html_info,
                           prods      =all_type_prods,
                           msg_succes ='',
                           msg_error  ='')

# -----------------------------------------end
# -----------------------------------------coupon
@app.route("/coupon")
def coupon_liste():
    return render_template("coupon.html")
# -----------------------------------------end
# -----------------------------------------commandes
@app.route("/commandes/liste", methods=["POST", "GET"])
def commandes_liste():
    session["id_dispo_"] = 2
    msg_succes = mgs_["success"]
    mgs_["success"] = ''
    commandes = COMMANDE().select()
    if session['user_connected']['role']==2:
        commandes = [cmd for cmd in commandes if cmd['client']['id']==session['user_connected']['id']]
    if request.method == "GET":
        if 'etat' in request.args and request.args['etat']!='3':
            commandes = [cmde for cmde in commandes if cmde['etat']==int(request.args['etat'])]
    else:
        commandes = [cmde for cmde in commandes if request.form['contact'] in cmde['client']['contact']]
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    return render_template("commande/commande.tableau.html",nbr=len(commandes),nbr_notifications=nbr_notifications,msg_succes=msg_succes,commandes=commandes)

@app.route("/commandes/grille")
def commandes_grille():
    session["id_dispo_"] = 1
    commandes = COMMANDE().select()
    msg_succes = mgs_["success"]
    mgs_["success"] = ''
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    if session['user_connected']['role']==2:
        commandes = [cmd for cmd in commandes if cmd['client']['id']==session['user_connected']['id']]
    return render_template("commande/commande.grille.html",nbr=len(commandes),nbr_notifications=nbr_notifications,msg_succes=msg_succes,commandes=commandes)

@app.route("/commandes/<path>/<action>/<ref>", methods=["POST"])
def action_cmde(path:str,ref:str,action:int):
    if COMMANDE().update(ref,"ref=%s", "etat=%s",(int(action),ref))!=False:
        if int(action)==0:
            cmde_dismis = COMMANDE().select_by("ref=%s", (ref,), False)
            for cmd_prod in UNECOMMANDEPRODUIT().select_by("commande=%s",(cmde_dismis['id'],)):
                prod = PRODUIT().select_id(cmd_prod['produit'])
                PRODUIT().update(cmd_prod['produit'], f"id={cmd_prod['produit']}", "qte_cmde = %s", (prod['qte_cmde']-cmd_prod['qte'],))
        mgs_['success'] = f"Commande {['rejeter','valider'][int(action)]} avec succes!"
    return redirect(f"/commandes/{path}{f'/{ref}' if path=='details' else ''}")

@app.route("/commandes/<path_>/<ref>/<action>/confirm")
def confirm_action(path_:str,ref:str,action:int):
    session["id_dispo_"] = 1
    commandes = COMMANDE().select()
    a_path = f"/commandes/{path_}{f'/{ref}' if path_=='details' else ''}"
    infos = f"Vous allez {['rejeter', 'valider'][int(action)]} la commde {ref} !"
    path = f"/commandes/{path_}/{action}/{ref}"
    path_ = path_.replace("liste",'tableau')
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    commande = COMMANDE().select_with(ref) if path_=="details" else None
    return render_template(f"commande/commande.{path_}.html",
                           commande=commande,
                           nbr_notifications=nbr_notifications,
                           a_path=a_path,
                           infos=infos,
                           path=path,
                           commandes=commandes,
                           ask=True)

@app.route("/commandes/details/<ref>")
def commandes_details(ref:str):
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    commande = COMMANDE().select_with(ref)
    msg_succes = mgs_["success"]
    mgs_["success"] = ''
    return render_template("commande/commande.details.html",msg_succes=msg_succes,commande=commande,nbr_notifications=nbr_notifications)
# -----------------------------------------end

@app.route("/notification")
def notification():
    notis = NOTIFICATION().select_by("etat in (1, 2)")
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    return render_template('notifications.html',nbr_notifications=nbr_notifications,notis=notis, nbr=len(notis))

@app.route("/notification/<id_>")
def notification_see_msg(id_:int):
    id_ = int(id_) // 34562
    noti = NOTIFICATION().select_id(id_)
    NOTIFICATION().update(noti['id'], f"id = {noti['id']}", "etat=%s", (1, ))
    if noti["type"] == 1:
        msg = Markup(f"<p>Nom: {noti['nom']}<br>Prenom: {noti['prenom']}<br>Email: {noti['mail']}<br><br><strong>Sujet: {noti['sujet']}</strong><br><br>{noti['message']}</p>")
    else:
        msg = Markup(f"<p>Mr/Mdme/Mdmlle {noti['nom']} {noti['prenom']}, vivant a/au {noti['adresse']} a passer une commande. <br><br><a href='{noti["action"]}'>Voir ici</a></p>")
    
    
    nbr_notifications = NOTIFICATION().count_("id", "etat = 2","")[0]
    notis = NOTIFICATION().select_by("etat in (1, 2)")
    return render_template('notifications.html', nbr_notifications=nbr_notifications,msg=msg, notis=notis, nbr=len(notis))


@app.route("/login", methods=["GET","POST"])
def login():
    if 'user_connected' in session:
        return redirect("/profil")
    errors = {}
    if request.method=="POST":
        if request.form['mail'].strip() == "":
            errors['mail'] = "Le mail est obligatoire"
        if request.form['password'].strip() == "":
            errors['password'] = "Le mot de passe est obligatoire"
        if errors == {}:
            user = USER().select_by("mail=%s and password=%s",(request.form['mail'].strip(), request.form['password'].strip()),False)
            
            if user==None:
                errors['failde'] = 'Login/Mot de passe incorrect'
            else:
                if user['etat'] == 0:
                    errors['failde'] = 'Erreur de compte !'
                else:
                    session['user_connected'] = user
                    mgs_['success'] = 'Connexion etablie'
                    path_redirect = "/profil"
                    if 'path_login' in mgs_:
                        path_redirect = mgs_['path_login']
                        mgs_.pop('path_login')
                    return redirect(path_redirect)
                
    return render_template("identification/connexion.html",errors=errors)

@app.route("/register", methods=["GET","POST"])
def register():
    errors = {}
    if request.method=="POST":
        if request.form['nom'].strip() == "":
            errors['nom'] = "Le nom est obligatoire"
        if request.form['prenom'].strip() == "":
            errors['prenom'] = "Le prenom est obligatoire"
        if request.form['adresse'].strip() == "":
            errors['adresse'] = "L'adresse est obligatoire"
        if request.form['contact'].strip() == "":
            errors['contact'] = "Le contact est obligatoire"
        if request.form['mail'].strip() == "":
            errors['mail'] = "Le mail est obligatoire"
        if request.form['password'].strip() == "":
            errors['password'] = "Le mot de passe est obligatoire"
        elif len(request.form['password'].strip()) <6:
            errors['password'] = "Le mot de passe doit avoir 6 caracteres minimun"
        if request.form['password_confirm'].strip() == "":
            errors['password_confirm'] = "Veuiller confirmer le mot de passe"
        elif request.form['password_confirm'].strip()!=request.form['password'].strip():
            errors['password_confirm'] = "Les mot de passe sont incompatible"
            
        if errors == {}:
            user = USER().select_by("mail=%s",(request.form['mail'].strip(),),False)
            if user!=None:
                USER().update(user['id'], "mail=%s", "etat=1, password=%s",(request.form['password'].strip(),user['mail']))
                user['etat'] = 1
            else:
                user = {field:request.form[field] for field in request.form}
                user.pop("password_confirm")
                user['role'] = 2
                user['etat'] = 1
                user['profil'] = "img/user_default.png"
                USER().insert(user)
                user = USER().select_id(USER().select_max_id())
            mgs_["success"] = 'Compte creer avec succes'
            session['user_connected'] = user
            return redirect('/profil')
                
    return render_template("identification/register.html",errors=errors)



@app.route("/login/identify", methods=["GET"])
def login_alternate():
    mgs_['path_login'] = '/cart/checkout'    
    return redirect("/login")
