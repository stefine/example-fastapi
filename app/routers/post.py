from app import schema, models
from app.database import get_db
from fastapi import status, Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from app.routers import oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


# @router.get("/", response_model=List[schema.Post])
@router.get("/", response_model=List[schema.PostWithCounts])
async def get_posts(db: Session = Depends(get_db), search: Optional[str] = "",
                    limit: int = 10, skip: int = 0):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)) \
    #     .order_by(models.Post.id).limit(limit=limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Votes.post_id)) \
        .join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True) \
        .group_by(models.Post.id).filter(models.Post.title.contains(search)) \
        .order_by(models.Post.id).limit(limit=limit).offset(skip).all()
    results = [{"post": post[0], "vote_count": post[1]} for post in posts]
    # results = db.query(models.Post, models.User.email, func.count(models.Votes.post_id)) \
    #     .join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True) \
    #     .join(models.User, models.Post.owner_id == models.User.id, isouter=True) \
    #     .group_by(models.Post.id, models.User.email).all()
    return results


@router.get("/{id}", response_model=schema.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    # url extracts the parameter and you can pass it to our function
    # post_id, res = find_post_and_id(id)
    # if post_id is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"message: post id with {id} not found")
    # # res = my_posts[post_id] if post_id is not None else f"message: post id with {id} not found"
    # # response.status_code = status.HTTP_404_NOT_FOUND if post_id is None else status.HTTP_200_OK

    # cursor.execute("""SELECT * FROM posts WHERE id=(%s)""", (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message: post id with {id} is not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
async def create_posts(post: schema.PostRequest, db: Session = Depends(get_db),
                       current_user=Depends(oauth2.get_current_user)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 10000)
    # my_posts.append(post_dict)
    # # we can convert pydantic model to dictionary by using .dict()
    # cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """,
    #                (post.title, post.content))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    owner_id = current_user.id
    new_post = models.Post(owner_id=owner_id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db),
                      current_user=Depends(oauth2.get_current_user)):
    # post_idx = find_post_index(id)
    # if post_idx is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"message: post id with {id} not found")
    # my_posts.pop(post_idx)
    # cursor.execute("""DELETE FROM posts WHERE id=(%s) RETURNING * """, (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message: post id with {id} not found")
    current_id = current_user.id
    if post.first().owner_id == current_id:
        post.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform delete action")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.Post)
async def update_post(data: dict, id: int, db: Session = Depends(get_db),
                      user_id: int = Depends(oauth2.get_current_user)):
    # post_idx = find_post_index(id)
    # if post_idx is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"message: post id with {id} not found")
    # my_posts[post_idx].update(data)
    # sql = """UPDATE posts SET """ + \
    #       ",".join(k + "=(%s) " for k in data.keys()) + \
    #       """WHERE id=(%s) RETURNING *"""
    # values = tuple(data.values()) + (id,)
    # cursor.execute(sql, values)
    # update_post = cursor.fetchone()

    update_post = db.query(models.Post).filter(models.Post.id == id)
    if update_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message: post id with {id} not found")
    update_post.update(data, synchronize_session=False)
    db.commit()
    # 这里的first()相当于returning *
    return update_post.first()
