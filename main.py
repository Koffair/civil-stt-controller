# main.py
from fastapi import FastAPI
import os

dircontent = os.listdir("/var/www/html")
print(dircontent)

app = FastAPI()
@app.get("/")
async def root():
 return {"dircontetn":dircontent}
 