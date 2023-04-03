import pika
from os import environ

hostname = environ.get('rabbit_host') or '127.0.0.1' # default hostname
port = environ.get('rabbit_port') or 5672 # default port

# Connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        # these parameters to prolong the expiration time (in seconds) of the connection
        heartbeat=3600, blocked_connection_timeout=3600,
    ))
channel = connection.channel()
# Set up the exchange if the exchange doesn't exist
# - use a 'topic' exchange to enable interaction
exchangename = "logging"
exchangetype = "direct"
channel.exchange_declare(exchange=exchangename,
                         exchange_type=exchangetype, durable=True)

############   Activity_Log queue    #############
queue_name = 'rewards_log'
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='log')

############   Email Notification queue    #############
queue_name = 'email_notification'
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='email')

############   Special Offer queue    #############
queue_name = 'special_offer'
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='specialOffer')

############   Special Offer Final queue    #############
queue_name = 'special_offer_final'
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='specialOfferFinal')

"""
This function in this module sets up a connection and a channel to a local AMQP broker,
and declares a 'topic' exchange to be used by the microservices in the solution.
"""
def check_setup():
    # The shared connection and channel created when the module is imported may be expired,
    # timed out, disconnected by the broker or a client;
    # - re-establish the connection/channel is they have been closed
    global connection, channel, hostname, port, exchangename, exchangetype

    if not is_connection_open(connection):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=hostname, port=port, heartbeat=3600, blocked_connection_timeout=3600))
    if channel.is_closed:
        channel = connection.channel()
        channel.exchange_declare(
            exchange=exchangename, exchange_type=exchangetype, durable=True)


def is_connection_open(connection):
    # For a BlockingConnection in AMQP clients,
    # when an exception happens when an action is performed,
    # it likely indicates a broken connection.
    # So, the code below actively calls a method in the 'connection' to check if an exception happens
    try:
        connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False
