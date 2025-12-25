-- Create schema for confessions app
CREATE SCHEMA IF NOT EXISTS confessions;

-- Set search path
SET search_path TO confessions, public;

-- Create confessions table
CREATE TABLE IF NOT EXISTS confessions (
    id SERIAL PRIMARY KEY,
    confession TEXT NOT NULL,
    location VARCHAR(200),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster queries
CREATE INDEX idx_confessions_created_at ON confessions(created_at DESC);
CREATE INDEX idx_confessions_location ON confessions(location);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_confessions_updated_at BEFORE UPDATE
    ON confessions FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
