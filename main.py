from fastapi import FastAPI, APIRouter, Depends
from posts.views import router as posts_router
from images.views import router as image_router
from new_posts.views import router as new_posts_router
import uvicorn
from fastapi.staticfiles import StaticFiles
from core.config import UPLOAD_DIR


app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name = 'static')
app.mount(f'/{UPLOAD_DIR}', StaticFiles(directory=UPLOAD_DIR), name='uploads')

app.include_router(posts_router)
app.include_router(image_router)
app.include_router(new_posts_router)


@app.get('/')
async def hello_world():
    return {'message': 'Hello world'}

if __name__ == "__main__":
    uvicorn.run('main:app', reload= True)