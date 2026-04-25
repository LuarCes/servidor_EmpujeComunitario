# db.py
# Módulo simple para obtener conexiones a MySQL usando variables de entorno.
# Si alguna variable no está definida, usa valores por defecto coherentes
# con tu dump (BD: empujecomunitario).

import os
import mysql.connector
from mysql.connector import pooling
import logging

# Configuración de logs para ver qué pasa en Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"DEBUG HOST={os.getenv('MYSQL_HOST')} TEST={os.getenv('TEST_VAR')}")

# Lee variables de entorno (Prioriza los datos de TiDB/Render)
MYSQL_HOST = os.getenv("MYSQL_HOST")
# Si no hay puerto en el entorno, TiDB suele usar 4000
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "4000")) 
MYSQL_DB   = os.getenv("MYSQL_DB", "empujecomunitario")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASSWORD")

# Validación rápida para avisarte en el log si te olvidaste una variable
if not all([MYSQL_HOST, MYSQL_USER, MYSQL_PASS]):
    logger.warning("⚠️ ¡Atención! Faltan variables de entorno de la base de datos. Usando valores por defecto (esto puede fallar en Render).")

try:
    # Creamos el pool de conexiones
    cnx_pool = pooling.MySQLConnectionPool(
        pool_name="ec_pool",
        pool_size=5,
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        database=MYSQL_DB,
        user=MYSQL_USER,
        password=MYSQL_PASS,
        # TiDB y MySQL moderno prefieren esto para evitar errores de autenticación
        auth_plugin="mysql_native_password"  
    )
    logger.info(f"✅ Pool de conexiones creado con éxito hacia {MYSQL_HOST}")
except Exception as e:
    logger.error(f"❌ Error crítico al crear el pool de conexiones: {e}")
    cnx_pool = None

def get_connection():
    """
    Devuelve una conexión lista para usar del pool.
    IMPORTANTE: Siempre cerrar con conn.close() después de usar.
    """
    if cnx_pool:
        return cnx_pool.get_connection()
    else:
        raise Exception("El pool de conexiones no está inicializado.")


