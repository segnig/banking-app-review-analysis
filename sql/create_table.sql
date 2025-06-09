CREATE TABLE Reviews (
    review_id VARCHAR(100) PRIMARY KEY,
    app_id VARCHAR(100) NOT NULL,
    app_name VARCHAR(100) NOT NULL,
    user_name VARCHAR(50),
    review TEXT,
    rating NUMERIC(2,1) CHECK (rating >= 1 AND rating <= 5),
    thumbs_up_count INTEGER DEFAULT 0,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE banks (
    bank_id TEXT PRIMARY KEY,
    bank_name TEXT NOT NULL,
    website_url TEXT,
    app_store_id TEXT,
    date_added TIMESTAMPTZ DEFAULT NOW()
);
