import os, sqlalchemy, pymysql

class Query:
    def __init__(self):
        conn = self.connSQL()

    def connSQL(self):
        print("Connecting to SQL...")
        engine = sqlalchemy.create_engine('mysql+pymysql://msap:RK58pycr@cubist.cs.washington.edu/msap_selfPres')
        conn = engine.connect()
        return conn

    def nt_posts_query(self):
        query = 
        conn.execute(sqlquery)

        conn.close()
                

def main():
    nt_posts = 

    q = Query()

if __name__ == "__main__":
    main()