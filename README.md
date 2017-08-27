# RemindMe
Automatically check train ticket availability and send SMS reminder if availability falls below certain number so that you don't forget to reserve your train tickets before the get sold out.

# Tech

RemindMe uses couple of open source and/or free projects, API's to work properly

  * [Mechanize] - Stateful programmatic web browsing in Python
  * [Twilio] - Give your web and mobile apps the power to exchange messages of any variety, from chat to SMS.

### Setup

- Create a free trial account in Twilio to recieve SMS in your verified phone number through the Twilio API. 
- Replace <account_sid>, <auth_token>, <your_phone_number> and <twilio_number> with the one from twilio.com/console after you signup.

### Installation

RemindMe was developed with Python v2.7

Install dependencies:

```sh
$ pip install -r requirements.txt
```

Run RemindMe

```sh
$ python remindme.py
```

### Todos

- Separate threshold for each train
- Include database/google spread sheet for storing journey details
- Interface for adding and removing trains from stored journeys