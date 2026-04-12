from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "CSV Cleaner API is running"}


# ---------------- MAIN ENTRY POINT ----------------
def main():
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=7860,
        reload=True
    )


if __name__ == "__main__":
    main()
