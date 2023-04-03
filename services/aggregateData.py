import graphene
from flask import Flask, jsonify
from invokes import invoke_http
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Object Declaration
class Reward(graphene.ObjectType):
    rid = graphene.Int()
    rewardName = graphene.String()
    reward_description = graphene.String()
    rewardTier = graphene.String()
    category = graphene.String()
    points = graphene.Int()
    quantity = graphene.Int()
    region = graphene.String()
    latitude = graphene.String()
    longitude = graphene.String()
    is_specialOffer = graphene.Int()
    startDate = graphene.String()
    endDate = graphene.String()
    promo_points = graphene.Int()

class Customer(graphene.ObjectType):
    cid = graphene.Int()
    name = graphene.String()
    email_addr = graphene.String()
    dateOfBirth = graphene.String()
    balancePoints = graphene.Int()
    tier = graphene.String()

class RewardsLog(graphene.ObjectType):
    redemptionsLogID = graphene.Int()
    redeemDate = graphene.String()
    redemptionTime = graphene.String()
    cid = graphene.Int()
    rid = graphene.Int()

# http://127.0.0.1:4010/graphql_aggregation
@app.route('/graphql_aggregation', methods=['GET'])
def graphql():

    # Data retrieved from reward
    rewards_data = invoke_http('http://reward:5000/reward')['data']['rewards']
    customer_data = invoke_http('http://customer:5200/customer')['data']['customer']
    rewardslog_data = invoke_http('http://rewardslog:5400/rewardslog')['data']['rewards']

    # Query Class
    class Query(graphene.ObjectType):
        rewards = graphene.List(Reward)
        rewardslog = graphene.List(RewardsLog)
        customer = graphene.List(Customer)

        def resolve_rewards(self, info):
            return resolve_rewards(None, info)
        
        def resolve_rewardslog(self, info):
            return resolve_rewardslog(None, info)
        
        def resolve_customer(self, info):
            return resolve_customer(None, info)
        
    # Resolver function
    def resolve_rewards(parent, info):
        return [Reward(**data) for data in rewards_data]

    def resolve_rewardslog(parent, info):
        return [RewardsLog(**data) for data in rewardslog_data]

    def resolve_customer(parent, info):
        return [Customer(**data) for data in customer_data]

    # Create scehema
    schema = graphene.Schema(query=Query)

    # 1 Query to retrieve all necessary data
    query = """
        query {
    rewards{
        rid
        category
        isSpecialoffer
        rewardTier
        region
    }
    customer{
        cid
        dateOfBirth
    }
    rewardslog{
        redemptionsLogID
        rid
        redeemDate
        redemptionTime
        cid
    }
    }
    """

    result = schema.execute(query)
    return jsonify(result.data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4010, debug=True)