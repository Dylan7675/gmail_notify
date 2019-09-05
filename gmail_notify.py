from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import email
from apiclient import errors
import notify2
import os
import time
import sys
import subprocess

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()


    labels = results.get('labels', [])
    label_list = [label['name'] for label in labels]

    chosen_labels = []
    label_input = input(f"Input labels one-by-one that you would like desktop notifications from \n\n{label_list}: ")

    while True:

        if label_input not in label_list:
            label_input = input("\nPlease input a valid label name:\n")

        if label_input in label_list:
            chosen_labels.append(label_input)
            label_input = input("\nWould you like emails from any other label? If so type in the label. If not hit enter: ")
            if label_input == "":
                break

    label_id_list = []

    for item in chosen_labels:
        for label in labels:
            if label['name'] == item:
                label_id_list.append(str(label['id']))

    while True:

        unread_messages = get_message(service, label_id_list)
        notification(unread_messages)
        time.sleep(500)


def get_message(service, labels):

    snippets = []
    for label in labels:
        try:
            results = service.users().messages().list(userId='me', q='is:unread', labelIds = [label]).execute()
            messages = results.get('messages', [])

        except errors.HttpError as error:
            print(f"an error has occured: {error}")

        if not messages:
            print(f"No messages found.")
        else:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                snippets.append(msg['snippet'])

    return(snippets)


def notification(messages):

    icon_path = os.getcwd() + "/mail.png"
    notify2.init('Email Notify')
    for message in messages:
        n = notify2.Notification("Ticket Update", message, icon=icon_path)
        n.set_urgency(notify2.URGENCY_NORMAL)
        n.set_timeout(30000)
        n.show()
        time.sleep(10)


def notify_send(messages):
    for message in messages:
        update = f"New Ticket Update\n    {message}"
        subprocess.Popen([f"notify-send", '{update}'])

if __name__ == '__main__':
    main()
