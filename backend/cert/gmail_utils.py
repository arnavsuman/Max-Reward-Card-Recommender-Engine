import os
import pickle
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Authenticate and return Gmail service
def get_service():
    """Authenticate the user and return a Gmail service instance."""
    creds = None
    # Check if we have a token file (it stores the user's access and refresh tokens)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there's no valid token, request a new one via OAuth2
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    return service

# List message IDs
def list_messages(service, user_id='me', max_results=5):
    """Fetch list of message IDs."""
    try:
        response = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        return response.get('messages', [])
    except Exception as e:
        print(f"Error listing messages: {e}")
        return []

# Get full message by ID
def get_message(service, user_id, msg_id):
    """Fetch a full email message using its ID."""
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        return message
    except Exception as e:
        print(f"Error getting message: {e}")
        return None

# Extract Subject and From fields
def get_headers(message):
    """Extract 'Subject' and 'From' headers."""
    headers = message.get('payload', {}).get('headers', [])
    subject = sender = "Unknown"
    for header in headers:
        name = header.get('name')
        if name == 'Subject':
            subject = header.get('value')
        elif name == 'From':
            sender = header.get('value')
    return subject, sender

# Extract email content from the message
def get_message_content(message):
    """Extract the email body content from the message."""
    payload = message.get('payload', {})
    parts = payload.get('parts', [])
    
    def decode_base64(data):
        """Helper to decode base64 encoded data."""
        return base64.urlsafe_b64decode(data).decode('utf-8')

    # Look through all parts of the email (handling multipart emails)
    for part in parts:
        mime_type = part.get('mimeType')
        body_data = part.get('body', {}).get('data')
        if body_data:
            try:
                decoded = decode_base64(body_data)
                if mime_type == 'text/plain':
                    return decoded  # Extract the plain text body
                elif mime_type == 'text/html':
                    return decoded  # Extract the HTML body (if needed)
            except Exception as e:
                print(f"Decoding error: {e}")

    # Fallback to the top-level body if no parts found
    body_data = payload.get('body', {}).get('data')
    if body_data:
        try:
            return decode_base64(body_data)
        except Exception as e:
            print(f"Fallback decoding error: {e}")

    return "No readable content found."

def extract_credit_card_statement():
    """Main function to extract content from the latest credit card statement email."""
    service = get_service()
    messages = list_messages(service, max_results=5)  

    if not messages:
        print("No messages found.")
        return

    print("\n--- Searching for latest credit card statement email ---")
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

if __name__ == '__main__':
    extract_credit_card_statement()
