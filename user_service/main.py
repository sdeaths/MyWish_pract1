from fastapi import FastAPI 
 
from rest.users_router import users_router 
 
app = FastAPI(title='Users Service') 
 
app.include_router(users_router, prefix='/api')