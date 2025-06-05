from fastapi import FastAPI, APIRouter, Depends
from posts.views import router as posts_router
from images.views import router as image_router
from new_posts.views import router as new_posts_router
from users.views import router as user_router
from auth.views import router as jwt_router
import uvicorn
from fastapi.staticfiles import StaticFiles
from core.config import UPLOAD_DIR
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name = 'static')
app.mount(f'/{UPLOAD_DIR}', StaticFiles(directory=UPLOAD_DIR), name='uploads')

app.include_router(posts_router)
app.include_router(image_router)
app.include_router(new_posts_router)
app.include_router(user_router)
app.include_router(jwt_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

@app.get('/')
async def hello_world():
    return {'message': 'Hello world'}

if __name__ == "__main__":
    uvicorn.run('main:app', reload= True)