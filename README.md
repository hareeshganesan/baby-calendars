# Baby Schedule Calendar Scripts

This project contains two Python scripts for managing a baby's schedule in Google Calendar:

1. `create_calendar_events.py`: Creates recurring calendar events from a CSV file.
2. `delete_calendar_events.py`: Bulk deletes calendar events with a specific tag.

## Prerequisites

- Python 3.6 or higher
- Google account with Calendar API enabled
- `credentials.json` file for Google Calendar API authentication

## Setup

1. Clone this repository or download the scripts to your local machine.

2. Install required Python packages:
   ```
   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

3. Set up Google Calendar API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - Create credentials (OAuth 2.0 Client ID)
   - Download the credentials and save as `credentials.json` in the same directory as the scripts

## Usage

### Creating Calendar Events

1. Prepare your CSV file with the following columns:
   - Start Time (HH:MM format)
   - Length (in minutes)
   - Activity
   - Notes (optional)

2. Update the `create_calendar_events.py` script:
   - Set `SHEET_ID` to your Google Sheet ID (if using Google Sheets)
   - Set `CALENDAR_ID` to your desired calendar ID (use 'primary' for primary calendar)
   - Set `TIME_ZONE` to your time zone (e.g., 'Europe/London')
   - Adjust `EVENT_TAG` if desired

3. Run the script:
   ```
   python create_calendar_events.py
   ```

4. Follow the authentication prompts in your web browser.

### Deleting Calendar Events

1. Ensure the `delete_calendar_events.py` script has the correct `EVENT_TAG` matching the one used in event creation.

2. Run the script:
   ```
   python delete_calendar_events.py
   ```

3. Confirm the deletion when prompted.

## Important Notes

- The creation script generates events for one week by default. Modify the script if a different time range is needed.
- The deletion script will remove ALL events with the specified tag. Use with caution.
- These scripts do not handle event conflicts. Ensure your calendar is prepared for bulk additions or deletions.
- Always back up your calendar data before running these scripts.

## Troubleshooting

- If you encounter authentication issues, delete the `token.json` file (if it exists) and re-run the script to re-authenticate.
- For API errors, check your `credentials.json` file and ensure the Calendar API is enabled in your Google Cloud Console.

## Limitations

- The scripts do not handle timezone changes or daylight saving time transitions automatically.
- There's no built-in conflict resolution for overlapping events.
- The scripts do not provide options for updating existing events without deletion.

## Contributing

Feel free to fork this project and submit pull requests for any enhancements.

## License

This project is licensed under the MIT License.