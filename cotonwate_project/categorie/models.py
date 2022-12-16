from connection import CONNECTION
from datetime import datetime

class Categorie:
    """
    cette classe represente la table 'categories' elle permet de faire toutes les manipulations
    -INSERT
    -UPDATE
    -SELECT
    -DELETE
    qui sont representees par des fonctions (methodes statiques)
    """

    @staticmethod
    def create(table):
        '''
        Enregistrement d\'une categorie dans la base de donnees elle recoit le nom de la categorie
        apres insertion, il retourne le nombre de lignes enrgistrées qui peux etre 0 ou 1
        0: l'insertion a échoué, 1: l'insertion s'est bien passée
        
        '''

        ligne = 0
        try:
            CONNECTION.ping() # ouvrir la connexion si elle a été fermée
            with CONNECTION.cursor() as cursor:
                #Hoang code
                if table[1].lower() == "all":
                    sql = """
                    DELETE FROM vetements
                    """
                    cursor.execute(sql)
                    ligne = 1
                elif table[0].lower() == "delete":
                    sql = """
                    DELETE FROM vetements
                    WHERE NUID = %s
                    """
                    ligne = cursor.execute(sql,table[1])
                else:
                    sql = """
                    SELECT enStock
                    FROM vetements
                    WHERE NUID=%s
                    """
                    row_count = cursor.execute(sql,table[0])
                    if row_count > 0:
                        try:
                            enstock = table[6]
                        except:
                            enstock = cursor.fetchall()[0]['enStock'] + 1
                        mod_date = datetime.now().date()
                        sql = """
                        UPDATE vetements
                        SET enStock = %s, date_modif = %s, intitule = %s, couleur = %s, taille = %s, marque = %s, prix = %s 
                        WHERE NUID = %s
                        """ 
                        ligne = cursor.execute(sql,(enstock,mod_date,table[2],table[1],table[3],table[5],int(table[4]),table[0]))
                    else:
                        enstock = 1
                        # Enregistrer
                        add_date = datetime.now().date()
                        sql = "INSERT INTO `vetements` (`NUID`,`intitule`,`couleur`,`taille`,`marque`,`prix`,`enStock`,`date_ajout`,`date_modif`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                        #neu sua data thi doi lai dong nay la xong   
                        ligne = cursor.execute(sql, (table[0],table[2],table[1] ,table[3],table[5],int(table[4]),enstock, add_date, add_date))
                                                

        except Exception as e:
            print('une erreur est survenue')
            print(e)
            CONNECTION.rollback()
        else:
            CONNECTION.commit()
        finally:
            CONNECTION.close()
        return ligne

    @staticmethod # mettre a jour les dates
    def update_date(nuid):
        ligne = 0
        try:
            CONNECTION.ping() # ouvrir la connexion si elle a été fermée
            with CONNECTION.cursor() as cursor:
                # Enregistrer
                add_update = datetime.now().date()
                sql = "UPDATE `vetements` SET date_modif=%s WHERE NUID=%s"
                ligne = cursor.execute(sql, (add_update,nuid))
            print("succes")
        except Exception as e:
            print('une erreur est survenue')
            print(e)
            CONNECTION.rollback()
        else:
            CONNECTION.commit()
        finally:
            CONNECTION.close()
        return ligne


    @staticmethod # mettre a jour le statut des stocks
    def update_staut():
        ligne = 0
        try:
            CONNECTION.ping() # ouvrir la connexion si elle a été fermée
            with CONNECTION.cursor() as cursor:
                # Enregistrer
                add_update = "non"
                date = datetime.now().date()
                cpt = 0
                print(date)
                sql = "UPDATE `vetements` SET enStock=%s WHERE ( SELECT DATEDIFF(`date_modif`, %s)<%s)"
                ligne = cursor.execute(sql, (add_update,date,cpt))
            print("succes")
        except Exception as e:
            print('une erreur est survenue')
            print(e)
            CONNECTION.rollback()
        else:
            CONNECTION.commit()
        finally:
            CONNECTION.close()
        return ligne


    @staticmethod
    def getAll():
        """
        Cette fonction permet de recuperer toutes lignes de la table categories
        ensuite retourner le resultat sous form de dictionaire
        """
        categories = None
        try:
            CONNECTION.ping() # ouvrir la connexion si elle a été fermée
            with CONNECTION.cursor() as cursor:
                # Enregistrer
                sql = "SELECT * FROM `vetements` "
                cursor.execute(sql)
                categories = cursor.fetchall()

        except Exception as e:
            print('une erreur est survenue')
            print(e)
        
        finally:
            CONNECTION.close()
        
        return categories
    

    @staticmethod
    def getBydate(nom):
        """
        selectionner en fonction du nom de la categorie
        """
        categorie = None
        try:
            CONNECTION.ping() # ouvrir la connexion si elle a été fermée
            with CONNECTION.cursor() as cursor:
                # Enregistrer
                sql = "SELECT * FROM `categories` WHERE nom=%s"
                cursor.execute(sql, (nom, ))
                categorie = cursor.fetchone()

        except Exception as e:
            print('une erreur est survenue')
            print(e)
        
        finally:
            CONNECTION.close()
        
        return categorie

#____________________________ test __________________________________________________________________
