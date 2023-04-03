from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
import amqp_setup, json

app = Flask(__name__)
CORS(app)

# 0. To update the promo_points, startDate, endDate of a reward for specialOffer, pass in RID only
@app.route('/specialOffer', methods=['PUT'])
def specialOffer():

    data = request.get_json()
    rid = data['params']['rid']
    startdatetime= data['params']["startdatetime"]
    enddatetime = data['params']['enddatetime']
    promopoints = data['params']['promopoints']

    try:
        # 1. Get reward details
        reward_url = "http://reward:5000/reward/" + str(rid)
        rewardDetails = invoke_http(reward_url, method='GET')

        # 2. Get special offer details from user input
        is_specialOffer = '1'
        promo_points = promopoints
        startDate = startdatetime
        endDate = enddatetime

        # 3. Update reward with special offer details
        specialOffer_details = {"category": rewardDetails['data']['category'],
                                "endDate": endDate,
                                "is_specialOffer": is_specialOffer,
                                "latitude": rewardDetails['data']['latitude'],
                                "longitude": rewardDetails['data']['longitude'],
                                "points": rewardDetails['data']['points'],
                                "promo_points": promo_points,
                                "quantity": rewardDetails['data']['quantity'],
                                "region": rewardDetails['data']['region'],
                                "rewardName": rewardDetails['data']['rewardName'],
                                "rewardTier": rewardDetails['data']['rewardTier'],
                                "reward_description": rewardDetails['data']['reward_description'],
                                "startDate": startDate
                                }

        # 4. Invoke special offer update on reward
        update_reward_specialOffer = invoke_http(reward_url, method='PUT', json=specialOffer_details)

        # 5. Receive reply from HTTP PUT, Publish message to AMQP
        code = update_reward_specialOffer["code"]
        if code in range(200, 300):
            # 6. This will carry the required information to be used when sending ad
            specialOffer_content = {
                "rid": rid,
                "endDate": endDate,
                "startDate": startDate,
                "promo_points": promo_points,
                "points": rewardDetails['data']['points'],
                "rewardName": rewardDetails['data']['rewardName'],
                "rewardTier": rewardDetails['data']['rewardTier'],
            }

            message = json.dumps(specialOffer_content)
            print('-----Publishing the (specialOffer) info message with routing_key=specialOffer-----')
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="specialOffer", body=message)
            print("Special Offer Content to RabbitMQ Exchange.")
            
        return jsonify(
            {
                "code": 201,
                "data": "Special Offer has been created for this item"
            }
        ), 201

    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "rid": rid,
                },
                "message": "An error occurred creating the special offer of the reward"
            }
        ), 500
    


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5900, debug=True)
