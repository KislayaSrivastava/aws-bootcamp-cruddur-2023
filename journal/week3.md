# Week 3 — Decentralized Authentication

#### Watched Decenteralized Authentication
I began the week by going through Ashish's Amazon Cognito Decentralized Authentication practices video. I understood about AuthZ/AuthN and other methods commonly used (OAuth2/SAML/JWT/OIDC) and their general use-cases. 
I understood the token lifecycle and people lifecycle. 

Later the Cognito service was explained and the importance of best practices to be used by an application and the AWS were highlighted. 

#### Setup Cognito User Pool
I logged into AWS console and created a userpool named "cruddur-user-pool" and application name "cruddur"
![image](https://github.com/KislayaSrivastava/aws-bootcamp-cruddur-2023/assets/40534292/8a120ffc-0c4b-405b-af12-c360b20d9269)

The next step was to integrate this information into our existing application. 

#### Setup Environment Variables for Frontend and to Enable Sign in 
To interact with aws-cognito from the frontend, we need to install aws-amplify. From the command line, I navigated to the frontend folder. Then I ran the following command:
```$ npm i aws-amplify --save```
Note: -- save option is used because we want this saved in package.json as a developer tool. After running the above command check package.json to see it included.

Then ```app.js``` file was configured with the below variables and the same records were inserted into docker-compose file
#### Required Homework


#### Watched Decenteralized Authentication


#### Watched Decenteralized Authentication
