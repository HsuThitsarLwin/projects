from flask import Flask
from exchangelib import Account, Credentials, Message, Mailbox
import json, os, amqp_setup

app = Flask(__name__)

# Routing key for AMQP
monitorBindingKey = ['email', 'specialOfferFinal']

# Credentials for Sender Email
email_address = "esdteam7@outlook.com"
username = "esdteam7@outlook.com"
password = "esd7huatah"
server_url = "https://outlook.office365.com"

credentials = Credentials(username=username, password=password)

# Set up the account and connect to the Exchange server
account = Account(primary_smtp_address=email_address, credentials=credentials, autodiscover=True,
                  config=None)

# 1. Set up service to listen to the two queues: email notification and special_offer_final
def recieveMessage():
    amqp_setup.check_setup()

    queue_name = 'email_notification'
    queue_name_two = 'special_offer_final'

    # NOTE: This listens for email for redemption scenario
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    
    # NOTE: This listens for when special offer is created
    amqp_setup.channel.basic_consume(
        queue=queue_name_two, on_message_callback=callback_two, auto_ack=True)
    
    amqp_setup.channel.start_consuming()


# 2. Handle messages that are received from queue email_notifications
def callback(channel, method, properties, body):
    print("\nReceived an email log by " + __file__)
    processRedemption(json.loads(body))

# 2b. Handle messages that are received from queue special_offer_final
def callback_two(channel, method, properties, body):
    print("\nReceived an special offer log by " + __file__)
    processSpecialOffer(json.loads(body))


# 3. Defined function to indicate what to do with messsages
def processRedemption(body):
    messageContent = f"Dear {body['customer_name']},\n\nWe are pleased to inform you that your {body['reward_name']} has been successfully redeemed!\n\nReward cost: {body['reward_cost']}\nYour current reward points balance: {body['customer_points']}\n\nThank you for using redeemNow!\n\nBest regards,\nredeemNow team"

    print("Compiling email redeem log")

    def send_email():
        # Create Message Object
        message = Message(
            account=account,
            subject="Redemption Successful",
            body=messageContent,
            to_recipients=[Mailbox(email_address=body['customer_email'])]
        )

        # Send the message
        message.send_and_save()
        return 'Email sent successfully'

    send_email()

# 3b. Defined function to mass send email to all customer of same tier
def processSpecialOffer(body):
    print("Printing email special offer log")
    messageContent = f"Dear {body['customer_name']},\n\nWe would like to inform you of a special offer taking place from {body['startDate']} to {body['endDate']}.\n\n{body['reward_name']} usually cost {body['points']} but can now be redeemed for {body['promo_points']}! Make sure to seize this offer while stocks last!\n\nBest Regards,\nredeemNow! Team"
    print(body['customer_name'])

    def send_specialOffer():
        # Create Message Object
        message = Message(
            account=account,
            subject="Special Offer Now",
            body=messageContent,
            to_recipients=[Mailbox(email_address=body['customer_email'])]
        )

        # Send the message
        message.send_and_save()
        return 'Special Offer sent successfully'

    send_specialOffer()

# Execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        monitorBindingKey, amqp_setup.exchangename))
    recieveMessage()
