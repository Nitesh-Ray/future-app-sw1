# schemas.py
# Pydantic schemas for request/response validation and serialization.
# These ensure data coming in/out matches expected types and shapes.

from pydantic import BaseModel, ConfigDict, Field

class ItemBase(BaseModel):
    """Common fields for item creation and display."""
    name: str
    description: str | None = None   # optional, can be null
    price: float

class ItemCreate(ItemBase):
    """Schema used when creating a new item (same as base, but explicit)."""
    pass

class Item(ItemBase):
    """Schema used for responses; includes the database id."""
    model_config = ConfigDict(from_attributes=True)  # allows ORM objects to be read
    id: int


# ----- User schemas -----
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str = Field(..., max_length=72)   # bcrypt limit

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# ----- Token schema for login response -----
class Token(BaseModel):
    access_token: str
    token_type: str

