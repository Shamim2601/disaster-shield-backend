import models,schemas,search_service
from sqlalchemy.orm import Session
from datetime import datetime

def get_all_posts(db:Session):
    pass

def create_post(db:Session,post:schemas.Post_Create,user:models.User):
    creator_id=user.user_id
    creation_time=int(round(datetime.now().timestamp()))
    db_post=models.Post(**post.dict(),creator_id=creator_id,creation_time=creation_time)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post_by_id(db:Session,post_id:int):
    return db.query(models.Post).filter(\
        models.Post.post_id == post_id).first()
    
def get_all_posts(db:Session):
    return db.query(models.Post).all()

def get_all_posts_with_sorting_and_filtering(db:Session,sort_type:schemas.Sort_Type,sort_enabled:bool=True):
    query = db.query(models.Post)
    if(sort_enabled):
        if(sort_type == schemas.Sort_Type.newest):
            query = query.order_by(models.Post.creation_time.desc())
        elif(sort_type == schemas.Sort_Type.oldest):
            query = query.order_by(models.Post.creation_time.asc())
        elif(sort_type == schemas.Sort_Type.volunteers):
            posts = query.all()
            # volunteers needed minus enlistments sorted in descending order, if volunteers needed is None, it is treated as negative infinity
            posts.sort(key=lambda post: post.volunteers_needed - len(post.enlistments) if post.volunteers_needed is not None else float("-inf"), reverse=True)
            return posts
    return query.all()

def update_post(db:Session,post_id:int,post:schemas.Post_Update):
    db.query(models.Post).filter(models.Post.post_id\
    == post_id).update(post.dict(exclude_unset=True),\
    synchronize_session=False)
    
    db.commit()
    return get_post_by_id(db,post_id)

def get_post_tag(db:Session,post_id:int,tag:str):
    return db.query(models.Post_Tag)\
        .filter(models.Post_Tag.post_id == post_id,
        models.Post_Tag.tag == tag).first()

def add_tag_to_post(db: Session, post_tag:schemas.Post_Tag):
        tag_obj = models.Post_Tag(**post_tag.dict())
        db.add(tag_obj)
        db.commit()
        db.refresh(tag_obj)
        return tag_obj

def remove_tag_from_post(db: Session, post_id: int, tag: str):
    db.query(models.Post_Tag).filter(
        models.Post_Tag.post_id == post_id,
        models.Post_Tag.tag == tag
    ).delete(synchronize_session=False)
    db.commit()
    
def get_post_enlistment(db:Session,post_id:int,user_id:int):
    return db.query(models.Post_Enlistment).filter(
        models.Post_Enlistment.post_id == post_id,
        models.Post_Enlistment.user_id == user_id
    ).first()

def add_post_enlistment(db:Session,post_id:int,user_id:int):
    post_enlistment=models.Post_Enlistment(post_id=post_id,user_id=user_id)
    db.add(post_enlistment)
    db.commit()
    db.refresh(post_enlistment)
    return post_enlistment

def submit_post_report(db: Session, post_id: int, user_id: int, report_reason: schemas.Post_Report_Reason):
    report = models.Post_Report(post_id=post_id, user_id=user_id, report_reason=report_reason)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def get_all_post_reports(db: Session):
    return db.query(models.Post_Report).all()

def get_post_report(db: Session, post_id: int, user_id: int):
    return db.query(models.Post_Report).filter(
        models.Post_Report.post_id == post_id,
        models.Post_Report.user_id == user_id
    ).first()
    
def search_sort_and_filter_posts(db:Session,search_query:str|None,sort_type:schemas.Sort_Type):
    # search
    search = False
    if search_query:
        search_query = search_query.strip()
        if search_query != "":
            search = True
    # sort, apply filter and get posts
    # if search enabled, do not sort
    posts = get_all_posts_with_sorting_and_filtering(db,sort_type, not search)
    if search:
        print("will do search")
        search_posts:list[search_service.Search_Post]=[]
        for post in posts:
            tags:list[str]=[]
            for t in post.tags:
                tags.append(t.tag)
            search_posts.append(search_service.Search_Post(
                post.post_id,post.title,post.post_content,tags,
                post.creator.first_name,post.creator.last_name,post.creator.username))
        search_service.get_ranked_post(search_query,search_posts)
        # print(f'for query: "{search_query}".After search, result: is')
        # for s_post in search_posts:
        #     # print("post id: ",s_post.post_id," score: ",s_post.score," title: "+s_post.title)
        #     print(s_post)
        # now discard from search_posts that have score 0 in search_posts
        search_posts = list(filter(lambda s_post: s_post.score > 0, search_posts))
        # print("After filtering out score 0 posts, result is")
        # for s_post in search_posts:
        #     print(s_post)
        # now filter from posts that are in search_posts
        posts = list(filter(lambda post: post.post_id in list(map(lambda s_post: s_post.post_id, search_posts)), posts))
        # now sort search_posts by score
        search_posts.sort(key=lambda s_post: s_post.score, reverse=True)
        # print("After sorting search_posts, result is")
        # for s_post in search_posts:
        #     print(s_post)
        sorted_posts=[]
        for s_post in search_posts:
            sorted_posts.append(list(filter(lambda post: post.post_id == s_post.post_id, posts))[0])
        posts = sorted_posts
    else:
        print("wont do search cause search query is empty")
    # sort
    return posts
