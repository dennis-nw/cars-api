CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
CREATE TABLE car_makes (
	id VARCHAR(100) NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE INDEX ix_name ON car_makes (name);
CREATE TABLE IF NOT EXISTS "car_models" (
	id VARCHAR(100) NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	make_id VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_car_models_make_id FOREIGN KEY(make_id) REFERENCES car_makes (id), 
	CONSTRAINT uq_car_models_name_make_id UNIQUE (name, make_id), 
	UNIQUE (name)
);
CREATE TABLE users (
	id INTEGER NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	password VARCHAR(150) NOT NULL, 
	created_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP), 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
