from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pika
import json
from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError


DATABASE_URL = "postgresql://postgres:postgres@user_db/user_db"

app = FastAPI()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# RabbitMQ connection
def send_message(queue, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message))
    connection.close()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.password_hash)

class Friend(Base):
    __tablename__ = "friends"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    friend_id = Column(Integer, ForeignKey("users.id"))

class Interest(Base):
    __tablename__ = "interests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)

Base.metadata.create_all(bind=engine)

# Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

class FriendRequest(BaseModel):
    friend_id: int

class InterestRequest(BaseModel):
    interest: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    send_message("user_events", {"event": "UserRegistered", "user_id": user_obj.id})
    return user_obj

@app.post("/login")
def login_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.post("/add_friend")
def add_friend(friend_request: FriendRequest, db: SessionLocal = Depends(get_db)):
    # Check if the friend exists in the users table
    friend = db.query(User).filter(User.id == friend_request.friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    # Create the friendship record
    new_friendship = Friend(user_id=1, friend_id=friend_request.friend_id)
    db.add(new_friendship)

    try:
        db.commit()
        send_message("user_events", {"event": "FriendAdded", "friend_id": friend_request.friend_id})
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add friend due to database constraints")

    return {"message": "Friend added"}

@app.post("/add_interest")
def add_interest(interest_request: InterestRequest, db: SessionLocal = Depends(get_db)):
    interest = Interest(user_id=1, name=interest_request.interest)
    db.add(interest)
    db.commit()
    send_message("user_events", {"event": "InterestAdded", "interest": interest_request.interest})
    return {"message": "Interest added"}
