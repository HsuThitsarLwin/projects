from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import datetime, pytz



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Define Reward Object
class Reward(db.Model):
    __tablename__ = 'rewards'

    # a function which counts upwards
    i = 0

    def mydefault():
        global i
        i += 1
        return i

    rid = db.Column(db.Integer, primary_key=True, default=mydefault)
    rewardName = db.Column(db.String(256), nullable=False)
    reward_description = db.Column(db.String(256))
    rewardTier = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(256), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String(256), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    is_specialOffer = db.Column(db.String(1), nullable=False)
    startDate = db.Column(db.DateTime, nullable=True)
    endDate = db.Column(db.DateTime, nullable=True)
    promo_points = db.Column(db.Integer, nullable=True)

    def __init__(self, rid, rewardName, reward_description, rewardTier, category, points, quantity,
                 region, latitude, longitude, is_specialOffer, startDate, endDate, promo_points):
        self.rid = rid
        self.rewardName = rewardName
        self.reward_description = reward_description
        self.rewardTier = rewardTier
        self.category = category
        self.points = points
        self.quantity = quantity
        self.region = region
        self.latitude = latitude
        self.longitude = longitude
        self.is_specialOffer = is_specialOffer
        self.startDate = startDate
        self.endDate = endDate
        self.promo_points = promo_points

    def json(self):
        return {"rid": self.rid, "rewardName": self.rewardName, "reward_description": self.reward_description,
                "rewardTier": self.rewardTier,
                "category": self.category, "points": self.points, "quantity": self.quantity,
                "region": self.region, "latitude": self.latitude, "longitude": self.longitude,
                "is_specialOffer": self.is_specialOffer, "startDate": self.startDate, "endDate": self.endDate,
                "promo_points": self.promo_points}

# Retrieving all rewards data
@app.route("/reward")
def get_all():
    rewardlist = Reward.query.all()
    if len(rewardlist):
        for reward in rewardlist:
            # Checks whether endDate exceeds current time
            gmt8 = pytz.timezone('Asia/Singapore') # Set timezone to GMT+8
            current_time = datetime.datetime.now(gmt8) # Get current time in GMT+8
            if reward.endDate is not None:
                reward_end_date = gmt8.localize(reward.endDate)
                if reward_end_date < current_time:
                    reward.startDate = None
                    reward.endDate = None
                    reward.promo_points = None
                    reward.is_specialOffer = 0
                    db.session.commit()

        return jsonify(
            {
                "code": 200,
                "data": {
                    "rewards": [reward.json() for reward in rewardlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no rewards."
        }
    ), 404

# Retrieving specific reward data
@app.route("/reward/<string:rid>")
def find_by_rid(rid):
    reward = Reward.query.filter_by(rid=rid).first()
    if rid:
        return jsonify(
            {
                "code": 200,
                "data": reward.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Reward not found."
        }
    ), 404

# Update specific reward quantity
@app.route("/reward/<string:rid>", methods=['PUT'])
def edit_points(rid):

    data = request.get_json()
    rewardpoints = Reward(rid, **data)

    try:
        reward = Reward.query.filter_by(rid=rid).first()
        # reward = rewardpoints
        reward.is_specialOffer = rewardpoints.is_specialOffer
        reward.startDate = rewardpoints.startDate
        reward.endDate = rewardpoints.endDate
        reward.promo_points = rewardpoints.promo_points
        reward.quantity = rewardpoints.quantity
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "rid": rid
                },
                "message": "An error occurred updating the reward points"
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": reward.json()
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
