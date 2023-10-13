# Pollen-Notifier

## Weather API Area Code

Search for your city on https://weather.com. Then, use the end of the url for the "Area Code".
e.g. `https://weather.com/weather/today/l/<AREA_CODE>`

As of 10/12/2023, Fremont has "b04611dabb63304e2e67eea44799e41fcab2515aa88e2c6d5ff7f725d56af64d"

## Twilio API

Make a Twilio account and go through their set-up process. Need to define these env vars in .env:

- `ACCOUNT_SID`: Account SID, found in Account Info
- `AUTH_TOKEN`: Auth Token, found in Account Info
- `TWILIO_PHONE_NUMBER`: Your Twilio phone number, found in Account Info
- `RECEIVER_PHONE_NUMBER`: the phone number to send messages to for the app

## Installation

```
pip install -r requirements.txt
pip install pre-commit
pre-commit install
```

## Usage

```
python app.py
```
