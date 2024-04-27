from fastapi import FastAPI
from app.schemas.schemas import VersionAPI
from app.routes import users, sub_users, town_hall


app = FastAPI()
app.title= "API: Solid Waste Collection Manager (SWCM)"
app.description= "SWCM or Solid Waste Collection Manager is an API written in Python, and developed by Johns-mx."
app.version= VersionAPI().version


app.include_router(users.user_router, prefix=f"/api/v{VersionAPI().major}/user", tags=["Users"])
app.include_router(sub_users.subuser_router, prefix=f"/api/v{VersionAPI().major}/user/sub", tags=["Sub users"])
app.include_router(town_hall.twn_hall_router, prefix=f"/api/v{VersionAPI().major}/town_hall", tags=["Town Hall"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)