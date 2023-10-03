import uvicorn

from src.app import create_app
from src.utils.dummy_data import create_dummy_data

app = create_app()


# Create dummy data on startup
@app.on_event("startup")
async def startup():
    await create_dummy_data()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
