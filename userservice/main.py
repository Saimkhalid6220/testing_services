from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional , Annotated
from fastapi import FastAPI,Depends
from sqlmodel import Field, SQLModel, Session, create_engine
from userservice import setting


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str = Field(index=True)

class User_session(User):
    acess_token:str

connectionString = str(setting.DATABASE_URL).replace(
    "postgresql" , "postgresql+psycopg"
)

engine = create_engine(connectionString , connect_args={})

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app:FastAPI)-> AsyncGenerator[None , None]:
    print("hooray  creating tables")
    create_db_and_table()
    yield

app = FastAPI()

def getSession():
    with Session(engine) as session:
        yield session

@app.post('/user/register' , response_model = User)
def register_user(user:User  ,session : Annotated[Session , Depends(getSession)])->User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# @app.post('/user/login' , response_model=User_session)
# def login_user(user:User , session:Annotated[Session , Depends(getSession])->User_session:
               
