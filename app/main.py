from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
#             {"title": "favoriate foods", "content": "I like pizza", "id": 2}]
#
#
# def find_post_and_id(id):
#     post_id, res = None, None
#     for post in my_posts:
#         if post["id"] == id:
#             post_id = id
#             res = post
#     return post_id, res
#
#
# def find_post_index(id):
#     post_idx = None
#     for idx, post in enumerate(my_posts):
#         if post["id"] == id:
#             post_idx = idx
#     return post_idx

# 这个get url不能放置在底下，原因是会把latest看做id，然后validate
# 所以url function的位置是对api有影响的
# @app.get("/posts/latest")
# async def get_post():
#     post = my_posts[len(my_posts) - 1]
#     return {"message": post}
