# Gmail_Notify

This is a project that checks any given Gmail inbox label for unread messages and sends a desktop notification every five minutes until the email has been marked as read. I created this tool because I found it really helpful to get constant reminders of emails that I regarded as important. 

## Getting Started

To get started clone this repository into your local enviroment.

### Prerequisites

Python 3.X

Gmail account

[Gmail API access](https://developers.google.com/gmail/api/quickstart/python)

### Installing

Clone this repository to your local enviroment.

```
git clone git@github.com:Dylan7675/gmail_notify.git
```

Change directories into gmail_notify. 

```
cd gmail_notify/
```

Install the required dependencies.

```
pip3 install -r requirements.txt
```

Enable Gmail API.

```
Follow the link in the prerequisits section and enable the Gmail API. This will download a credentials.json file.
```

Move the credentials file to the repository.

```
mv ~/Downloads/credentials.json .
```

### Running the script

This script can be easily ran with the standard python .py execution.

```
python3 gmail_notify.py
``` 

## Acknowledgments

* Big thanks to the writers of the Gmail API for the well writen documentaion and quick-start script.

