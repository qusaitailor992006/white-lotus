import uvicorn
import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"🌸 Starting White Lotus: Food Vibe Folks application on http://{host}:{port}")
    print(f"👉 Public Website:   http://{host}:{port}/")
    print(f"👉 Admin Dashboard:  http://{host}:{port}/admin")
    print(f"👉 Admin Login:      http://{host}:{port}/admin/login")
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
