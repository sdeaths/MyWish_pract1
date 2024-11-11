from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import random

DATABASE_URL = "postgresql://postgres:postgres@ad_db/ad_db"

app = FastAPI()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    gifts = relationship("Gift", back_populates="wishlist")

class Gift(Base):
    __tablename__ = "gifts"
    id = Column(Integer, primary_key=True, index=True)
    wishlist_id = Column(Integer, ForeignKey("wishlists.id"))
    name = Column(String)
    wishlist = relationship("Wishlist", back_populates="gifts")

Base.metadata.create_all(bind=engine)

# Pydantic schemas
class WishlistCreate(BaseModel):
    user_id: int
    interests: list[str]

class GiftResponse(BaseModel):
    id: int
    name: str

class WishlistResponse(BaseModel):
    id: int
    user_id: int
    gifts: list[GiftResponse]

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mock function to generate gift ideas based on interests
def generate_gift_ideas(interests):
    # Sample gift ideas associated with interests
    gift_ideas = {
        "technology": ["Smartphone", "Laptop", "Tablet"],
        "sports": ["Football", "Basketball", "Tennis Racket"],
        "books": ["Fantasy Novel", "Science Book", "Mystery Novel"],
        "music": ["Guitar", "Piano", "Headphones"],
        "art": ["Paint Set", "Sketchbook", "Easel"]
    }
    ideas = []
    for interest in interests:
        if interest in gift_ideas:
            ideas.extend(gift_ideas[interest])
    return ideas if ideas else ["Gift Card"]

# Endpoint to create a wishlist
@app.post("/create_wishlist", response_model=WishlistResponse)
def create_wishlist(wishlist_data: WishlistCreate, db: Session = Depends(get_db)):
    # Create the wishlist
    wishlist = Wishlist(user_id=wishlist_data.user_id)
    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)

    # Generate gift ideas based on interests
    gift_ideas = generate_gift_ideas(wishlist_data.interests)

    # Add gifts to the wishlist
    for idea in gift_ideas:
        gift = Gift(wishlist_id=wishlist.id, name=idea)
        db.add(gift)

    db.commit()

    # Reload the wishlist with gifts for response
    db.refresh(wishlist)
    return WishlistResponse(
        id=wishlist.id,
        user_id=wishlist.user_id,
        gifts=[GiftResponse(id=gift.id, name=gift.name) for gift in wishlist.gifts]
    )

# Endpoint to retrieve a wishlist by user ID
@app.get("/wishlist/{user_id}", response_model=WishlistResponse)
def get_wishlist(user_id: int, db: Session = Depends(get_db)):
    wishlist = db.query(Wishlist).filter(Wishlist.user_id == user_id).first()
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    return WishlistResponse(
        id=wishlist.id,
        user_id=wishlist.user_id,
        gifts=[GiftResponse(id=gift.id, name=gift.name) for gift in wishlist.gifts]
    )
