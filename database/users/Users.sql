CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
  user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  username VARCHAR(255) NOT NULL,
  e_password VARCHAR(255) NOT NULL,
  salt VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_info (
  user_id UUID PRIMARY KEY REFERENCES users(user_id),
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  age INT,
  address VARCHAR(255)
);
