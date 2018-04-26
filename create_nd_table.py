import os, sqlalchemy, pymysql

class NeuroDiv:

    def connSQL(self):
        print("Connecting to SQL...")
        engine = sqlalchemy.create_engine('mysql+pymysql://msap:RK58pycr@cubist.cs.washington.edu/msap_selfPres')
        conn = engine.connect()
        return conn

    def load_nt_subreddit_table(self, file):
        conn = self.connSQL()

        with open(file) as f:
            for line in f:
                subreddit = line.rstrip('\n')
                sqlquery = ("INSERT INTO nd_subreddits (subreddit) VALUES ('{:s}');".format(subreddit))
                conn.execute(sqlquery)

        conn.close()
                

def main():
    f = os.path.normpath(os.path.join(os.getcwd(), 'neurodivergent.txt'))
    nt = NeuroDiv()
    nt.load_nt_subreddit_table(f)

if __name__ == "__main__":
    main()