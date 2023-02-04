CREATE SCHEMA petproject;

CREATE  TABLE petproject.address (
	address_id           BIGINT UNSIGNED NOT NULL   AUTO_INCREMENT  PRIMARY KEY,
	user_id              BIGINT UNSIGNED NOT NULL,
	address              VARCHAR(100)  NOT NULL,
	zip_code             INT UNSIGNED NOT NULL,
	city                 VARCHAR(100)  NOT NULL,
	county               VARCHAR(100)  NOT NULL,
	country              VARCHAR(100)  NOT NULL,
	CONSTRAINT user_id UNIQUE ( user_id )
 ) engine=InnoDB;

CREATE  TABLE petproject.user (
	user_id              BIGINT UNSIGNED NOT NULL   AUTO_INCREMENT  PRIMARY KEY,
	username             VARCHAR(100)  NOT NULL,
	email                VARCHAR(100)  NOT NULL,
	password             VARCHAR(100)  NOT NULL,
	firstname            VARCHAR(100)  NOT NULL,
	lastname             VARCHAR(100)  NOT NULL,
	middlename           VARCHAR(100),
	phone                VARCHAR(30),
	mobile               VARCHAR(30)
 ) engine=InnoDB;

CREATE  TABLE petproject.pet_carer (
	pet_carer_id         BIGINT UNSIGNED NOT NULL   AUTO_INCREMENT  PRIMARY KEY,
	user_id              BIGINT UNSIGNED NOT NULL,
	rating               DOUBLE UNSIGNED,
	CONSTRAINT unique_index UNIQUE ( user_id ),
	CONSTRAINT fk_pet_carer_user FOREIGN KEY ( user_id ) REFERENCES petproject.`user`( user_id ) ON DELETE CASCADE ON UPDATE CASCADE
 ) engine=InnoDB;

CREATE  TABLE petproject.pet_owner (
	owner_id             BIGINT UNSIGNED NOT NULL   AUTO_INCREMENT  PRIMARY KEY,
	user_id              BIGINT UNSIGNED NOT NULL,
	rating               DOUBLE UNSIGNED,
	CONSTRAINT user_id UNIQUE ( user_id ),
	CONSTRAINT user_id FOREIGN KEY ( user_id ) REFERENCES petproject.`user`( user_id ) ON DELETE CASCADE ON UPDATE CASCADE
 ) engine=InnoDB;

CREATE  TABLE petproject.service (
	service_id           BIGINT UNSIGNED NOT NULL   AUTO_INCREMENT  PRIMARY KEY,
	owner_id             BIGINT UNSIGNED NOT NULL,
	`type`               ENUM('PET-WALKING','PET-FEED','PET-TAXI','OVERNIGHT-CARE','PET-HOTEL')  NOT NULL,
	days                 VARCHAR(10)  NOT NULL,
	start_time           TIME  NOT NULL,
	time_interval        TINYINT UNSIGNED NOT NULL,
	start_date           DATE  NOT NULL,
	end_date             DATE,
	description          VARCHAR(300),
	CONSTRAINT fk_service_pet_owner FOREIGN KEY ( owner_id ) REFERENCES petproject.pet_owner( owner_id ) ON DELETE CASCADE ON UPDATE CASCADE
 ) engine=InnoDB;

CREATE INDEX fk_service_pet_owner ON petproject.service ( owner_id );

CREATE  TABLE petproject.pet (
	pet_id               BIGINT UNSIGNED NOT NULL   AUTO_INCREMENT  PRIMARY KEY,
	owner_id             BIGINT UNSIGNED NOT NULL,
	name                 VARCHAR(100)  NOT NULL,
	full_name            VARCHAR(150),
	date_of_birth        DATE  NOT NULL,
	sex                  CHAR(1)  NOT NULL,
	category             VARCHAR(50)  NOT NULL,
	breed                VARCHAR(100)  NOT NULL,
	color                VARCHAR(25),
	rating               DOUBLE UNSIGNED,
	CONSTRAINT fk_pet_pet_owner FOREIGN KEY ( owner_id ) REFERENCES petproject.pet_owner( owner_id ) ON DELETE CASCADE ON UPDATE CASCADE
 ) engine=InnoDB;

CREATE INDEX fk_pet_pet_owner ON petproject.pet ( owner_id );

CREATE  TABLE petproject.pet_service (
	service_id           BIGINT UNSIGNED NOT NULL,
	pet_id               BIGINT UNSIGNED NOT NULL,
	CONSTRAINT fk_for_service FOREIGN KEY ( service_id ) REFERENCES petproject.service( service_id ) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fk_for_pet FOREIGN KEY ( pet_id ) REFERENCES petproject.pet( pet_id ) ON DELETE CASCADE ON UPDATE CASCADE
 ) engine=InnoDB;

CREATE INDEX fk_for_service ON petproject.pet_service ( service_id );

CREATE INDEX fk_for_pet ON petproject.pet_service ( pet_id );

CREATE  TABLE petproject.route (
	route_id             BIGINT UNSIGNED NOT NULL   AUTO_INCREMENT  PRIMARY KEY,
	service_id           BIGINT UNSIGNED NOT NULL,
	pet_carer_id         BIGINT UNSIGNED NOT NULL,
	appointment          DATETIME  NOT NULL,
	CONSTRAINT unique_index UNIQUE ( service_id, appointment ),
	CONSTRAINT fk_route_service FOREIGN KEY ( service_id ) REFERENCES petproject.service( service_id ) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fk_route_pet_carer FOREIGN KEY ( pet_carer_id ) REFERENCES petproject.pet_carer( pet_carer_id ) ON DELETE CASCADE ON UPDATE CASCADE
 ) engine=InnoDB;

CREATE INDEX fk_route_pet_carer ON petproject.route ( pet_carer_id );

ALTER TABLE petproject.`user` COMMENT 'User account that contains the registered people of the PET-project app.';

ALTER TABLE petproject.service COMMENT 'Registered service requests in the PET-project application.\n\nTypes:\n- PET-WALKING: Get your pet walked by a pet carer\n- PET-FEED: Get your pet fed by a pet carer when you are not at home\n- PET-TAXI: Get your pet transported by a competent specialist\n- OVERNIGHT-CARE: Get your pet left under supervision overnight\n- PET-HOTEL: Get your pet cared when you go for a vacation';

ALTER TABLE petproject.service MODIFY start_time TIME  NOT NULL   COMMENT '24h time format: "hh:mm" (e.g: "14:00")';

ALTER TABLE petproject.service MODIFY time_interval TINYINT UNSIGNED NOT NULL   COMMENT 'The length of the event given in minutes.';

ALTER TABLE petproject.pet MODIFY date_of_birth DATE  NOT NULL   COMMENT 'Date with the format: YYYY-MM-DD';

ALTER TABLE petproject.pet MODIFY sex CHAR(1)  NOT NULL   COMMENT '(M) for Male, (F) for Female';

ALTER TABLE petproject.pet MODIFY category VARCHAR(50)  NOT NULL   COMMENT 'Category of the animal like: Dog, Cat, Snake, Weasel';

ALTER TABLE petproject.route COMMENT 'Registered walking routes connected to walker & service entities';

ALTER TABLE petproject.route MODIFY appointment DATETIME  NOT NULL   COMMENT 'Datetime in ISO format: "YYYY-MM-DDThh:mm:ssZ:" (e.g: "2023-01-28T12:00:00Z")';
