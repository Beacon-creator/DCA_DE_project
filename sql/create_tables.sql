CREATE TABLE IF NOT EXISTS netflix_titles_table  (
    show_id         VARCHAR PRIMARY KEY,
    type            VARCHAR(20) NOT NULL,       
    title           TEXT NOT NULL,
    director        TEXT,
    cast            TEXT,
    country         VARCHAR(255),
    date_added      DATE,                        
    release_year    INT NOT NULL,
    rating          VARCHAR(20),
    listed_in       TEXT,                      
    description     TEXT,
    year_added      INT,
    month_added     INT,
    day_added       INT,
    duration_value  INT,
    duration_unit   VARCHAR(20)
);