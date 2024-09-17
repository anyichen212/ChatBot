import os.path
import json
from dotenv import load_dotenv
import requests
import asyncio

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

load_dotenv()
# The ID and range of a sample spreadsheet.
SHEET_ID = "1QJe-Nipz7pQ6ADQJcErxyfgRHWoWKOT62Yt-Qgk7mJI" #"1aja-o-wPhztpV-oEJbJzuDLq7WkYjBZhlZOi4_yiY8o"
RANGE_NAME = "Sheet1!A1:C2"
SERVER_ID = int(os.getenv('SERVER_ID'))
BOAT_TOKEN = os.getenv('BOAT_TOKEN')


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
        # Pass: spreadsheet_id,  range_name, value_input_option and  _values
    # update_values(
    #     creds,
    #     SPREADSHEET_ID,
    #     "A1:C2",
    #     "USER_ENTERED",
    #     [["A", "Bitch"], ["C", "D"]],
    # )


    # edit for testing
    #asyncio.run(time())
    #setBoat()
    #test_boat()
    #update_values(sheet)
    #get_values(sheet)
    read_json()

async def time():
    print(0)
    await asyncio.sleep(0.1)
    print(1)

def test_boat():
    api = f"https://unbelievaboat.com/api/v1/guilds/{SERVER_ID}/users/{292401603493756928}"
    res = requests.get(api,headers={"Authorization": BOAT_TOKEN})
    print(res.json())

def setBoat():
    api = f"https://unbelievaboat.com/api/v1/guilds/{SERVER_ID}/users/{292401603493756928}"
    res = requests.patch(api, json={'cash':300}, headers={
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": BOAT_TOKEN})
    print(res.json().get("cash"))

def update_values(sheet):
    sheetData = sheet.values().batchGet(
        spreadsheetId=SHEET_ID, 
        ranges=["[Log]Community!A:E", "[Log]Community!J2", "[Log]Community!I4:J"], 
    ).execute().get("valueRanges")
    print(sheetData[2].get("values"))

def get_values(sheet):
    sheetData = sheet.values().get(
        spreadsheetId=SHEET_ID, 
        range="[Log]Villagerdata!A3:O" 
    ).execute().get("values")
    print(sheetData)

    for i,val in enumerate(sheetData[0]):
        new_val = val.split('.')[0]
        new_val = new_val.lower()
        sheetData[0][i] = new_val

    idx = 1
    sheet_len = len(sheetData)
    data = {"key":{}}
    while idx < sheet_len:
        chara_data = {}
        for i,val in enumerate(sheetData[0]):
            chara_data[val] = sheetData[idx][i]

        data["key"][chara_data["name"].lower()] = chara_data["id"]
        data["key"][chara_data["alias"].lower()] = chara_data["id"]

        data[chara_data["id"]] = chara_data
        idx += 1
    with open("vgData.json", mode="w", encoding="utf-8") as write_file:
        json.dump(data, write_file, indent=4)

def read_json():
    with open('vgData.json', 'r') as file:
        data = json.load(file)
    
    charaKey = data["key"]
    print(charaKey)

if __name__ == "__main__":
  main()