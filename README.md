# IoT Project - Smile To Access
IoT project to analysis faces (Smile and Emotions) with AWS Rekognition, Raspberry, Pi Camera, Flask, and MySQL

Important references used: 

https://www.hackster.io/gr1m/raspberry-pi-facial-recognition-16e34e 

https://github.com/af001/pi-detector

## Technical description

### Requirement 
In this project we have used the following hardware/software components: 
* Raspberry Pi 3 (Model B+)
* Raspberry Pi-Camera 5Mp
* Amazon Rekognition Service 
* Python 3.6 (64 bit)
* Flask library 
* MySQL 


### AWS Rekognition 

We have used AWS Free Tier service, which allows us to have 1000 faces stored per month in addition to 5000 images processed per month. 
We have created an AWS account which gives us 12 month Free Tier on the following link: 

https://portal.aws.amazon.com/billing/signup 

Then we have created a new IAM user that has administrative privileges to Rekognition service, after that we are able to download our credentials which contains two main keys: 

* `aws_access_key_id`
* `aws_access_key_secret` 

Those information can be obtained from “security credential” in the console. 
We have also configured the region to be “US-East”. 

In this project we have used four main api methods: 
* Create collection 
* Index Faces 
* Detect Faces 
* Search Faces by image  

 https://docs.aws.amazon.com/rekognition/latest/dg/API_Reference.html 


### Architecture 

The system architecture is based on the following components:
- Hardware (Raspberry and pi camera)
- Software (Flask, MySQL, AWS)

The process start with a running flask application which serve HTML pages. The client first can ask two different business services: 
* train new pictures 
* access
 
Once the client ordered a service, the application will call the relevant functionality in the application which contains invoking AWS Rekognition service with a specific request and handle the response back. Then store the information in MySQL database. And displaly the relevant results in the client side (html page).  

### Setup environment
We must have a stable python version (2.7 is used in our project) with these libraries: 

* Picamera: This package provides a pure Python interface to the raspberry pi camera module for Python 2.7 (or above) or Python 3.2 (or above).
* Mysql.connector: MySQL driver written in python 
* Boto3: is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python
* Flask: is a lightweight WSGI web application framework

We have also installed AWS Command line interface (awscli) on raspberry: 

https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html#install-tool-pip 

Then we configure aws credentials by using this command:  `aws configure`


### Python Project Description 
Our python project has the following packages: 
* Modules include aws method implementation, camera access and database initialization
* Resources include sql script for database creation 
* Static include js, css, images files 
* Templates include html pages 
* Main.py which is the main application code
