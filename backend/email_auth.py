from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import base64
import os
import requests 
import json
from pymongo import MongoClient
import re


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Authenticate and return Gmail service
def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

# List message IDs
def list_messages(service, user_id='me', max_results=5):
    try:
        response = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        return response.get('messages', [])
    except Exception as e:
        print(f"Error listing messages: {e}")
        return []

# Get full message by ID
def get_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        return message
    except Exception as e:
        print(f"Error getting message: {e}")
        return None

# Extract Subject and From fields
def get_headers(message):
    headers = message.get('payload', {}).get('headers', [])
    subject = sender = "Unknown"
    for header in headers:
        name = header.get('name')
        if name == 'Subject':
            subject = header.get('value')
        elif name == 'From':
            sender = header.get('value')
    return subject, sender

# Extract email content
def get_message_content(message):
    payload = message.get('payload', {})
    parts = payload.get('parts', [])
    
    def decode_base64(data):
        return base64.urlsafe_b64decode(data).decode('utf-8')

    for part in parts:
        mime_type = part.get('mimeType')
        body_data = part.get('body', {}).get('data')
        if body_data:
            try:
                decoded = decode_base64(body_data)
                if mime_type == 'text/plain':
                    return decoded
                elif mime_type == 'text/html':
                    return decoded
            except Exception as e:
                print(f"Decoding error: {e}")

    # Fallback to top-level body
    body_data = payload.get('body', {}).get('data')
    if body_data:
        try:
            return decode_base64(body_data)
        except Exception as e:
            print(f"Fallback decoding error: {e}")

    return "No readable content found."


def main():
    service = get_service()
    messages = list_messages(service, max_results=10)  

    if not messages:
        print("No messages found.")
        return

    print(f"\n--- Searching for latest email from a bank ---")
    for msg in messages:
        msg_detail = get_message(service, 'me', msg['id'])
        if msg_detail:
            subject, sender = get_headers(msg_detail)
            if "Credit Card Statement" in subject:
                content = get_message_content(msg_detail)
                print(f"From   : {sender}")
                print(f"Subject: {subject}")
                print(f"Content:\n{content}\n")
                break
    else:
        print("No recent emails from a bank found.")


def parse_spends(content):
    try:
        spends = json.loads(content)
        # Optionally, ensure it only returns expected categories
        allowed = {"travel", "groceries", "dining"}
        return {k: float(v) for k, v in spends.items() if k in allowed}
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return {"travel": 0, "groceries": 0, "dining": 0}

def call_recommendation_api(spends):
    try:
        res = requests.post("http://localhost:8000/recommend", json=spends)
        if res.status_code == 200:
            print(f"\n Recommended Card: {res.json().get('recommended_card')}")
        else:
            print(f" API Error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f" Failed to call recommendation API: {e}")

def upload_mongoDB(sender, content, bank_name, personal_email, user_full_name):
    text = sender
    email_match = re.search(r"<([^>]+)>", text)

    if email_match:
        email = email_match.group(1).strip()
        
    client = MongoClient("mongodb://localhost:27017/")

    db = client["maxxmaicard"]

    statements_collection = db["statements"]

    document = {
        "emailID": email,
        "statement": content
    }

    statements_inserted_id = statements_collection.insert_one(document).inserted_id

    print(f"\n Inserted statement document with _id: {statements_inserted_id}")

    #USER PROFILE INSERTION

    statements_collection = db["user_profiles"]

    document2 = {
        "name": user_full_name,
        "email": personal_email,
        "statement_id": statements_inserted_id, 
        "preferences": {
            "bank": bank_name,  
            "has_existing_card": True
        }
    }

    # Insert document into collection
    inserted_id = statements_collection.insert_one(document2).inserted_id

    print(f"Inserted User Profile document with _id: {inserted_id}")

def main():
    service = get_service()
    messages = list_messages(service, max_results=10)

    if not messages:
        print("No messages found.")
        return

    print(f"\n--- Searching for latest email from a bank ---")
    for msg in messages:
        msg_detail = get_message(service, 'me', msg['id'])
        if msg_detail:
            subject, sender = get_headers(msg_detail)
            if "Credit Card Statement" in subject:
                content = get_message_content(msg_detail)
                print(f"From   : {sender}")
                print(f"Subject: {subject}")
                print(f"Content:\n{content}\n")

                # Step 1: Parse spends
                spends = parse_spends(content)
                print(f"Parsed Spends: {spends}")

                # Step 2: Call API
                call_recommendation_api(spends)

                #Step 3: Upload o MongoDB
                user_full_name = input("Enter Full Name: ")
                bank_name = input("Enter Preferred Banking Partner(s): ")
                personal_email = input("Enter Personal Email ID: ")
                upload_mongoDB(sender, content, bank_name, personal_email, user_full_name)
                break
    else:
        print("No recent emails from a bank found.")

if __name__ == "__main__":
    main()