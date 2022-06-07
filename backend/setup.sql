DROP DATABASE IF EXISTS trivia;
DROP DATABASE IF EXISTS trivia_test;
DROP USER IF EXISTS ismail;
CREATE DATABASE trivia;
CREATE DATABASE trivia_test;
CREATE USER ismail WITH ENCRYPTED PASSWORD 'Smart 5441';
GRANT ALL PRIVILEGES ON DATABASE trivia TO ismail;
GRANT ALL PRIVILEGES ON DATABASE trivia_test TO ismail;
ALTER USER ismail CREATEDB;
ALTER USER ismail WITH SUPERUSER;