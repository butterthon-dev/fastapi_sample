from api.endpoints.swagger_ui import openapi, swagger_ui_router
from api.endpoints.v1 import api_v1_router
# from fastapi import FastAPI
from core.config import get_env
from core.fastapi import FastAPI  # オーバーライドしたFastAPIクラスを使用する
from middleware import (
    CORSMiddleware,
    HttpRequestMiddleware
)

app = FastAPI(
    docs_url=None,  # Noneを設定しないとswagger-uiのルーターで定義したものに変わらない
    redoc_url=None,  # Noneを設定しないとswagger-uiのルーターで定義したものに変わらない
)

app.include_router(api_v1_router, prefix='/api/v1')

# ミドルウェアの設定
app.add_middleware(HttpRequestMiddleware)
app.add_middleware(CORSMiddleware)


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# swagger-uiは開発時のみ表示されるようにする
if get_env().debug:
    app.include_router(swagger_ui_router)
    app.openapi = openapi
