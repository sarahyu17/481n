import bz2, json, os, sqlalchemy

class ProcessData:

    # bz2 file format only, read in data
    def process_table(self, input):
        input = bz2.BZ2File(input)

        engine = connSQL()
        connection = engine.connect()

        for line in input:
            obj = json.loads(line)
            sqlquery = ("INSERT INTO posts_small (author, subreddit, body) "
                        "VALUES ({:s}, {:s}, {:s})".format(obj["author"], obj["subreddit"], obj["body"]))
            connection.execute(sqlquery)

        connection.close()



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

    def connSQL(self):
        print("Connecting to SQL...")
        engine = sqlalchemy.create_engine('mysql+pymysql://msap:RK58pycr@cubist.cs.washington.edu/msap_selfPres')
        return engine

def main():
    #file = input('file: ')
    path = os.path.normpath(os.path.join(os.getcwd(), '..', 'data/RC_2017-01.bz2'))

    pd = ProcessData()
    pd.process_table(path)



if __name__ == '__main__':
    main()
