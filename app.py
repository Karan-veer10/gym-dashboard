import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc

# Load data
df = pd.read_csv('gym_data.csv')
df['CheckInDate'] = pd.to_datetime(df['CheckInDate'])

# Charts
# 1. Line Chart - Check-ins per day
checkin_data = df.groupby('CheckInDate').size().reset_index(name='CheckIns')
line_fig = px.line(checkin_data, x='CheckInDate', y='CheckIns', title='Daily Member Check-ins')

# 2. Bar Chart - Popular Gym Areas
area_counts = df['AreaUsed'].value_counts().reset_index()
area_counts.columns = ['Area', 'Count']  # Rename columns for clarity
area_fig = px.bar(area_counts, x='Area', y='Count', title='Popular Gym Areas',
                  labels={'Area': 'Area Used', 'Count': 'Visits'})


# 3. Pie Chart - Membership Type Distribution
pie_fig = px.pie(df, names='MembershipType', title='Membership Type Distribution')

# 4. Inactive Members (no check-in in last 7 days)
recent_date = df['CheckInDate'].max()
active_members = df[df['CheckInDate'] >= recent_date - pd.Timedelta(days=7)]['MemberID'].unique()
inactive_members = df[~df['MemberID'].isin(active_members)][['MemberID', 'Name']].drop_duplicates()

# App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("🏋️‍♂️ Gym Membership Activity Dashboard", className="text-center my-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=line_fig), md=6),
        dbc.Col(dcc.Graph(figure=area_fig), md=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=pie_fig), md=6),
        dbc.Col([
            html.H5("Inactive Members (Past 7 Days)", className="mt-4"),
            html.Ul([html.Li(f"{row['MemberID']} - {row['Name']}") for _, row in inactive_members.iterrows()])
        ], md=6)
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
