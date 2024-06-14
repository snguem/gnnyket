import mysql.connector
import json

class Query:
    def __init__(self,host:str,name:str,user:str="root",password:str="") -> None:
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
        except:
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
            except :
                print("Impossible d'executer la requette")
                return False
        elif sql.lower().startswith("insert"):
            try:
                cursor=self.connexion.cursor()
                cursor.execute(sql,values)
                return True
            except:
                return False

class database_manage(Query):
    def __init__(self, file_db:str, host: str, name: str, user: str = "root", password: str = "") -> None:
        super().__init__(host, name, user, password)
        self.datas_file=file_db
        # 
        try:
            self.load_datas()
        except:pass
    
    def create_tables(self)->bool:
        if self.datas.get("tables")!=None:
            tables=self.datas["tables"]
            for table in tables:
                attributs=""
                foreign_key=""
                for attribut in table["attributs"]:
                    attributs+=f",{attribut["name"]} {attribut["type"].upper()}{f"({attribut["length"]})" if attribut["type"] not in ["date","double"] else ""}{" PRIMARY KEY" if attribut["primary_key"]==True else ""}{" AUTO_INCREMENT" if attribut["auto_increment"]==True else ""}{" UNIQUE" if attribut["unique"]==True else ""}{f" DEFAULT {attribut["default_value"]}" if attribut["default_value"]!=None else ""}"
                    foreign_key+=f", FOREIGN KEY({attribut["name"]}) REFERENCES {attribut["foreign_key"]["table_name"]}({attribut["foreign_key"]["attribut_name"]})" if attribut["foreign_key"]["value"] else ""
                attributs=attributs.replace(",","",1)
                foreign_key=foreign_key.replace(",","",1) if foreign_key=="" else foreign_key
                
                try:
                    cur=self.connexion.cursor()
                    cur.execute(f"CREATE TABLE {table["name"]} ({attributs+foreign_key})")
                    print(f"creation table {table["name"]}: {attributs}{foreign_key}\n")
                except mysql.connector.errors.Error as er:
                    print(er)
                
            print(f"tables crees avec succes")
            return True
        else:
            print("la structure du fichier de donnees n'est pas correct ~ consulter la methode `info_database_struct`")
            return 0
    
    def drop_data_base(self)->bool:
        if(self.database_name!=None):
            try:
                # creation de la base de donnees
                self.connexion.cursor().execute(f"DROP DATABASE {self.database_name}")
            except :
                print("Impossible de supprimer la base de donnee")
                return 0
        
        else:
            print("la structure du fichier de donnees n'est pas correct ~ consulter la methode `info_database_struct`")
            return 0
        return 1

    def info_database_struct(self):
        return  """
                    file database structure:
                    {
                        "name":"gestion_classe",
                        "tables":[
                            {
                                "name":"salle",
                                "attributs":[
                                    {
                                        "name":"id",
                                        "type":"int",
                                        "length":11,
                                        "primary_key":true,
                                        "auto_increment":true,
                                        "unique":false,
                                        "default_value":null,
                                        "foreign_key":{
                                            "value":false,
                                            "table_name":null,
                                            "attribut_name":null
                                        }
                                    },
                                    {
                                        "name":"date",
                                        "type":"date",
                                        "length":0,
                                        "primary_key":false,
                                        "auto_increment":false,
                                        "unique":false,
                                        "default_value":null,
                                        "foreign_key":{
                                            "value":false,
                                            "table_name":null,
                                            "attribut_name":null
                                        }
                                    },
                                    {
                                        "name":"texte",
                                        "type":"varchar",
                                        "length":100,
                                        "primary_key":false,
                                        "auto_increment":false,
                                        "unique":true,
                                        "default_value":null,
                                        "foreign_key":{
                                            "value":false,
                                            "table_name":null,
                                            "attribut_name":null
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                """

    def load_datas(self):
        try:
            if self.datas_file!=None:
                with open(self.datas_file, 'r') as f:
                    self.datas = json.load(f)
                self.file_struct_charged=True
            else:
                print("veuillez renseigner le chemin du fichier de structuration de votre base de donnee")
        except json.JSONDecodeError as err:
            self.datas={}
    

if __name__=="__main__":
    USER = "root"
    PASSWORD = ""
    setting=database_manage(file_db="gnnyket.bd.json",
                            host="localhost",
                            name="gnnyket",
                            user=USER,
                            password=PASSWORD)

    setting.create_tables()
