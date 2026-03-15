import joblib
import numpy as np
import pandas as pd
import os

# ── Paths ──────────────────────────────────────────────────────────────────────
ML_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Load all models & encoders once at startup ─────────────────────────────────
score_model    = joblib.load(os.path.join(ML_DIR, "score_model.pkl"))
wickets_model  = joblib.load(os.path.join(ML_DIR, "wickets_model.pkl"))
poly_score     = joblib.load(os.path.join(ML_DIR, "poly_score.pkl"))
poly_wickets   = joblib.load(os.path.join(ML_DIR, "poly_wickets.pkl"))
enc_pitch_sc   = joblib.load(os.path.join(ML_DIR, "enc_pitch_score.pkl"))
enc_teams_sc   = joblib.load(os.path.join(ML_DIR, "enc_teams_score.pkl"))
enc_pitch_wk   = joblib.load(os.path.join(ML_DIR, "enc_pitch_wickets.pkl"))
enc_teams_wk   = joblib.load(os.path.join(ML_DIR, "enc_teams_wickets.pkl"))
meta_data      = joblib.load(os.path.join(ML_DIR, "meta.pkl"))


def _encode_score(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])
    df['pitch_condition'] = enc_pitch_sc.transform(df[['pitch_condition']])
    ohe = enc_teams_sc.transform(df[['batting_team', 'bowling_team', 'venue']])
    ohe_df = pd.DataFrame(ohe, columns=enc_teams_sc.get_feature_names_out(['batting_team','bowling_team','venue']))
    df = df.drop(['batting_team','bowling_team','venue'], axis=1)
    return pd.concat([df.reset_index(drop=True), ohe_df.reset_index(drop=True)], axis=1)


def _encode_wickets(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])
    df['pitch_condition'] = enc_pitch_wk.transform(df[['pitch_condition']])
    ohe = enc_teams_wk.transform(df[['batting_team', 'bowling_team', 'venue']])
    ohe_df = pd.DataFrame(ohe, columns=enc_teams_wk.get_feature_names_out(['batting_team','bowling_team','venue']))
    df = df.drop(['batting_team','bowling_team','venue'], axis=1)
    return pd.concat([df.reset_index(drop=True), ohe_df.reset_index(drop=True)], axis=1)


def predict_score_and_wickets(batting_team, bowling_team, venue, pitch_condition,
                               current_score, overs_completed, wickets_out,
                               runs_last_5_overs, overs_remaining, run_rate):
    # Step 1: Predict Final Score
    score_features = {
        'batting_team': batting_team, 'bowling_team': bowling_team,
        'venue': venue, 'pitch_condition': pitch_condition,
        'current_score': float(current_score), 'overs_completed': float(overs_completed),
        'wickets_out': float(wickets_out), 'runs_last_5_overs': float(runs_last_5_overs),
        'overs_remaining': float(overs_remaining), 'run_rate': float(run_rate),
    }
    score_df = _encode_score(score_features)
    predicted_score = round(float(score_model.predict(poly_score.transform(score_df))[0]))

    # Step 2: Predict Wickets Remaining
    wickets_features = {
        'batting_team': batting_team, 'bowling_team': bowling_team,
        'venue': venue, 'pitch_condition': pitch_condition,
        'current_score': float(current_score), 'overs_completed': float(overs_completed),
        'overs_remaining': float(overs_remaining), 'final_score': float(predicted_score),
        'run_rate': float(run_rate),
    }
    wickets_df = _encode_wickets(wickets_features)
    predicted_wk = max(0, min(10, round(float(wickets_model.predict(poly_wickets.transform(wickets_df))[0]))))

    return {
        "predicted_score":   predicted_score,
        "wickets_remaining": predicted_wk,
        "wickets_lost":      10 - predicted_wk,
    }


def get_meta():
    return meta_data
