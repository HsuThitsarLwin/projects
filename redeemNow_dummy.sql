# CREATION OF CUSTOMER DB

create database redeemNow_customer;
use redeemNow_customer;
create table customer (
	cid int not null auto_increment,
	name varchar(256) not null,
	email_addr varchar(256) not null,
	dateOfBirth date not null,
	balancePoints int not null,
	tier varchar(256) not null,
	primary key (cid)
);
INSERT INTO customer (cid, name, email_addr, dateOfBirth, balancePoints, tier) VALUES
(1001, 'John Smith', 'john.smith@example.com', '1987-05-02', 1500, 'Gold');
INSERT INTO customer (name, email_addr, dateOfBirth, balancePoints, tier) VALUES
('Jane Doe', 'jane.doe@example.com', '1992-11-12', 3000, 'Platinum'),
('Mike Johnson', 'mike.johnson@example.com', '1985-08-21', 500, 'Silver'),
('Sara Wilson', 'sara.wilson@example.com', '1998-02-18', 2000, 'Gold'),
('Tom Lee', 'tom.lee@example.com', '1995-07-10', 3500, 'Platinum'),
('Emily Chen', 'emily.chen@example.com', '1989-12-03', 1000, 'Silver'),
('David Kim', 'david.kim@example.com', '1976-09-24', 4000, 'Platinum'),
('Linda Brown', 'linda.brown@example.com', '1991-06-07', 700, 'Silver'),
('Michael Davis', 'michael.davis@example.com', '1983-03-15', 2500, 'Gold'),
('Sarah Jones', 'sarah.jones@example.com', '2000-01-01', 1200, 'Silver');
INSERT INTO customer (cid, name, email_addr, dateOfBirth, balancePoints, tier) VALUES
(9999, 'Administrator', 'admin@example.com', '2000-05-02', 999999, 'Platinum');


# CREATION OF REWARDS DB
create database redeemNow_Rewards;
use redeemNow_Rewards;
create table rewards (
    rid int not null auto_increment,
    rewardName varchar(256) not null,
	reward_description varchar(256),
    rewardTier varchar(256) not null,
    category varchar(256) not null,
    points int not null,
	quantity int not null,
	region varchar(256) not null,
	latitude float not null,
    longitude float not null,
    is_specialOffer char(1) not null,
    startDate datetime null,
    endDate datetime null,
    promo_points int null,
    primary key (rid)
);


insert into rewards 
(rid, rewardName, reward_description, rewardTier, category, points, quantity, region, latitude, longitude, is_specialOffer)
values
(1001, 'Smartphone Gimbal Stabilizer', 'Handheld smartphone stabilizer', 'Silver', 'Technology', 5000, 50, 'North', 1.4414, 103.8002, 0);

INSERT INTO rewards (rewardName, reward_description, rewardTier, category, points, quantity, region, latitude, longitude, is_specialOffer)
VALUES 
('iPhone 12 Pro', 'The latest and greatest iPhone with 128GB storage', 'Gold', 'Technology', 25000, 50, 'Central', 1.290270, 103.851959, '0'),
('Samsung Galaxy S21', 'The newest Samsung phone with 256GB storage', 'Silver', 'Technology', 20000, 40, 'North', 1.417978, 103.821022, '0'),
('Bose QuietComfort 35', 'Noise-cancelling headphones', 'Silver', 'Technology', 15000, 30, 'West', 1.344981, 103.683227, '0'),
('Fitbit Versa 2', 'Fitness tracker and smartwatch', 'Bronze', 'Technology', 8000, 20, 'East', 1.355226, 103.936516, '0'),
('PlayStation 5', 'The latest gaming console from Sony', 'Gold', 'Entertainment', 30000, 50, 'Central', 1.306681, 103.834219, '0'),
('Nintendo Switch', 'Hybrid gaming console', 'Silver', 'Entertainment', 18000, 30, 'North', 1.434038, 103.828671, '0'),
('Xbox Series X', 'The latest gaming console from Microsoft', 'Gold', 'Entertainment', 25000, 40, 'East', 1.326849, 103.891860, '0'),
('Sony 65" 4K Smart TV', 'High-end 4K television with smart features', 'Gold', 'Entertainment', 28000, 30, 'West', 1.290609, 103.794720, '0'),
('JBL Flip 5', 'Portable Bluetooth speaker', 'Bronze', 'Technology', 5000, 20, 'Central', 1.281870, 103.850054, '0'),
('Samsung Galaxy Tab S7+', 'Tablet with S Pen included', 'Silver', 'Technology', 16000, 30, 'North', 1.395178, 103.911261, '0'),
('Philips Airfryer XXL', 'Airfryer with extra large capacity', 'Bronze', 'Food', 10000, 20, 'West', 1.320919, 103.700542, '0'),
('KitchenAid Stand Mixer', 'Iconic stand mixer for baking and cooking', 'Gold', 'Food', 25000, 40, 'Central', 1.287045, 103.842268, '0'),
('Nespresso Vertuo Coffee Machine', 'Coffee machine with versatile brewing options', 'Silver', 'Food', 12000, 30, 'East', 1.352958, 103.938117, '0'),
('Dining voucher for Fat Cow', 'Fine dining Japanese restaurant', 'Gold', 'Food', 18000, 20, 'Central', 1.290245, 103.851943, '0'),
('Movie tickets for Golden Village', 'Movie tickets for two with popcorn and drinks', 'Silver', 'Entertainment', 10000, 25, 'North', 1.432140, 103.774478, '0'),

('$50 GrabFood Voucher', 'Food delivery voucher', 'Bronze', 'Food', 2000, 100, 'West', 1.3459, 103.7024, 0),
('$50 McDonalds Voucher', 'Fast food voucher', 'Bronze', 'Food', 2000, 100, 'West', 1.3459, 103.7024, 0),
('2 Golden Village Movie Tickets', 'Movie tickets', 'Bronze', 'Entertainment', 2000, 100, 'Central', 1.3048, 103.8318, 0),
('1 Month Free Netflix Subscription', 'Streaming service subscription', 'Silver', 'Entertainment', 5000, 50, 'North', 1.4414, 103.8002, 0),
('1 Month Free Disney+ Subscription', 'Streaming service subscription', 'Silver', 'Entertainment', 5000, 50, 'North', 1.4414, 103.8002, 0);



# CREATION OF REWARDS_LOG DB
CREATE DATABASE redeemNow_rewardsLog;
USE redeemNow_rewardsLog;
CREATE TABLE rewardsLog (
    redemptionsLogID INT NOT NULL AUTO_INCREMENT,
    redeemDate DATE NOT NULL,
    redemptionTime TIME NOT NULL,
    cid INT NOT NULL,
    rid INT NOT NULL,
    PRIMARY KEY (redemptionsLogID)
);
INSERT INTO rewardsLog (redeemDate, redemptionTime, cid, rid) VALUES
('2023-03-01', '14:00:00', 1001, 1001),
('2023-03-02', '12:30:00', 1002, 1009),
('2023-03-03', '16:45:00', 1003, 1008),
('2023-03-04', '10:15:00', 1004, 1017),
('2023-03-05', '11:00:00', 1005, 1004),
('2023-03-06', '13:20:00', 1006, 1017),
('2023-03-07', '15:00:00', 1007, 1010),
('2023-03-08', '09:45:00', 1008, 1009),
('2023-03-09', '11:30:00', 1009, 1012),
('2023-03-10', '14:15:00', 1010, 1003);


# Test Creation
use redeemnow_customer;
select * from customer;

use redeemnow_rewards;
select * from rewards;

use redeemnow_rewardslog;
select * from rewardsLog;

