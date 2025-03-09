from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.pdf_routes import router as pdf_router

# Create FastAPI app
app = FastAPI(title="PDF Processing API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello from Python FastAPI!"}

# Register routers
app.include_router(pdf_router, prefix="/api", tags=["PDF Operations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True) 