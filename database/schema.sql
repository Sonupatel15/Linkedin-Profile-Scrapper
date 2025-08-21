CREATE TABLE IF NOT EXISTS profiles (
    profile_id SERIAL PRIMARY KEY,
    linkedin_url TEXT UNIQUE NOT NULL,
    name TEXT,
    first_name TEXT,
    last_name TEXT,
    location TEXT,
    headline TEXT,
    company TEXT,
    past_company1 TEXT,
    past_company2 TEXT,
    school1 TEXT,
    school2 TEXT,
    skills JSONB,
    experiences JSONB,
    certifications JSONB,
    last_updated TIMESTAMP NOT NULL DEFAULT NOW()
);
