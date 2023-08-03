from fastapi import FastAPI
from routes.recipient_list import recipient_routes
from routes.user import user_routes  # Import user route file
from config.config import settings
import uvicorn

app = FastAPI()


app.include_router(user_routes)  # Include user routes in the app
app.include_router(recipient_routes)  # Include user routes in the app

# @app.get('/health')
# async def health_check():
#     return {'status': 'ok 👍 '}

if __name__ == "__main__":
    port = int(settings.PORT)

    app_module = "main:app"
    uvicorn.run(app_module, host="0.0.0.0", port=port, reload=True)