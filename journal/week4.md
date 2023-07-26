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

   a. In addition two python modules needed to run postgres were added to the requirements.txt file and then compiled.

   ```
   psycopg[binary]
   psycopg[pool]
   ```
   Then the modules were compiled using 
   ```pip install -r requirements.txt```

   b. The environment variable was modified for the ```backend-flask``` application in ```docker-compose.yml```
   ```
    backend-flask:
      environment:
        CONNECTION_URL: "${CONNECTION_URL}"
   ```
   c. I also created 2 environment variables to store connection URLs *CONNECTION_URL* for localhost and *PROD_CONNECTION_URL* for production RDS instance

   ```export CONNECTION_URL="postgresql://postgres:password@localhost:5432/cruddur"```
   ```export PROD_CONNECTION_URL="postgresql://cruddurroot:<MYPASSWORD>@cruddur-db-instance.<myUniqueID>.ap-south-1.rds.amazonaws.com:5432/cruddur"  ```

   
   d. Using the command ```gp env <ENVIRONMENT_VARIABLE>=<VALUE OF THE VARIABLE>``` the environment variables can be exported into Gitpod's environment variables.
   e. Connecting to the aws RDS via the terminal can done by ```psql $PROD_CONNECTION_URL```
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

  Also to add a different color to the header the below code block was used in all the scripts. The label value kept on changing depending on what the script was doing. 

  ```
    CYAN='\033[1;36m'
    NO_COLOR='\033[0m'
    LABEL="<LABEL YOUR LABEL"
    printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
  ```

  c. In db folder there were two files created, schema.sql and seed.sql. The schema.sql file contained table model for the database and the seed.sql contains manually generated testing data for seeding the tables. 
  d. In addition multiple scripts db-seed, db-connect, db-schema-load and others were created in bin folder. In addition, one script ```db-setup``` was created which called all these scripts sequentially to first drop the database if it exists, then create the database, then load the schema in two tables users and activities and finally seeding the tables with the mock data.
  e. I was able to successfully connect to the database using the script ```db-connect```
  f. At the time of connecting to the production database, we faced an issue where we had to give the GITPOD's IP as a trusted resource in the security-group created in the RDS Database. Since each time the GITPOD's ip would change so 
    1-> The IP was found and exported via ```export GITPOD_IP=$(curl ifconfig.me)```
    2-> Two new environment variables were created namely DB_SG_RULE_ID and DB_SG_RULE. The DB_SG_RULE is the security group id of the security group attached to the rds instance and the DB_SG_RULE_ID is the rule id contained in the security group attached to the rds instance. 
    ```
      export DB_SG_ID="<SECURITY_GROUP_ID>"
      gp env DB_SG_ID="<SECURITY_GROUP_ID>"
      export DB_SG_RULE_ID="<SECURITY_GROUP_RULE_ID>"
      gp env DB_SG_RULE_ID="<SECURITY_GROUP_RULE_ID>"
    ```
    3-> So a script was created which used the GITPOD_IP and the exported environment variables of DB_SG_ID and DB_SG_RULE_ID to modify the security group rule each time post startup of the application. 
    ```
      aws ec2 modify-security-group-rules \
      --group-id $DB_SG_ID \
      --security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={Description=GITPOD,IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$GITPOD_IP/32}"
    ```
    4-> To trigger this script at every instance of the gitpod coming up, a command was added to the gitpod.yml file under postgres section 
      ```
        export GITPOD_IP=$(curl ifconfig.me)
        source "$THEIA_WORKSPACE_ROOT/backend-flask/bin/rds-update-sg-rule"
      ```
### Install Postgres Driver in Backend Application and Connecting to Local RDS Instance

a) Created a new folder ```lib``` under ```backend-flask``` and created a file ```db.py``` to help enable query the database.
```

```
   

   
