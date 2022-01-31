import pymysql
from pymysql.cursors import DictCursor
import config
#функция подключения к базе данных
def connect():
    return pymysql.connect(host='localhost',
        user=config.user,
        password=config.password,
        db=config.bd,
        charset='utf8mb4',
        cursorclass=DictCursor)

def checkUser(id):
    connection=connect()
    with connection.cursor() as cursor:
        query = f"""
        SELECT
            id,name,groupmember,Contacts
        FROM
            users
        WHERE id={id}
        """
        cursor.execute(query)
    data=cursor.fetchone()
    connection.close()
    return data

def users(groupmember):
    connection = connect()
    with connection.cursor() as cursor:
        query = f"""
        SELECT
            id,name,groupmember,Contacts
        FROM
            users
        WHERE groupmember={groupmember}
        """
        cursor.execute(query)
    data=cursor.fetchall()
    connection.close()
    return data

def allusers():
    connection = connect()
    with connection.cursor() as cursor:
        query = f"""
        SELECT
            id,name,groupmember,Contacts
        FROM
            users
        """
        cursor.execute(query)
    data=cursor.fetchall()
    connection.close()
    return data

def allcars():
    connection = connect()
    with connection.cursor() as cursor:
        query = f"""
        SELECT
            idDriver,name,gosNom,lastTO
        FROM
            cars
        """
        cursor.execute(query)
    data=cursor.fetchall()
    connection.close()
    return data

def carsDriver(id):
    connection = connect()
    with connection.cursor() as cursor:
        query = f"""
        SELECT
            idDriver,name,gosNom,lastTO
        FROM
            cars
        WHERE idDriver={id}
        """
        cursor.execute(query)
    data=cursor.fetchall()
    connection.close()
    return data

def AddUserDB(id,name,groupmember,contacts):
    connection = connect()
    with connection.cursor() as cursor:
        query = f"""
        INSERT
        INTO `users` (`id`, `name`, `groupmember`, `Contacts`) 
        VALUES(%s,%s,%s,%s)
        """
        cursor.execute(query,(int(id),str(name),int(groupmember),str(contacts)))
        connection.commit()
    connection.close()

def AddDocDB(id,name,tgID):
    connection = connect()
    with connection.cursor() as cursor:
        query = f"""
        INSERT
        INTO `docs` (`idDriver`, `name`, `tgID`) 
        VALUES(%s,%s,%s)
        """
        cursor.execute(query,(int(id),str(name),tgID))
        connection.commit()
    connection.close()

def checkDocIDdriver(id):
    connection = connect()
    with connection.cursor() as cursor:
        query = f"""
        SELECT
            id,idDriver,name,tgID
        FROM
            docs
        WHERE idDriver={id}
        """
        cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

def checkDocID(id):
    connection = connect()
    with connection.cursor() as cursor:
        query = f"""
        SELECT
            id,idDriver,name,tgID
        FROM
            docs
        WHERE id={id}
        """
        cursor.execute(query)
    data = cursor.fetchone()
    connection.close()
    return data