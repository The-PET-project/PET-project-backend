USE petproject;

INSERT INTO user (username, email, password, firstname, lastname)
    VALUES ('admin', 'admin@pet-project.com', 'secure-admin-password', 'Admin', 'User');

INSERT INTO address (user_id, address, zip_code, city, county, country)
    VALUES (1, 'Main street 6', 2468, 'London', 'Greater London', 'England');
