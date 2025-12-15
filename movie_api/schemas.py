from pydantic import BaseModel, Field

class MovieCreate(BaseModel):
    title : str = Field(min_length=1, max_length=100)
    director : str = Field(min_length=1, max_length=50)
    year : int = Field(ge=1900,le=2050)
    rating: float = Field(ge=1.0, le=10.0,default=7.0)
    available: bool = True


class Movie(MovieCreate):
    id : int
    owner_id : int | None = None

    class Config:
        from_attributes = True

class MovieUpdate(BaseModel):
    title : str | None = Field(default=None,min_length=1,max_length=100)
    director : str | None = Field(default=None,min_length=1,max_length=50)
    year : int | None = Field(default=None,ge=1900,le=2050)
    rating : float | None = Field(default=None,ge=1.0,le= 10.0)
    available : bool | None = None

class UserCreate(BaseModel):
    username : str = Field(min_length=1, max_length=50)
    password : str = Field(min_length=8, max_length=100)
    email : str | None =Field(default=None, min_length=8, max_length=100)

class User(BaseModel):
    id : int
    username : str
    email : str
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username : str = Field(min_length=1, max_length=50)
    password : str = Field(min_length=8, max_length=100)


