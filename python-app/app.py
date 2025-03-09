# This file is kept for compatibility with the original structure
# The main application is now in main.py

from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000) 