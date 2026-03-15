from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder, OrdinalEncoder

app = Flask(__name__)


df = pd.read_csv("ipl data set.csv")


X = df[['batting_team','bowling_team','venue','pitch_type',
        'current_score','overs_completed','wickets_out',
        'runs_last_5_overs','overs_remaining','run_rate']]

y = df['final_score']


pitch_encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
X['pitch_type'] = pitch_encoder.fit_transform(X[['pitch_type']])

team_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

team_data = team_encoder.fit_transform(X[['batting_team','bowling_team','venue']])

team_columns = team_encoder.get_feature_names_out(
    ['batting_team','bowling_team','venue']
)

team_df = pd.DataFrame(team_data, columns=team_columns)

X = X.drop(['batting_team','bowling_team','venue'], axis=1)
X = pd.concat([X.reset_index(drop=True), team_df], axis=1)


poly = PolynomialFeatures(degree=2)

X_poly = poly.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)


@app.route("/")
def home():
    return render_template("IPL.html")


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    score = float(data["current_score"])
    overs = float(data["overs_completed"])

    if overs == 0:
        run_rate = 0
    else:
        run_rate = score / overs

    overs_remaining = 20 - overs

    input_df = pd.DataFrame([{
        'batting_team': data['batting_team'],
        'bowling_team': data['bowling_team'],
        'venue': data['venue'],
        'pitch_type': data['pitch_type'],
        'current_score': score,
        'overs_completed': overs,
        'wickets_out': int(data['wickets_out']),
        'runs_last_5_overs': int(data['runs_last_5_overs']),
        'overs_remaining': overs_remaining,
        'run_rate': run_rate
    }])

  
    input_df['pitch_type'] = pitch_encoder.transform(input_df[['pitch_type']])

    
    team_encoded = team_encoder.transform(
        input_df[['batting_team','bowling_team','venue']]
    )

    team_encoded_df = pd.DataFrame(team_encoded, columns=team_columns)

    input_df = input_df.drop(['batting_team','bowling_team','venue'], axis=1)

    input_df = pd.concat(
        [input_df.reset_index(drop=True), team_encoded_df],
        axis=1
    )

    input_poly = poly.transform(input_df)

    prediction = model.predict(input_poly)

    predicted_score = int(prediction[0])

    return jsonify({
        "predicted_score": predicted_score
    })


if __name__ == "__main__":
    app.run(debug=True)