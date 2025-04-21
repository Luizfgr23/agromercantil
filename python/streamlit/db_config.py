import psycopg2
import pandas as pd

def conexao_db():
    return psycopg2.connect(
        host="localhost",
        database="agromercantil",
        user="postgres",
        password="lfgr"
    )
    
def run_query(query):
    conn = conexao_db()
    df = pd.read_sql(query,conn)
    conn.close()
    return df