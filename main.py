from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import socket
import uvicorn
from router.router import router
from config.database import get_db


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Chat Server!"}


@app.middleware("http")
async def log_request_info(request: Request, call_next):
    body = await request.body()
    print("📥 Request:", request.method, request.url)
    print("🔧 Headers:", dict(request.headers))
    print("🧾 Body:", body.decode("utf-8"))
    response = await call_next(request)
    return response


def get_local_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "127.0.0.1"


if __name__ == "__main__":
    ip = get_local_ip()
    print(f"🚀 Server đang chạy tại: http://{ip}:8888")
    print("🌐 Bạn có thể truy cập API trên thiết bị khác cùng Wi-Fi bằng IP này.")
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
