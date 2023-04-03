import pandas as pd
from flask import Flask
import plotly.graph_objs as go
import plotly.express as px
from dash import dcc, html, dash
import requests
import numpy as np
from scipy.stats import gaussian_kde
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

dash_app = dash.Dash(__name__, server=app, url_base_pathname='/charts/')
dash_app.title = "Admin Dashboard"
dash_app.layout = html.Div ("")

@app.route('/charts', methods=['GET'])
def render_dashboard():

    url = "http://aggregatedata:4010/graphql_aggregation?t="

    response = requests.get(url)
    json_data = response.json()
    rewardslog = response.json()["rewardslog"]
    # customer_data = response.json()["customer"]
    rewards = response.json()["rewards"]

    df_rewardslog = pd.DataFrame(rewardslog)
    df_rewardslog['redemptionHour'] = pd.to_datetime(df_rewardslog['redemptionTime'], format='%H:%M:%S').dt.hour
    hourly_counts = df_rewardslog.groupby('redemptionHour').size().reset_index(name='count')
    all_hours = pd.DataFrame({'redemptionHour': range(24)})
    hourly_counts = all_hours.merge(hourly_counts, on='redemptionHour', how='left')
    hourly_counts['count'] = hourly_counts['count'].fillna(0)


    fig = px.bar(hourly_counts, x='redemptionHour', y='count', title='Redemption Count By Hour Chart',
                labels={'redemptionHour': 'Hour', 'count': 'Redemption Count'},)

    # Calculate KDE
    kde_x = np.linspace(hourly_counts['redemptionHour'].min(), hourly_counts['redemptionHour'].max(), 100)
    kde = gaussian_kde(df_rewardslog['redemptionHour'])
    kde_y = kde.evaluate(kde_x)

    # Add KDE plot to the bar chart
    fig.add_trace(go.Scatter(x=kde_x, y=kde_y * hourly_counts['count'].max() / kde_y.max(), mode='lines', name='KDE'))


    # Update the x-axis range to show all hours
    fig.update_xaxes(range=[0, 23], tickmode='linear', tick0=0, dtick=1)
        
    # Number_of_redemption_by_Reward_Tiers chart NUMBER 2
        
    df_rewards = pd.DataFrame(rewards)
    # Merge DataFrames
    merged_df = df_rewardslog.merge(df_rewards, on="rid")

    # Group by 'redeemDate' and 'rewardTier', and calculate the redemption count
    grouped_df = merged_df.groupby(['redeemDate', 'rewardTier']).size().reset_index(name='count')

    # Create the line chart
    fig2 = px.line(grouped_df, x="redeemDate", y="count", color="rewardTier",
                title="Redemption Rate Per Reward Tier Chart",
                labels={"redeemDate": "Date", "count": "Redemption Count", "rewardTier": "Reward Tier"})

    # Category By Age Chart NUMBER 3

    def age_group(date_of_birth):
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
        age = (datetime.now() - dob).days // 365
        if 20 <= age <= 30:
            return "20-30"
        elif 31 <= age <= 40:
            return "31-40"
        elif 41 <= age <= 50:
            return "41-50"
        else:
            return None

    customers = {customer["cid"]: age_group(customer["dateOfBirth"]) for customer in json_data["customer"]}
    rewards_by_category = {reward["rid"]: reward["category"] for reward in json_data["rewards"]}

    redemptions_by_age_group = {"20-30": {}, "31-40": {}, "41-50": {}}

    for redemption in json_data["rewardslog"]:
        cid = redemption["cid"]
        rid = redemption["rid"]
        age_group = customers.get(cid, None)
        category = rewards_by_category[rid]

        if age_group is not None:
            if category not in redemptions_by_age_group[age_group]:
                redemptions_by_age_group[age_group][category] = 0
            redemptions_by_age_group[age_group][category] += 1

    categories = set(rewards_by_category.values())

    rows = []
    for age_group, categories in redemptions_by_age_group.items():
        for category, count in categories.items():
            rows.append({"age_group": age_group, "category": category, "count": count})

    df_merged = pd.DataFrame(rows)

    # Create the histogram
    fig3 = px.histogram(df_merged, x='category', y='count', color='category',
                        histfunc='sum', nbins=3, title='Category by Age Groups Chart',
                        labels={'category': 'Category', 'count': 'Customer Count'},
                        facet_col="age_group", facet_col_spacing=0.1)

    # Update the layout
    fig3.update_layout(barmode='group')

    # Redemption for each category chart NUMBER 4
    category_count = {}
    for log in json_data["rewardslog"]:
        rid = log["rid"]
        category = None
        
        for reward in json_data["rewards"]:
            if reward["rid"] == rid:
                category = reward["category"]
                break
        
        if category:
            if category not in category_count:
                category_count[category] = 0
            category_count[category] += 1

    fig4 = go.Figure(go.Pie(labels=list(category_count.keys()), values=list(category_count.values())))
    fig4.update_layout(title="Redemption Count for Each Category")

    dash_app.layout = html.Div([
        dcc.Graph(id='graph1', figure=fig),
        dcc.Graph(id='graph2', figure=fig2),
        dcc.Graph(id='graph3', figure=fig3),
        dcc.Graph(id='graph4', figure=fig4)
    ])

    return dash_app.index()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4020, debug=True)
