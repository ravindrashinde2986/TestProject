from fastapi import FastAPI
from . import models
from .database import engine
from .router import users, posts, auth, vote

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)

# my_posts = [
#     {"id": 1, "title": "list of tech books", "content": "Check out these books"},
#     {
#         "id": 2,
#         "title": "list of beaches in maharashtra",
#         "content": "Check out these amazing beaches",
#     },
# ]
#
# current_post_id = 2
#
# # try:
# #     con = psycopg2.connect(database='TestProject', user='postgres', password='root@123', port=5434, cursor_factory=RealDictCursor)
# #     cur =  con.cursor()
# #     print("database connection was successful !")
# # except Exception as Error:
# #     print(f"Error while connecting the databse {Error}")
#
#
# def find_post(id):
#     for post in my_posts:
#         if post["id"] == int(id):
#             return post
#
#
# def find_the_post_index(id):
#     print(id, type(id))
#     for index, post in enumerate(my_posts):
#         print(post["id"])
#         print(index)
#         if post["id"] == id:
#             return index
