# main.py
# FastAPI application with CRUD endpoints.
# Demonstrates dependency injection, database session handling, and REST design.

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, auth
from database import SessionLocal, engine
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Create all tables defined in models (if they don't exist)
models.Base.metadata.create_all(bind=engine)

# Create FastAPI instance with a title (shows in docs)
app = FastAPI(title="Simple CRUD API")


# Mount static files (for the frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the main HTML page at the root
@app.get("/")
def read_root():
    return FileResponse("static/index.html")


# Dependency: provide a database session per request and close it afterwards
def get_db():
    db = SessionLocal()
    try:
        yield db          # yield session to endpoint function
    finally:
        db.close()        # always close after request

# ----------------------------
# Authentication Endpoints
# ----------------------------

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    """Create a new user account."""
    # Check if username already exists
    existing_user = auth.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    # Hash password and save user
    hashed = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    """Authenticate user and return JWT token."""
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create token with user id as subject
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}




# ----------------------------
# Create a new item, Protected Item Endpoints
# ----------------------------

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)  # require auth
                ):
    # Convert Pydantic model to dict, then create ORM instance
    db_item = models.Item(**item.model_dump())
    db.add(db_item)        # add to session (pending)
    db.commit()            # save to database
    db.refresh(db_item)    # refresh to get generated id
    return db_item         # response_model converts ORM object to dict

# ----------------------------
# List items with pagination
# ----------------------------
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: models.User = Depends(auth.get_current_user)):
    # Query all items, skip and limit for basic pagination
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items

# ----------------------------
# Get a single item by ID
# ----------------------------
@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db),current_user: models.User = Depends(auth.get_current_user)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        # Return 404 if not found
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# ----------------------------
# Update an existing item
# ----------------------------
@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    # Update fields from the incoming data
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

# ----------------------------
# Delete an item
# ----------------------------
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}