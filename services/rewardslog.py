from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json,os, amqp_setup
from os import environ
import datetime, pytz
from threading import Thread

app = Flask(__name__)

# Routing key for AMQP
monitorBindingKey = 'rewards_log'

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define RewardLog Object
class RewardsLog(db.Model):
    __tablename__ = 'rewardslog'

    # a function which counts upwards
    i = 0

    def mydefault():
        global i
        i += 1
        return i

    redemptionsLogID = db.Column(
        db.Integer, primary_key=True, default=mydefault)
    redeemDate = db.Column(db.String(256), nullable=False)
    redemptionTime = db.Column(db.String(256), nullable=False)
    cid = db.Column(db.Integer, primary_key=True, default=mydefault)
    rid = db.Column(db.Integer, primary_key=True, default=mydefault)

    def __init__(self, redemptionsLogID, redeemDate, redemptionTime, cid, rid):
        self.redemptionsLogID = redemptionsLogID
        self.redeemDate = redeemDate
        self.redemptionTime = redemptionTime
        self.cid = cid
        self.rid = rid

    def json(self):
        return {"redemptionsLogID": self.redemptionsLogID, "redeemDate": str(self.redeemDate), "redemptionTime": str(self.redemptionTime),
                "cid": self.rid, "rid": self.rid}

# 1. Set up service to listen to AMQP Queue
def receiveRewardsLog():
    amqp_setup.check_setup()

    queue_name = 'rewards_log'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    # an implicit loop waiting to receive messages;
    amqp_setup.channel.start_consuming()
    # it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


# 2. Handle messages that are received from an AMQP
def callback(channel, method, properties, body):
    print("\nReceived a reward log by " + __file__)
    processRewardsLog(json.loads(body))

# 3. Defined function to indicate what to do with messsages
def processRewardsLog(body):
    print("Recording an Reward log:")

    # Define nested function to create reward log
    def create_reward_log():
        # Set up the application context
        with app.app_context():
            # Create new log
            query = text(
                "INSERT INTO rewardslog (redeemDate, redemptionTime, rid, cid) VALUES (:redeem_date, :redemption_time, :reward_id, :customer_id)")
            values = {'redeem_date': body['redeem_date'], 'redemption_time': body['redemption_time'],
                      'reward_id': body['reward_id'], 'customer_id': body['customer_id']}

            # Execute query
            db.session.execute(query, values)

            # Commit the changes to the database
            db.session.commit()

            # Return a JSON response with the created Reward object
            return jsonify(
                {
                    "code": 201,
                    "data": values
                }
            ), 201

    # Call the nested function to create the reward log
    return create_reward_log()

@app.route("/rewardslog")
def get_all():
    rewardsloglist = RewardsLog.query.all()
    if rewardsloglist:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "rewards": [log.json() for log in rewardsloglist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Reward log not found."
        }
    ), 404


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        monitorBindingKey, amqp_setup.exchangename))
    
    # Start the AMQP listener in a separate thread
    amqp_thread = Thread(target=receiveRewardsLog)
    amqp_thread.start()

    # Start the Flask app on the main thread
    app.run(host='0.0.0.0', port=5400, debug=True)
