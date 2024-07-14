import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Error to get your own credentials.json by creating a new project in the Google Cloud Console
# and enabling the Google Calendar and Google Sheets APIs
if not os.path.exists('credentials.json'):
    print("Error: You need to download a credentials.json file from the Google Cloud Console and save it in the same directory as this script.")
    exit()
    
# Configuration Constants
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = '<replace with calendar ID>'  # Use 'primary' for the user's primary calendar, or specify a calendar ID
EVENT_TAG = '<replace with a new event tag>'  # The tag used to identify events for deletion

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def delete_tagged_events():
    creds = get_credentials()
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        page_token = None
        deleted_count = 0
        
        while True:
            events = service.events().list(calendarId=CALENDAR_ID, pageToken=page_token).execute()
            for event in events['items']:
                if EVENT_TAG in event.get('description', ''):
                    service.events().delete(calendarId=CALENDAR_ID, eventId=event['id']).execute()
                    print(f"Deleted event: {event['summary']}")
                    deleted_count += 1
            
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        
        print(f"Total events deleted: {deleted_count}")
        
    except HttpError as error:
        print(f"An error occurred: {error}")

def main():
    print(f"This script will delete all events tagged with '{EVENT_TAG}' from your calendar.")
    confirmation = input("Are you sure you want to proceed? (yes/no): ")
    
    if confirmation.lower() == 'yes':
        delete_tagged_events()
    else:
        print("Operation cancelled.")

if __name__ == '__main__':
    main()