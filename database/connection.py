import mysql.connector
from mysql.connector import pooling, Error
import logging
from config import Config

logger = logging.getLogger(__name__)

# Global connection pool reference
_pool = None

def init_db_pool():
    global _pool
    if _pool is not None:
        return _pool
    try:
        _pool = pooling.MySQLConnectionPool(
            pool_name="attendease_pool",
            pool_size=5,
            pool_reset_session=True,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            charset="utf8mb4",
            autocommit=False
        )
        logger.info("MySQL connection pool initialized successfully.")
        return _pool
    except Error as e:
        logger.warning(f"Could not initialize MySQL connection pool: {e}")
        _pool = None
        return None

def get_db_connection():
    """
    Returns a MySQL connection either from pool or directly.
    Raises Error if connection cannot be established.
    """
    global _pool
    if _pool is None:
        init_db_pool()
        
    if _pool is not None:
        try:
            conn = _pool.get_connection()
            return conn
        except Error as e:
            logger.warning(f"Failed to acquire connection from pool ({e}), attempting direct connection.")
    
    # Fallback to direct connection
    return mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset="utf8mb4",
        autocommit=False
    )

def query_all(query, params=None):
    """
    Execute a parameterized SELECT query and return all rows as list of dicts.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        return results
    except Error as e:
        logger.error(f"query_all error: {e} | Query: {query} | Params: {params}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def query_one(query, params=None):
    """
    Execute a parameterized SELECT query and return a single row as dict, or None.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        return result
    except Error as e:
        logger.error(f"query_one error: {e} | Query: {query} | Params: {params}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def execute(query, params=None, commit=True):
    """
    Execute an INSERT, UPDATE, or DELETE query.
    Returns (lastrowid, rowcount).
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        last_id = cursor.lastrowid
        row_count = cursor.rowcount
        if commit:
            conn.commit()
        return last_id, row_count
    except Error as e:
        if conn and commit:
            conn.rollback()
        logger.error(f"execute error: {e} | Query: {query} | Params: {params}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def execute_transaction(operations):
    """
    Execute a list of (query, params) tuples within a single atomic transaction.
    operations: [ (query1, params1), (query2, params2), ... ]
    Returns list of lastrowids.
    """
    conn = None
    cursor = None
    results = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for query, params in operations:
            cursor.execute(query, params or ())
            results.append(cursor.lastrowid)
        conn.commit()
        return results
    except Error as e:
        if conn:
            conn.rollback()
        logger.error(f"execute_transaction rollback due to error: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def log_audit(user_id, action, entity_type, entity_id=None, details=None, ip_address=None):
    """
    Record an administrative or critical user action into audit_logs.
    """
    query = """
        INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details, ip_address)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        execute(query, (user_id, action, entity_type, entity_id, details, ip_address))
    except Exception as e:
        logger.warning(f"Failed to record audit log: {e}")
