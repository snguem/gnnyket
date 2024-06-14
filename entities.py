import mysql.connector
import json, os, shutil
from config import *


class Query:
    def __init__(self,host:str=HOST,name:str=DATABASE,user:str=USER_,password:str=PASSWORD) -> None:
        # 
        self.host=host
        self.user=user
        self.password=password
        self.database_name=name
        # 
        self.connection()
    
    def connection(self):
        try:
            self.connexion= mysql.connector.connect(
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        database=self.database_name
                    )
            self.is_connected=True
        except mysql.connector.Error as e:
            print("\n\n\nerreur de connexion: ",e)
            self.is_connected=False
    
    def close(self):
        try:
            self.connexion.close()
            self.is_connected=False
        except:
            pass

    def query(self, sql:str, values:tuple=(), all:bool=True)-> list|bool:
        if sql.lower().startswith("select"):
            try:
                cursor=self.connexion.cursor()
                cursor.execute(sql,values)
                return cursor.fetchall() if all else cursor.fetchone()
            except mysql.connector.Error as e:
                print("Impossible d'executer la requette /", e)
                return False
        elif sql.lower().startswith("insert"):
            try:
                cursor=self.connexion.cursor()
                cursor.execute(sql,values)
                return cursor.lastrowid
            except mysql.connector.Error as e:
                print(sql,"\n", values)
                print(e.msg)
                return False
        elif sql.lower().startswith("update") or sql.lower().startswith("delete"):
            try:
                cursor=self.connexion.cursor()
                cursor.execute(sql,values)
                return cursor.lastrowid
            except mysql.connector.Error as e:
                print(sql,"\n", values)
                print(e.msg)
                return False


class ENTITI(Query):
    def __init__(self, table:str, keys:tuple) -> None:
        super().__init__()
        # table name
        self.name = table
        # attributs of class
        self.keys=keys
        
    def insert(self,elements:dict):
        index=",".join(["%s" for i in range(len(self.keys))])
        values=[]
        # 
        sql=f"""INSERT INTO {self.name}({",".join(self.keys)}) VALUES({index})"""
        # 
        for k in self.keys:
            if not k in elements:
                values.append(None)
            else:
                values.append(elements[k])
                
        return self.query(
            sql,values
        )
    
    def select(self,all:bool=True):
        sql=f"SELECT * FROM {self.name} WHERE etat=1 ORDER BY id DESC"
        datas=self.query(
                sql,all=all
            )
        datas_dict=[]
        if type(datas)==list and len(datas)>0:
            for ligne in datas:
                datas_dict.append(dict(zip(self.keys, ligne)))
        return datas_dict
    
    def select_max_id(self):
        sql=f"SELECT max(id) FROM {self.name}"
        return self.query(
                sql,all=False
            )[0]
    
    def update(self,id:int,condition:str,suplements:str,values:tuple|list):
        sql=f"UPDATE {self.name} SET {suplements} WHERE {condition}"
        print("\n\nquery return:",self.query(sql,values,all=False))
        if self.query(sql,values,all=False):
            return self.select_id(id)
        else:
            return None
    
    def delete(self,id:int) -> bool:
        sql=f"DELETE FROM {self.name} WHERE id={id}"
        # print
        if self.query(sql,all=False):
            return True
        else:
            return False
    
    def select_by(self,supplement:str=None,values:tuple=(), all:bool=True, sql:str=None):
        sql=f"SELECT * FROM {self.name} WHERE {supplement}{ ' ORDER BY id DESC' if all else ''}" if sql==None else sql
        datas=self.query(
                sql,values,all=all
            )
        datas_dict=[]
        if type(datas)==list and len(datas)>0:
            for ligne in datas:
                datas_dict.append(dict(zip(self.keys, ligne)))
        else:
            try:
                datas_dict = dict(zip(self.keys, datas))
            except:
                datas_dict = datas
            
        return datas_dict
    
    def select_id(self,id:int):
        sql=f"SELECT * FROM {self.name} WHERE id={id}"
        datas= self.query(
                sql,all=False
            )
        
        datas_dict = dict(zip(self.keys, datas))
        return datas_dict
    
    def count_(self, key:str,condition:str, etat="and etat=1"):
        return self.query(
            f'SELECT COUNT({key}) FROM {self.name} WHERE {condition} {etat}'
        )[0]
    

class TYPE_PRODUIT(ENTITI):
    def __init__(self) -> None:
        super().__init__('type_produit', ('id','ref','libelle','etat'))
    
    def select_with(self):
        types = self.select()
        new_types = []
        for type_ in types:
            type_["nbr"] = PRODUIT().count_('type_produit',f"type_produit = {type_["id"]}")[0]
            new_types.append(type_)
        return new_types

class COUPON(ENTITI):
    def __init__(self) -> None:
        super().__init__('coupon', ('id','code','date_crea','date_exp','reduction','etat'))

class USER(ENTITI):
    def __init__(self) -> None:
        super().__init__('user', ('id','nom','prenom','adresse','contact','mail','profil','role','password','etat'))

    
    def select_count_contact(self, contact:str):
        sql=f"SELECT count(id) as nbr FROM {self.name} WHERE contact = '{contact}'"
        return self.query(
                sql,all=False
            )[0]

    def select_count_mail(self, mail:str):
        sql=f"SELECT count(id) as nbr FROM {self.name} WHERE mail = '{mail}'"
        return self.query(
                sql,all=False
            )[0]

class PRODUIT(ENTITI):
    def __init__(self) -> None:
        super().__init__('produit', ('id','img','libelle','qte_stock','qte_cmde','categorie','type_produit','prix','taille','description','etat'))

    def select_with(self,el=None):
        all_prod = self.select_by(f"{'qte_stock > qte_cmde and' if el==None else ''} etat=1")
        new_prods = []
        for prod in all_prod:
            prod["type_prod"] = TYPE_PRODUIT().select_by("id=%s",(prod["type_produit"],),False)
            prod["prix_format"] = '{:,}'.format(int(prod["prix"]))
            new_prods.append(prod)
            
        return new_prods
    
    def discovert(self):
        produits=[]
        for prod in self.select_by(sql=f"SELECT * FROM {self.name} WHERE qte_stock > qte_cmde and etat=1 ORDER BY RAND() LIMIT 4"):
            prod['prix_format'] = "{:,}".format(prod['prix'])
            produits.append(prod)
        return produits
    
    def select_id(self, id: int):
        prod = super().select_id(id)
        prod["prix_format"] = '{:,}'.format(int(prod["prix"]))
        return prod
    
    def select(self, all: bool = True):
        prods = []
        for prod in super().select(all):
            prod["prix_format"] = '{:,}'.format(int(prod["prix"]))
            prods.append(prod)
        return prods
    
    
    def select_count_categori(self,all=True)->dict:
        catgs = {}
        if all:
            for cat in ["homme", "enfant", "femme", "mixte"]:
                catgs[cat] = "{:,}".format(self.count_("categorie",f"qte_stock>qte_cmde and etat=1 and categorie = '{cat}'")[0])
        return catgs

class COMMANDE(ENTITI):
    def __init__(self) -> None:
        super().__init__('commande', ('id','ref','date','montant','heure','montant_paye', 'client','etat'))
        
    def select(self):
        cmdes = []
        for cmde in self.select_by("etat in (0,1,2)"):
            cmde["montant_format"] = '{:,}'.format(cmde["montant"])
            cmde["client"] = USER().select_id(cmde["client"])
            cmde['heure_format'] = f"{(cmde['heure']//60):02}H{cmde['heure']%60:02}"
            cmdes.append(cmde)
        return cmdes
    
    def select_with(self, ref:str):
        cmds = self.select_by("ref=%s",(ref,), False)
        cmds['client'] = USER().select_id(cmds['client'])
        cmds['heure_format'] = f"{cmds['heure']//60:02}H{cmds['heure']%60:02}"
        cmds['montant_format'] = "{:,}".format(cmds["montant"])
        cmds['factures'] = []
        for fact in UNECOMMANDEPRODUIT().select_by("commande=%s",(cmds['id'],)):
            cmds['factures'].append(
                {'produit':PRODUIT().select_id(fact['produit']),'cmd':fact, 'montant_format':"{:,}".format(fact['montant'])}
            )
        return cmds

class UNECOMMANDEPRODUIT(ENTITI):
    def __init__(self) -> None:
        super().__init__('unecommandeproduit', ('id','montant','produit','commande','qte','etat'))

class NOTIFICATION(ENTITI):
    def __init__(self) -> None:
        super().__init__('notification', ('id','message','type','action','nom','prenom','contact','mail','adresse','sujet','etat'))




if __name__=="__main__":
    test = PRODUIT()
    if test.is_connected:
        print(test.count_("categorie", "categorie='homme'"))
        # converBinaryToFile(test.select_by("mail LIKE '%\snguemaabessolo@gmail.com%'")[0]["profil"],os.path.join(os.path.dirname(__file__),"src", "static", "img","profiler", "user.jpeg"))
        
        # Chemins de l'image source et de destination
        # chemin_source = os.path.join(os.path.dirname(__file__), "user.jpeg")
        # chemin_destination = os.path.join(os.path.dirname(__file__),"src", "static", "img", "user.jpeg")

        # # Déplacer l'image
        # shutil.move(chemin_source, chemin_destination)

        # print("L'image a été déplacée avec succès.")
        # with open("user.jpeg", "wb") as f:
        #     f.write()
        # # print(test.query(
        #     "select * from user where mail LIKE '%\snguemaabessolo@gmail.com%'",
            
        # ))