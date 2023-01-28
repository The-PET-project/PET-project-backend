USE petproject;

INSERT INTO user (username, email, password, firstname, lastname)
    VALUES ('admin', 'admin@pet-project.com', 'secure-admin-password', 'Admin', 'User');

INSERT INTO address (user_id, address, zip_code, city, county, country)
    VALUES (1, 'Horsensvej 68B', 7100, 'Vejle', 'Syddanmark', 'Denmark');
