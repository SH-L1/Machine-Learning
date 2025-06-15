USE ml_dashboard_db;

CREATE TABLE models (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    algorithm VARCHAR(255),
    training_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    accuracy DECIMAL(5, 4),
    model_path VARCHAR(500),
    description TEXT
);

CREATE TABLE processed_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_name VARCHAR(255) NOT NULL,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    num_rows INT,
    num_cols INT,
    data_path VARCHAR(500),
    description TEXT
);