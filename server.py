import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run('src.fastapi_app:app', host="0.0.0.0",
                port=int(os.getenv('PORT', '8000')),
                reload=True)
