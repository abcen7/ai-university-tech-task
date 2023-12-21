from fastapi import FastAPI
from aiohttp import ClientError, ClientSession, TCPConnector
import uvicorn

from fastapi import FastAPI
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fetch_github_user import get_github_user
from os.path import abspath

app = FastAPI()

# Настройка для Google Sheets
PATH_TO_FILE = abspath("./10/google-credentials.json")
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_TO_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open("TechnicalTaskTest").sheet1

@app.get("/get_user/{username}")
async def get_user(username: str):
    user_info = await get_github_user(username)
    if user_info:
        sheet.append_row([value for value in user_info.values() if value])
    return user_info

@app.get("/get_sheet_data")
async def get_sheet_data():
    data = sheet.get_all_values()
    return data
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)