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
from psycopg_pool import ConnectionPool
import os

connection_url = os.getenv("CONNECTION_URL")
pool = ConnectionPool(connection_url)

def query_wrap_object(template):
  sql = f"""
  (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
  {template}
  ) object_row);
  """
  return sql

def query_wrap_array(template):
  sql = f"""
  (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
  {template}
  ) array_row);
  """
  return sql

connection_url = os.getenv("CONNECTION_URL")
pool = ConnectionPool(connection_url)
```

b) The environment variable ```CONNECTION_URL``` in docker compose was updated from ```CONNECTION_URL``` to ```PROD_CONNECTION_URL```
c) Under ```services/home-activities.py``` the mock endpoint was replaced with an actual API call
```
from datetime import datetime, timedelta, timezone
from opentelemetry import trace
from lib.db import pool,query_wrap_array

tracer = trace.get_tracer("home.activities")

class HomeActivities:
  def run(cognito_user_id=None):
    print("HOME ACTIVITY")
    #logger.info("HomeActivities")
    with tracer.start_as_current_span("Home-Activities_MockData"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat())

      sql = query_wrap_array("""
      SELECT 
      activities.uuid,
        users.display_name,
        users.handle,
        activities.message,
        activities.replies_count,
        activities.reposts_count,
        activities.likes_count,
        activities.reply_to_activity_uuid,
        activities.expires_at,
        activities.created_at
      FROM public.activities
      LEFT JOIN public.users ON users.uuid = activities.user_uuid
      ORDER BY activities.created_at DESC
      """)
      print(sql)
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchone()
      print(json[0])
      return json[0]
```
d) Post this when the job was triggered, I was able to successfully see the records.
![image](https://github.com/KislayaSrivastava/aws-bootcamp-cruddur-2023/assets/40534292/0a97ff48-d706-48c1-90ef-1d93c2ec887d)

### Setup Cognito post confirmation lambda

Now post setup of the database it was expected to write into ```user``` table when a new user signed up from the application. 

Two Steps were taken:
a) A new lambda function was created and post creating the following script was updated in its code. 
```
  import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']

    print('User Attributes')
    print(user)
    
    user_display_name = user['name']
    user_email        = user['email']
    user_handle       = user['preferred_username']
    user_cognito_id   = user['sub']

    try:
        conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
        cur = conn.cursor()
        
        sql = f"""
            INSERT INTO users (
                display_name,
                email,
                handle,
                cognito_user_id
                )
            values (
                '{user_display_name}',
                '{user_email}',
                '{user_handle}',
                '{user_cognito_id}')
        """
        print('Connection URL---')
        print(conn)
        print('SQL Statement ----')
        print(sql)
        
        cur.execute(sql)
        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event
```

b) Next since psycopg2 is not avaiable as a AWS Supported layer so i used a third party pre-compiled layer for this. Since my default region is ```ap-south-1``` so i had to choose a layer compatible with that region. The version of python supported was ```3.7``` so i made my lambda function on python 3.7 and added the layer for ```ap-south-1``` from this link <https://github.com/jetbridge/psycopg2-lambda-layer> 

![image](https://github.com/KislayaSrivastava/aws-bootcamp-cruddur-2023/assets/40534292/4dcf2119-be5d-404c-83f8-087b3f5f2435)

Now the environment variable were also added in the configuration setup of the Lambda function

![image](https://github.com/KislayaSrivastava/aws-bootcamp-cruddur-2023/assets/40534292/26aaa2b2-8fa2-47cd-9c5b-3c3d2bdf899b)

c) The next part was to integrate this function into the same VPC which housed our Cognito and other functions.
![image](https://github.com/KislayaSrivastava/aws-bootcamp-cruddur-2023/assets/40534292/b5e41b53-a641-4bee-a9d2-539ff947fce1)

Once all of this was done, I tried saving the changesbut got this error message at the bottom of the page.

```
The provided execution role does not have permissions to call CreateNetworkInterface on EC2
```
Googling let me to this page <https://stackoverflow.com/questions/41177965/the-provided-execution-role-does-not-have-permissions-to-call-describenetworkint> and i used the AWS CLI option mentioned to modify the security group id and add the AWS managed policy (AWSLambdaVPCAccessExecutionRole) to the service role.

  1) Ask Lambda API for function configuration, query the role from that, output to text for an unquoted return.
```
    aws lambda get-function-configuration \
        --function-name <<your function name or ARN here>> \
        --query Role \
        --output text
```
  From this output take the service name and then use that in the below attach-policy command.

  2. Attach Managed Policy AWSLambdaVPCAccessExecutionRole to Service Role
```
aws iam attach-role-policy \
    --role-name your-service-role-name \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
```
d) Now this lamdba function was added as a ````Post Confirmation``` lambda trigger under the ```user pool properties``` of the user Pool.

e) Post all of this one record was successfully inserted into the database table.

![image](https://github.com/KislayaSrivastava/aws-bootcamp-cruddur-2023/assets/40534292/04cb8343-43ef-495a-ab14-9d05da3b468b)

Cognito User Pool Update   

![image](https://github.com/KislayaSrivastava/aws-bootcamp-cruddur-2023/assets/40534292/be717165-fafc-4ebb-b195-81989d229c4e)

### Creating New Activities with a Database Insert


