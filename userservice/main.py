from userservice.routers import auth, manageUser
from fastapi import FastAPI

app = FastAPI(
    title='User Service',
    version='1.0.0'
)

app.include_router(auth.router)
app.include_router(manageUser.router)


