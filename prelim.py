import json

post_ids = {}
posts_by_author = {}
posts_by_subreddit = {}
nd_subreddits = ()
nd_posters = {}
nt_subreddits_nd_users_post_to = ()


def read_data(filename):
    for line in filename:
        post = json.loads(line)
        post_id = len(post_ids)
        post_ids[post_id] = post
        author = post["author"]
        subreddit = post["subreddit"]

        if author not in posts_by_author:
            posts_by_author[author] = []
        posts_by_author[author].append(post_id)

        if subreddit not in posts_by_subreddit:
            posts_by_subreddit[subreddit] = []
        posts_by_subreddit[subreddit].append(post_id)









