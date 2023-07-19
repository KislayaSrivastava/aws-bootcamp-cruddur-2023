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

App.js, HomeFeedPage.js,SigninPage.js, ProfileInfo.js were modified as below and then the application was restarted to ensure it was working correctly.Also the environment variables were added to docker-compose.yml file. 

1) To configure the aws-amplify, the following was added in the App.js file:

```
import { Amplify} from 'aws-amplify';
Amplify.configure({
  "AWS_PROJECT_REGION": process.env.REACT_APP_AWS_PROJECT_REGION,
  "aws_cognito_identity_pool_id": process.env.REACT_APP_AWS_COGNITO_IDENTITY_POOL_ID,
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID,
  "oauth": {},
  Auth: {
    // We are not using an Identity Pool
    // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
    region: process.env.REACT_APP_AWS_PROJECT_REGION,           // REQUIRED - Amazon Cognito Region
    userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,         // OPTIONAL - Amazon Cognito User Pool ID
    userPoolWebClientId: process.env.REACT_APP_CLIENT_ID,   // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
  }
});
```

2) Following modifications were made to the HomeFeedPage.js

```
import { Auth } from 'aws-amplify';
// Check Auth Method was changed to 
const checkAuth = async () => {
    Auth.currentAuthenticatedUser({ 
      //checks to see if user is authenticated, if yes logs the user and 
      // returns authenticated user and passes this info to cognito_user.
      // Optional, By default is false. 
      // If set to true, this call will send a 
      // request to Cognito to get the latest user data
      bypassCache: false 
    })
    .then((user) => {
      console.log('user',user);
      return Auth.currentAuthenticatedUser()
    }).then((cognito_user) => {
        setUser({
          display_name: cognito_user.attributes.name,
          handle: cognito_user.attributes.preferred_username
        })
    })
    .catch((err) => console.log(err));
  };
```

3) To enable signing in with a cognito username, the following modifications were made to the SigninPage.js file:  

```
import { Auth } from 'aws-amplify';
// changed onsubmit method
const onsubmit = async (event) => {
    setErrors('')
    event.preventDefault();
    console.log('onsubmit')
    Auth.signIn(email, password)
    .then(user => {
      console.log('user',user)
      localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
      window.location.href = "/"
    })
    .catch(error => { 
      if (error.code == 'UserNotConfirmedException') {
        window.location.href = "/confirm"
      }
      setErrors(error.message)
    });
    return false
  }
```

4) Finally, to allow user sign-out, the ProfileInfo.js file was modified as follows:

import { Auth } from 'aws-amplify';
// sign-out method modified
const signOut = async () => {
 try {
     await Auth.signOut({ global: true });
     window.location.href = "/"
 } catch (error) {
     console.log('error signing out: ', error);
    }
}

Then a account was created manually in the system but that led to Token authentication errors since it was manually created. The status of teh account was pending verification and it could not be changed via console. So post some analysis, the below command was shown by Andrew to set a password with admin rights to avoid verification. 

```
aws cognito-idp admin-set-user-password \
 --user-pool-id <your-user-pool-id> \
 --username <username> \
 --password <password> \
 --permanent
```

![image](https://github.com/KislayaSrivastava/aws-bootcamp-cruddur-2023/assets/40534292/74f610ca-2c1f-4fd7-9d27-e8abc8b16659)

Post this I was able to successfully login to my application. 

LOGIN SCREENSHOT TO BE PUT

#### Implementing Custom Signup, Confirmation, and Recovery Page
Next in the similar way, i implemented custom signup, confirmation and password recovery pages.
In all three files, added the Auth function from aws-amplify and then set the correct attributes to be passed to the authentication feature 

1) Modified the SignupPage.js file:
```
import { Auth } from 'aws-amplify';
//modified on-submit
const onsubmit = async (event) => {
    event.preventDefault();
    setErrors('')
    try {
    const { user } = await Auth.signUp({
      username: email,
      password: password,
      attributes: {
        name: name,
        email: email,
        preferred_username: username,
      },
      autoSignIn: { // optional - enables auto sign in after user is confirmed
        enabled: true,
      }
    });
    console.log(user);
    window.location.href = `/confirm?email=${email}`
  } catch (error) {
      console.log(error);
      setErrors(error.message)
  }
    return false
  }
```

2) Modified ConfirmationPage.js

```
import { Auth } from 'aws-amplify';
// modified these 2 methods
const resend_code = async (event) => {
    setErrors('')
    try {
      await Auth.resendSignUp(email);
      console.log('code resent successfully');
      setCodeSent(true)
    } catch (err) {
      // does not return a code
      // does cognito always return english
      // for this to be an okay match?
      console.log(err)
      if (err.message == 'Username cannot be empty'){
        setErrors("You need to provide an email in order to send Resend Activiation Code")   
      } else if (err.message == "Username/client id combination not found."){
        setErrors("Email is invalid or cannot be found.")   
      }
    }
  }

  const onsubmit = async (event) => {
    event.preventDefault();
    setErrors('')
    try {
      await Auth.confirmSignUp(email, code);
      window.location.href = "/"
    } catch (error) {
      setErrors(error.message)
    }
    return false
  }
```

3) Modified RecoveryPage.js

```
import { Auth } from 'aws-amplify';
//updated onsubmit_send_code and onsubmit_confirm_code methods
const onsubmit_send_code = async (event) => {
    event.preventDefault();
    setErrors('')
    Auth.forgotPassword(username)
    .then((data) => setFormState('confirm_code') )
    .catch((err) => setErrors(err.message) );
    return false
  }

  const onsubmit_confirm_code = async (event) => {
    event.preventDefault();
    setErrors('')
    if (password == passwordAgain){
      Auth.forgotPasswordSubmit(username, code, password)
      .then((data) => setFormState('success'))
      .catch((err) => setErrors(err.message) );
    } else {
      setErrors('Passwords do not match')
    }
    return false
  }
```

I was able to successfully reset my password and login with the new password post these changes. 

One thing i found was, it was always better to re-start docker and then the changes would correctly flow. I was struggling with my changes but then i was able to show the pages post refreshing docker. 

Screenshot of my password reset email

![image](https://github.com/KislayaSrivastava/aws-bootcamp-cruddur-2023/assets/40534292/da425810-280f-463f-ac9e-a907dffd07bf)


#### Watched Decenteralized Authentication


#### Watched Decenteralized Authentication
