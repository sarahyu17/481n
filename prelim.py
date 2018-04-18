import json

class Prelim:
    def __init__(self):
        self.post_ids = {}
        self.posts_by_author = {}
        self.posts_by_subreddit = {}
        self.nd_subreddits = ()
        self.nd_posters = ()
        self.nt_subreddits_of_nd_users = ()

    def read_data(self, filename):
        with open(filename) as f:
            for line in f:
                post = json.loads(line)
                post_id = len(self.post_ids)
                self.post_ids[post_id] = post
                author = post["author"]
                subreddit = post["subreddit"]

                if author not in self.posts_by_author:
                    self.posts_by_author[author] = []
                self.posts_by_author[author].append(post_id)

                if subreddit not in self.posts_by_subreddit:
                    self.posts_by_subreddit[subreddit] = []
                self.posts_by_subreddit[subreddit].append(post_id)

    def load_nd_subreddits(self, nd_list):
        with open(nd_list) as f:
            for line in f:
                self.nd_subreddits.add(line)

    def find_nd_users(self):
        for subreddit in self.posts_by_subreddit.keys():
            if subreddit in self.nd_subreddits:
                post_ids = self.posts_by_subreddit[subreddit]
                for post_id in post_ids:
                    post = self.post_ids[post_id]
                    self.nd_posters.add(post["author"])

    def find_nt_subreddits(self):
        for poster in self.nd_posters:
            post_ids = self.posts_by_author[poster]
            for post_id in post_ids:
                post = self.post_ids[post_id]
                self.nt_subreddits_of_nd_users.add(post["subreddit"])

    def save_nt_subreddits(self, filename):
        f = open(filename)
        for subreddit in self.nt_subreddits_of_nd_users:
            f.write(subreddit + '\n')

        f.close()


    def main():
        comments = "./RC_2005-12"

        v1 = Prelim()
        v1.read_data(comments)
        v1.load_nd_subreddits("./neurodivergent")
        v1.find_nd_users()
        v1.find_nt_subreddits()

        v1.save_nt_subreddits("./nt_subreddits")



    if __name__ == "__main__":
        main()







