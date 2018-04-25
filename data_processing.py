import bz2, json, os, sqlalchemy, pymysql, langid

class ProcessData:

    def connSQL(self):
        print("Connecting to SQL...")
        engine = sqlalchemy.create_engine('mysql+pymysql://msap:RK58pycr@cubist.cs.washington.edu/msap_selfPres?charset=utf8', encoding='utf-8')
        return engine

    # bz2 file format only, read in data
    def process_table(self, input):
        input = bz2.BZ2File(input)

        engine = self.connSQL()
        connection = engine.connect()
        print("Connected")
        i = 0

        print("Starting SQL queries")
        for line in input:
            print(i)
            i +=1
            
            obj = json.loads(line)
            # sanitize data for SQL input 
            author = obj["author"]
            subreddit = obj["subreddit"]
            body = obj["body"]
            # remove special characters
            body.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+\n"})
            body.replace("'", "\\'")

            # language filter
            lang = langid.classify(body)
            if lang[0] != "en":
                continue
 
            sqlquery = ("INSERT INTO posts_small (author, subreddit, body) VALUES ('{:s}', '{:s}', '{:s}');".format(author, subreddit, body))
            connection.execute(sqlquery)

        print("Done.")
        connection.close()
        print("Closed.")


        '''
        with open(output, 'w') as csvfile:
            fieldnames = ['author', 'subreddit', 'body']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for line in input:
                obj = json.loads(line)
                writer.writerow({'author': obj['author'],
                                 'subreddit': obj['subreddit'],
                                 'body': obj['body']})
        # optional columns in csv
		'id' : obj['id'],
                'score': obj['score'],
                'controversiality': obj['controversiality'],
                'parent_id': obj['parent_id'] if 'parent_id' in obj else 'n/a'
                
		# dict entry for this post
                id = obj['id']
                entry = {
                    'author' : obj['author'],
                    'parent_id' : obj['parent_id'] if 'parent_id' in obj else 'n/a',
                    'subreddit' : obj['subreddit'],
                    'score' : obj['score'],
                    'controversiality' : obj['controversiality'],
                    'body' : obj['body']
                }
                self.data[id] = entry
                
             '''

def main():
    #file = input('file: ')
    path = os.path.normpath(os.path.join(os.getcwd(), '..', 'data/RC_2017-01.bz2'))

    pd = ProcessData()
    pd.process_table(path)



if __name__ == '__main__':
    main()
