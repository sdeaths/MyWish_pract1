from fastapi import FastAPI 
 
from rest.ad_router import ads_router 
 
app = FastAPI(title='Ads Service') 
 
app.include_router(ads_router, prefix='/api')