from pollen_scraper import extract_pollen_info
from twilio_gateway import TwilioGateway

# Use Fremont since Union City page has less information
FREMONT_AREA_CODE = "b04611dabb63304e2e67eea44799e41fcab2515aa88e2c6d5ff7f725d56af64d"


def main():
    pollen_info = extract_pollen_info(FREMONT_AREA_CODE)
    print(pollen_info)

    twilio_gateway = TwilioGateway()
    message = twilio_gateway.send_message(pollen_info)
    print(message.sid)


if __name__ == "__main__":
    main()
