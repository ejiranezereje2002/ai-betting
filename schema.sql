CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    league_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    league_name VARCHAR(100) NOT NULL,
    season VARCHAR(20) NOT NULL,
    home_team_id INT REFERENCES teams(team_id),
    away_team_id INT REFERENCES teams(team_id),
    match_date TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled',
    home_goals INT DEFAULT 0,
    away_goals INT DEFAULT 0,
    home_xg NUMERIC(4,2) DEFAULT 0.00,
    away_xg NUMERIC(4,2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE predictions (
    prediction_id SERIAL PRIMARY KEY,
    match_id INT REFERENCES matches(match_id),
    market_type VARCHAR(50) NOT NULL,
    selection VARCHAR(50) NOT NULL,
    model_probability NUMERIC(5,4) NOT NULL,
    market_odds NUMERIC(5,2) NOT NULL,
    expected_value NUMERIC(5,4) NOT NULL,
    is_high_confidence BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE prediction_feedback (
    feedback_id SERIAL PRIMARY KEY,
    prediction_id INT REFERENCES predictions(prediction_id),
    user_id VARCHAR(100),
    rating VARCHAR(20) NOT NULL,
    user_notes TEXT,
    match_result_status VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_matches_date ON matches(match_date);
CREATE INDEX idx_predictions_confidence ON predictions(is_high_confidence);
