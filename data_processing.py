import bz2, json, os, csv

class ProcessData:
    def __init__(self):
        self.data = {}

    # bz2 file format only, read in data
    def read_data(self, input, output):
        input = bz2.BZ2File(input)
        with open(output, 'w') as csvfile:
            fieldnames = ['author', 'subreddit', 'body']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for line in input:
                obj = json.loads(line)
                writer.writerow({'author': obj['author'],
                                ''' 'parent_id': obj['parent_id'] if 'parent_id' in obj else 'n/a','''
                                 'subreddit': obj['subreddit'],
                                 '''
				 'id' : obj['id'],
				 'score': obj['score'],
                                 'controversiality': obj['controversiality'],
                                 '''
				 'body': obj['body']
                                 })

                '''
        
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
    pd.read_data(path, 'test.csv')



if __name__ == '__main__':
    main()
