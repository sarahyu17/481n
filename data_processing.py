import bz2, json, os, csv

class ProcessData:
    def __init__(self):
        self.data = {}

    # bz2 file format only, read in data
    def read_data(self, input, output):
        input = bz2.BZ2File(input)
        with open(output, 'wb') as csvfile:
            fieldnames = ['id', 'author', 'parent_id', 'subreddit', 'score', 'controversiality', 'body']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for line in input:
                obj = json.loads(line)
                writer.writerow({'id' : obj['id'],
                                 'author': obj['author'],
                                 'parent_id': obj['parent_id'] if 'parent_id' in obj else 'n/a',
                                 'subreddit': obj['subreddit'],
                                 'score': obj['score'],
                                 'controversiality': obj['controversiality'],
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
    file = raw_input('file: ')
    path = os.path.normpath(os.path.join(os.getcwd(), '..', file))

    pd = ProcessData()
    pd.read_data(file, 'test.csv')



if __name__ == '__main__':
    main()