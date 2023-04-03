from flask import Flask
from flask_cors import CORS
from invokes import invoke_http
import amqp_setup, json, os


app = Flask(__name__)
CORS(app)

# Routing key for AMQP
monitorBindingKey = 'special_offer'

# 1. Set up service to listen to AMQP Queue
def receiveSpecialOffer():
    amqp_setup.check_setup()
    queue_name = 'special_offer'

    # Set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming()

# 2. Handle messages that are received from an AMQP
def callback(channel, method, properties, body):
    print("\nReceived a special offer log by " + __file__)
    processSpecialOffer(json.loads(body))

# 3. Defined function to indicate what to do with messsages
def processSpecialOffer(body):
    print("Recording an Special Offer log:")

    # Collect customer details that are of matching reward tier
    customersInTier = invoke_http("http://customer:5200/customer/customer_by_tier/" + body['rewardTier'])
    for customer in customersInTier['customer']:
        # putting it together in a json
        specialOffer_email_details = {"customer_email": customer["email_addr"],
                                    "customer_name": customer["name"],
                                    "reward_name": body['rewardName'],
                                    "points": body['points'],
                                    "promo_points": body['promo_points'],
                                    "startDate": body['startDate'],
                                    "endDate": body['endDate']
                                    }
        # Publish to email_api.py to be mass send
        message = json.dumps(specialOffer_email_details)
        print('-----Publishing the (special offer email content) message with routing_key=specialOffer_email_content-----')
        print(customer["email_addr"])
        # publish to email_api so will require another routing key
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="specialOfferFinal",body=message)
        print("Special offer email content published to RabbitMQ Exchange.")        


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    # app.run(port=6000, debug=True)
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        monitorBindingKey, amqp_setup.exchangename))
    receiveSpecialOffer()
