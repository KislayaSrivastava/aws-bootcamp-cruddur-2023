# Week 1 — App Containerization
I have watched the live streaming video on app containerization. 

I created two seperate dockerfiles one for the backend and one for the frontend. 

This is for the flask backend. 

![image](https://user-images.githubusercontent.com/40534292/227092675-b0f09a24-69c5-4059-9a47-ee6dd1c536d2.png)

This is for the react frontend

![image](https://user-images.githubusercontent.com/40534292/227092823-d6bfce50-ebbf-45f9-be7d-9a34234df9e0.png)

I build the files using docker build command and then checked the generated URL at respective port numbers to ensure that the application was accessible. 
I later created the docker compose file which contained all the information needed to bring up the application in one go. 

![image](https://user-images.githubusercontent.com/40534292/227093621-bcbb962b-fde5-41e6-a568-733124009545.png)

Then right-clicking on this file and using docker compose up, i was able to bring up the application in one go.  
Later i committed all the changes to github. 

In the next video I followed along with Andrew and created the flask backend endpoint and the react page for showing the notifications. Later i tested the changes and finally committed them to github from Gitpod.

In the next video, i added dynamoDB local container settings to the docker compose file and tested it out. It was working. 
In the same video, steps were provided to add a postgres container to the docker and to connect to the test database. 

I tried out the steps. I was unable to install the postgres container. Message while installing postgres

![image](https://user-images.githubusercontent.com/40534292/227094600-55484a59-0c99-4112-90f4-03188d395e67.png)

Tried different ways to get to the psql terminal but was unsuccessful. 

![image](https://user-images.githubusercontent.com/40534292/227095526-77fb3587-4aeb-4802-a096-cb75042b5380.png)

Later i added an postgres extension in gitpod.yml file that installed the databases extensions. 

Even with that, i was not able to connect using default id and password. 

![image](https://user-images.githubusercontent.com/40534292/227095145-97dbef57-1375-4cad-9219-9981ccf52bb4.png)

In the next two videos i understood docker security and cost considerations. Later i gave the two quizzes. 

So Was able to do successfully everything apart from enabling postgres and running it. 

Still trying to find solution to this issue. 
