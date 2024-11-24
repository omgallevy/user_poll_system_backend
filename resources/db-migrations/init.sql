DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT(11) NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(300) NOT NULL,
    last_name VARCHAR(300) NOT NULL,
    age INT(3) NOT NULL,
    email VARCHAR(300) NOT NULL,
    address VARCHAR(300) NOT NULL,
    joining_date DATE DEFAULT NULL,
    is_registered BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id)
);
