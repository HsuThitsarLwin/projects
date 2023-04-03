from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
from datetime import datetime
import amqp_setup, pika, json, time, requests

app = Flask(__name__)
CORS(app)

# 0. Retrieve the cid and rid from UI
@app.route('/redeemRewards', methods=['POST'])
def redeem_rewards():
    data = request.get_json()
    # Retrieve the rid and cid parameters from the POST request data
    rid = data['params']['rid']
    cid = data['params']['cid']

    try:
        # 1a. Get reward details from reward catalogue by id
        # 1b. Get points needed for reward and store in variable
        reward_url = "http://reward:5000/reward/" + str(rid)
        customer_url = "http://customer:5200/customer/" + str(cid)

        rewardDetails = invoke_http(reward_url, method='GET')
        customerDetails = invoke_http(customer_url, method='GET')

        print(rewardDetails, customerDetails)

        # 2. Get reward quantity by rid
        quantity = rewardDetails['data']['quantity']

        # 3. Get customer balancePoints by cid
        customerPoints = int(customerDetails['data']['balancePoints'])
        print('Customer Points: ' + str(customerPoints))

        # 4. Checks if there is promo, and saves the reward's points to be deducted into deductPoints
        if (rewardDetails['data']['is_specialOffer'] == '0'):
            deductPoints = rewardDetails['data']['points']
            print('Points:' + str(deductPoints))
        else:
            deductPoints = rewardDetails['data']['promo_points']
            print('Promo Points:' + str(deductPoints))

        # 5. Checks if customer has enough points to redeem item, if not, print error message and do nothing (might want to add a popup in webapp)
        if (customerPoints - deductPoints >= 0):
            newPoints = customerPoints - deductPoints
            print('New Points:', newPoints)
            customer_details = {"name": customerDetails['data']['name'],
                                "email_addr":  customerDetails['data']['email_addr'],
                                "dateOfBirth":  customerDetails['data']['dateOfBirth'],
                                "balancePoints": newPoints,
                                "tier": customerDetails['data']['tier'],
                                }

            # 6. Invoke customer balance update
            invoke_http(customer_url, method='PUT', json=customer_details)

            # 7. Reduce Quantity by 1
            newQuantity = quantity - 1
            reward_details = {"category": rewardDetails['data']['category'],
                              "endDate": rewardDetails['data']['endDate'],
                              "is_specialOffer": rewardDetails['data']['is_specialOffer'],
                              "latitude": rewardDetails['data']['latitude'],
                              "longitude": rewardDetails['data']['longitude'],
                              "points": rewardDetails['data']['points'],
                              "promo_points": rewardDetails['data']['promo_points'],
                              "quantity": newQuantity,
                              "region": rewardDetails['data']['region'],
                              "rewardName": rewardDetails['data']['rewardName'],
                              "rewardTier": rewardDetails['data']['rewardTier'],
                              "reward_description": rewardDetails['data']['reward_description'],
                              "startDate": rewardDetails['data']['startDate']}

            # 8. Invoke reward quantity update
            invoke_http(reward_url, method='PUT', json=reward_details)

            # 9. Aggregate data for Email MS
            customer_email = customerDetails['data']['email_addr']
            customer_name = customerDetails['data']['name']
            customer_points = customerDetails['data']['balancePoints']
            reward_name = rewardDetails['data']['rewardName']
            reward_cost = rewardDetails['data']['points']

            email_content = {
                "customer_email": customer_email,
                "customer_name": customer_name,
                "customer_points": customer_points,
                "reward_name": reward_name,
                "reward_cost": reward_cost
            }

            # 10. Publish to Email MS
            message = json.dumps(email_content)
            print('\n-----Publishing the (email info) message with routing_key=email-----')
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="email", body=message)
            print("Email content published to RabbitMQ Exchange.")

            # 11. Aggregate data for RewardLog MS
            customer_id = customerDetails['data']['cid']
            reward_id = rewardDetails['data']['rid']
            redemption_time = time.strftime("%H:%M:%S", time.localtime())  # get time
            redeem_date = datetime.today().strftime('%Y-%m-%d')  # get date

            log_content = {
                "customer_id": customer_id,
                "reward_id": reward_id,
                "redemption_time": redemption_time,
                "redeem_date": redeem_date,
            }

            # 12. Publish to redemption log ms
            log_message = json.dumps(log_content)
            print('\n-----Publishing the logging content with routing_key=log-----')
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="log", body=log_message, properties=pika.BasicProperties(delivery_mode=2))
            print("Log published to RabbitMQ Exchange.\n")

            return jsonify(
                {
                    "code": 201,
                    "data": "Successful Redemption"
                }
            ), 201
        
        else:
            # 13. If there is not enough points
            return jsonify(
                {
                    "code": 402,
                    "data": "You don't have enough points to claim this!! thank you for wasting computation resources ://"
                }
            ), 201

    except:
        # Error Code
        return jsonify(
            {
                "code": 500,
                "data": {
                    "rid": rid,
                    "cid": cid
                },
                "message": "An error occurred redeeming the reward."
            }
        ), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5800, debug=True)
