class Search_Post:
    post_id:int
    title:str
    content:str|None
    tags:list[str]
    creator_first_name:str
    creator_last_name:str
    creator_username:str
    score:int=0
    def __init__(self, post_id, title, content, tags, creator_first_name,creator_last_name,creator_username):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.tags = tags
        self.creator_first_name = creator_first_name
        self.creator_last_name = creator_last_name
        self.creator_username = creator_username
        self.score = 0
    def __str__(self) -> str:
        return f"Search_Post(post_id={self.post_id}, title='{self.title}', content='{self.content}', tags={self.tags}, " \
               f"first_name='{self.creator_first_name}', " \
               f"username='{self.creator_username}', score={self.score})"
    
def pre_process_search_query(search_query:str)->str:
    return search_query.strip().lower()

def tokenize(search_query:str)->list[str]:
    return search_query.split()

def get_ranked_post(search_query:str,posts:list[Search_Post]):
    for i in range (len(posts)):
        posts[i].score = 0
    q = pre_process_search_query(search_query)
    if q == "":
        return
    # tokenize the query
    tokens:list[str]=tokenize(q)
    # make the tokens unique
    tokens = list(set(tokens))
    for token in tokens:
        for post in posts:
            if token in post.title.lower():
                post.score+=1
            if post.content and token in post.content.lower():
                post.score+=1
            for t in post.tags:
                if token in t.lower():
                    post.score+=1    
            if token in post.creator_first_name.lower():
                post.score+=1
            if token in post.creator_last_name.lower():
                post.score+=1
            if token in post.creator_username.lower():
                post.score+=1
    # get max score
    max_score = 0
    for post in posts:
        if post.score>max_score:
            max_score = post.score
    max_score+=1
    # now check for exact match
    found = False
    for post in posts:
        if q in post.title.lower():
            post.score=max_score
            found = True
        elif post.content and q in post.content.lower():
            post.score=max_score
            found = True
        elif q in post.creator_first_name.lower():
            post.score=max_score
            found = True
        elif q in post.creator_last_name.lower():
            post.score=max_score
            found = True
        elif q in post.creator_username.lower():
            post.score=max_score
            found = True
        else:
            for t in post.tags:
                if q in t.lower():
                    post.score=max_score
                    found = True
                    break
     
    if found:
        print("here found")
        max_score+=1
        q = search_query.strip()
        print("unlowered q:",q)
        for post in posts:
            if q in post.title:
                post.score=max_score
            elif post.content and q in post.content:
                post.score=max_score
            elif q in post.creator_first_name:
                post.score=max_score
            elif q in post.creator_last_name:
                post.score=max_score
            elif q in post.creator_username:
                post.score=max_score
            else:
                for t in post.tags:
                    if q in t:
                        post.score=max_score
                        break     
        
    
    
    
# q = "I am A Little bird"
# posts:list[Search_Post] = [
#     Search_Post(1, "I am a little bird", "s", ["destiny", "song"], "User1"),
#     Search_Post(2, "I am A Little bird", "In the forest, there lived a", ["nature", "forest"], "User2"),
#     Search_Post(3, "Bird watching", "Learn about different bird species.", ["bird", "nature"], "User3"),
#     Search_Post(4, "Birds are amazing", "Birds are fascinating creatures.", ["bird", "little"], "User4"),
#     Search_Post(5, "User5's post", "This is a test post.", ["test", "user5"],"user5")
# ]
# get_ranked_post(q,posts)

# # sort the post based on score
# sorted_posts = sorted(posts, key=lambda post: post.score, reverse=True)

# for post in sorted_posts:
#     print(f"Post ID: {post.post_id}, Title: {post.title}, Score: {post.score}")