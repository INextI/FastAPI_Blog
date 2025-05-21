from fastapi import FastAPI, APIRouter, Depends
from posts.views import router as posts_router
import uvicorn

app = FastAPI()


app.include_router(posts_router)


@app.get('/')
async def hello_world():
    return {'message': 'Hello world'}

if __name__ == "__main__":
    uvicorn.run('main:app', reload= True)