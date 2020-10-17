-- Create Database
CREATE DATABASE pricewatch;

-- connect to Database
\c pricewatch

-- activate uuid extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- create table
CREATE TABLE product (
   id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
   producttypeid uuid REFERENCES producttype(id),
   productId varchar(128),
   productIdAsString varchar(128),
   name varchar(256),
   fullname varchar(256),
   simpleName varchar(256)
);

-- insert urls
INSERT INTO url (value) VALUES ('https://www.digitec.ch/de/s1/product/corsair-rm650-2019-650w-pc-netzteil-11245247');
INSERT INTO url (value) VALUES ('https://www.digitec.ch/de/s1/product/gigabyte-b450-gaming-x-am4-amd-b450-atx-mainboard-12285290');
INSERT INTO url (value) VALUES ('https://www.digitec.ch/de/s1/product/corsair-vengeance-lpx-2x-8gb-ddr4-3200-dimm-288-ram-5711579');
INSERT INTO url (value) VALUES ('https://www.digitec.ch/de/s1/product/samsung-860-evo-basic-1000gb-25-ssd-7197973');
INSERT INTO url (value) VALUES ('https://www.digitec.ch/de/s1/product/intertech-cxc2-blue-ohne-psu-frontblende-aus-tempered-glass-1x-usb-30-2x-usb-20-3-blaue-luefter-lieg-10145427');
INSERT INTO url (value) VALUES ('https://www.digitec.ch/de/s1/product/amd-ryzen-5-1600-am4-320ghz-6-core-prozessor-12503590');

-- create price value table
CREATE TABLE price (
   id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
   productid uuid REFERENCES product(id),
   price decimal NOT NULL,
   date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- create productType table
CREATE TABLE producttype (
   id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
   typeid INTEGER,
   name varchar(256)
);

GRANT UPDATE, INSERT, SELECT, DELETE ON ALL TABLES IN SCHEMA public TO pricewatch;


-- UPDATE 20200524
ALTER TABLE price ADD COLUMN insteadOfPrice decimal;

-- update 20201017
ALTER TABLE product ADD COLUMN date DATE NOT NULL DEFAULT CURRENT_DATE;

