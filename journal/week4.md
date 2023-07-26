# Week 4 — Postgres and RDS

### Creating Postgres Instance 
1) Initial setup of Postgres database was done in week 1 in the docker-compose file. This was once again checked that the database was coming up corrrectly when the application was being started. 

2) Below command was used to create a RDS PostGres database using AWS CLI in Gitpod. My default region is ```ap-south-1``` 

```
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 14.6 \
  --master-username cruddurroot \
  --master-user-password mypassword123 \
  --allocated-storage 20 \
  --availability-zone ap-south-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp2 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
```

Post this command execution, i logged into the RDS service on the console and verified that i could see the database. Then to save the cost, i stopped the database temporarily. 

![image](https://github.com/KislayaSrivastava/aws-bootcamp-cruddur-2023/assets/40534292/b7f1b70e-3f09-4c69-923d-528ce983982f)

3) Andrew asked to comment the dyanamoDB portion of the code in docker-compose.yml file to save the gitpod credits and so i commented that portion out. 

4) General command to connect to a postgres database is as below
   ```  postgresql://[username[:password]@][netloc][:port][/dbname][?param1=value1&...]    ```

   Command to connect to the local database on local host is below
   ```psql -Upostgres --host localhost```
   After this a prompt comes which asks for the password for user postgres. The password is by default ```password```

   Post logging into the database, i created a database named cruddur
   ```CREATE DATABASE CRUDDUR```

   Also learnt different postgresql commands to use while interacting with the database.

   ```
      \x on -- expanded display when looking at data
      \q -- Quit PSQL
      \l -- List all databases
      \c database_name -- Connect to a specific database
      \dt -- List all tables in the current database
      \d table_name -- Describe a specific table
      \du -- List all users and their roles
      \dn -- List all schemas in the current database
      CREATE DATABASE database_name; -- Create a new database
      DROP DATABASE database_name; -- Delete a database
      CREATE TABLE table_name (column1 datatype1, column2 datatype2, ...); -- Create a new table
      DROP TABLE table_name; -- Delete a table
      SELECT column1, column2, ... FROM table_name WHERE condition; -- Select data from a table
      INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...); -- Insert data into a table
      UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition; -- Update data in a table
      DELETE FROM table_name WHERE condition; -- Delete data from a table
   ```

### Setting up Postgres Drivers on backend-flask 

   a. In addition two python modules needed to run postgres were added to the requirements.txt file and then compiled.

   ```
   psycopg[binary]
   psycopg[pool]
   ```

   b. I also created 2 environment variables to store connection URLs *CONNECTION_URL* for localhost and *PROD_CONNECTION_URL* for production RDS instance

   ```export CONNECTION_URL="postgresql://postgres:password@localhost:5432/cruddur"```
   ```export PROD_CONNECTION_URL="postgresql://cruddurroot:<MYPASSWORD>@cruddur-db-instance.<myUniqueID>.ap-south-1.rds.amazonaws.com:5432/cruddur"  ```

   c. Using the command ```gp env <ENVIRONMENT_VARIABLE>=<VALUE OF THE VARIABLE>``` the environment variables can be exported into Gitpod's environment variables.
   d. Connecting to the aws RDS via the terminal can done by ```psql $PROD_CONNECTION_URL```
   Post using this command I was able to successfully connect to the PostgreSQL installed on the RDS Client. 

### Bash scripting for Database Operations and SQL files

  a. Created two new folders in ```backend-flask``` named ```bin``` and ```db```. In bin folder the batch scripts are stored to execute Create/Connect/Seed data commands on the database. 
  b. Since we were first using localhost then moving to the production environment, then we added below conditional statement to the code 

  ```
   if [ "$1" = "prod" ]; then
    CON_URL=$PROD_CONNECTION_URL
   else
    CON_URL=$CONNECTION_URL
   fi 
  ```
   
   

   
