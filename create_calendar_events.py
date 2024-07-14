import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

# Error to get your own credentials.json by creating a new project in the Google Cloud Console
# and enabling the Google Calendar and Google Sheets APIs
if not os.path.exists('credentials.json'):
    print("Error: You need to download a credentials.json file from the Google Cloud Console and save it in the same directory as this script.")
    exit()

# Configuration Constants
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/spreadsheets.readonly']
SHEET_ID = '<replace with your sheet id>'  # The ID of the Google Sheet
CALENDAR_ID = '<replace with your calendar id>'  # Use 'primary' for the user's primary calendar, or specify a calendar ID
TIME_ZONE = '<replace with a timezone>'  # e.g., 'America/New_York'
EVENT_TAG = '<replace with a tag>'  # Unique tag for identifying these events

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

def get_schedule_from_sheet():
    creds = get_credentials()
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        # Get all values from the first sheet
        result = sheet.values().get(spreadsheetId=SHEET_ID, range='A:D').execute()
        values = result.get('values', [])
        
        # Remove header row and any empty rows
        return [row for row in values[1:] if row]
    except HttpError as err:
        print(f"An error occurred: {err}")
        return None

def create_calendar_events(schedule):
    creds = get_credentials()
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=7)
        
        for item in schedule:
            time, length, activity = item[0], item[1], item[2]
            notes = item[3] if len(item) > 3 else ""
            
            # Parse the time string
            hour, minute = map(int, time.split(':'))
            
            # Parse the length (assuming it's in minutes)
            duration = int(length)
            
            # Create start and end datetime objects
            start_datetime = datetime.datetime.combine(start_date, datetime.time(hour, minute))
            end_datetime = start_datetime + datetime.timedelta(minutes=duration)
            
            # Add the unique tag to the description
            full_description = f"{notes}\n\n{EVENT_TAG}"
            
            event = {
                'summary': activity,
                'description': full_description,
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': TIME_ZONE,
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': TIME_ZONE,
                },
                'recurrence': [
                    f'RRULE:FREQ=DAILY;UNTIL={end_date.strftime("%Y%m%dT%H%M%SZ")}'
                ],
            }
            
            event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")
            
    except HttpError as error:
        print(f"An error occurred: {error}")

def main():
    schedule = get_schedule_from_sheet()
    if schedule:
        create_calendar_events(schedule)

if __name__ == '__main__':
    main()