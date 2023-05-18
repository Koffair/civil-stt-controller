# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

dircontent = os.listdir(os.getenv('INPUT_FOLDER'))
print(dircontent)

app = FastAPI()
@app.get("/")
async def root():
 return {"dircontetn":dircontent}
 