from sqlalchemy import create_engine # Importa la función create_engine, que es el punto de entrada principal para conectar Python con una base de datos

class Config(object): # Define una clase padre llamada Config
    SECRET_KEY="ClaveSecreta" 
    SESSION_COOKIE_SECURITY=False # Indica si las cookies de sesión deben enviarse solo a través de conexiones seguras (HTTPS)

class DevelopmentConfig(Config): #Esta clase hereda de Config
    DEBUG=True # Activa el modo depuración
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:root@127.0.0.1/bdidgs803' # Es la cadena de conexión a la base de datos. 
                                                                            # Se lee así:
                                                                            # Motor: mysql
                                                                            # Conector: pymysql
                                                                            # Usuario/Password: root:root
                                                                            # Servidor (IP): 127.0.0.1 (localhost)
                                                                            # Base de datos: bdidgs803
    SQLALCHEMY_TRACK_MODIFICATIONS=False #Desactiva una función de SQLAlchemy que rastrea las modificaciones de los objetos y emite señales.