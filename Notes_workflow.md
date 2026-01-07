## 📁 Project Setup and Structure

### Step 1: Project Template
- Start by executing the `template.py` file to create all initial required files and folder.

### Step 2: Package Management
- Write the setup for importing local packages in `setup.py` and `pyproject.toml` files.
- **Tip**: Learn more about these files from `crashcourse.txt`.
- install required moduled listed in requirements.txt 
    - "pip install -r requirements.txt"

## 📊 MongoDB Setup and Data Management

### Step 4: MongoDB Atlas Configuration
1. Sign up for [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and create a new project.
2. Set up a free M0 cluster, configure the username and password, and go to "network access" and ip address(`0.0.0.0/0`) so that you can access it from anywhere and any network.
3. Retrieve the MongoDB connection string for Python and save it (replace `<password>` with your password).

### Step 5: Pushing Data to MongoDB
1. Create a folder named `notebook`, add the dataset, and create a notebook file `mongoDB_demo.ipynb`.
2. Use the notebook to push data to the MongoDB database.
3. Verify the data in MongoDB Atlas under Database > Browse Collections.

## **Note**
### **-e .**
- e in requirements.txt  :  SO basically any directory with file name   __init__.py is a package and since it stored in our local machine so we call it local packages.
- so if we wanted to import src anywhere in local machine without errors( when importing src in other directories) then we need to install these local packages in your local machine.

- So how to install it in venv : just add -e . in the end of requirements.txt file.
- The setup.py and pyproject.toml file works together to install local packages in the venv
- so now you can access src package outside the src or anywhere within this venv

## **setup.py and pyproject.toml**

1. What is a pyproject.toml file?

TOML (Tom’s Obvious, Minimal Language): It’s a simple configuration file format (like JSON or YAML) but is easier to read and write. 
TOML is becoming the standard for Python packaging metadata.

2. Why pyproject.toml is important:

> It was introduced with PEP 518 to modernize Python package building. Previously, everything was done using setup.py 
  but now pyproject.toml allows for more flexibility, better dependency management, and cleaner project configuration.
> It centralizes metadata about the project: project name, version, dependencies, authors, etc.
> It supports various build systems (like setuptools, poetry, etc.).

3. Explaining sections of pyproject.toml:

[project]: Defines the basic project information (name, version, description, authors).
[tool.setuptools]: Specifies that setuptools is being used to build the project.
[tool.setuptools.dynamic]: Links the external files (like requirements.txt) to dynamically pull dependencies.

4. setup.py with the advent of pyproject.toml: Some tasks previously handled by setup.py (like metadata) are now managed 
   by pyproject.toml. However, setup.py can still be used, especially if you have complex build steps.

5. How do setup.py, pyproject.toml, and requirements.txt work together?

> pyproject.toml: It’s now the central place for project metadata. Instead of defining your dependencies and project 
  information in setup.py, you can define them in pyproject.toml.
  As we did in your project, the line [tool.setuptools.dynamic] dependencies = {file = "requirements.txt"} links your requirements.txt 
  file to the TOML file, so when the project is built, the dependencies are fetched from requirements.txt.

> setup.py: While it’s still used for custom builds and configurations, most of the basic functionality (like metadata and dependencies) 
  is being transferred to pyproject.toml. You might still keep a minimal setup.py if you have custom build steps, but for many projects, 
  it’s not necessary anymore with pyproject.toml.

> requirements.txt: It lists all project dependencies and their versions.

When you run pip install -r requirements.txt, it ensures that all dependencies are installed. The pyproject.toml file can reference 
it (as we did) so that package dependencies are automatically pulled from there.

# **Data Ingestion 📥**
- src.constant
    - Add code in constant dir : add all constant variables here.
- src.configuration 
    - Add code to mongo_db_connection.py and define the func for mongo_db connection to stablish connection with mongo db server.
    - How to set MongoDb URL in venv variable  for (os.getenv(MONGODB_URL_KEY) in src.configure.mongo_db_connection.py)---> set: export MONGODB_URL="mongodb+srv://santosh4thmarch_db_user:santosh@#9605@cluster0.5cjjjrf.mongodb.net/?appName=Cluster0"
    check: echo $MONGODB_URL

    - in constants package MONGODB_URL_KEY = "MONGODB_URL" must be as same beacause os.getenv(MONGODB_URL_KEY) will look for the str "MONGODB_URL" which is saved in venv byt this command        #export MONGODB_URL="mongodb+srv://santosh4thmarch_db_user:santosh@#9605@cluster0.5cjjjrf.mongodb.net/?appName=Cluster0" 

    - > The real issue is that the MongoDB URL contains @#9605 which needs to be URL-encoded as %40%239605. Update your environment variable with the properly encoded credentials:
    - > export MONGODB_URL="mongodb+srv://santosh4thmarch_db_user:santosh%40%239605@cluster0.5cjjjrf.mongodb.net/?appName=Cluster0"

- src.data_access
    - Add code in proj1_data.py , it will use configuration.mongo_db_connection.py and fetch data from mongoDB and convert it into data frame
- src.entity
    - Add code to config_entity.py , till DataIngestionConfig class --> pulling variables data from constant local package module ---> and  storing data ingestion variables , we are gonna use dataclass(this Auto creates the essential methods like __init__ so we just need to store varaibles as instance) module to store varibales 
    - Add code to Artifact_entity.py, till DataIngestionArtifact class : it will return file paths of output data file like training file path

- src.components
    - Add code in data_ingestion.py , in this file we are gonna use all 4 points that we dicussed in upper and it will save Train & Test data sets in the end.

- src.pipeline
    - Add code in training_pipeline.py : it will use all files and modules to fetch and save mongo db data into our local for instant.
    

# **Data Validation, Data Transformation & Model Trainer**

## Data Validation
1. complete the work on src.utils.main_utils.py (it have some reusable function which will be used in most of MLops projects), and config.schema.yaml (to store dataset table schema details for data validation) files
2. follow below workflow and add code in these
    - constants : All varibles and their values for data validation has been added already
    - config_entity : create @dataclass class to store data validation related only paths or orther varibles values
    - artifact_entity : store what type of values and what Data validation will return in the end.
    - components : code src.components.data_validation.py file.
    - pipeline : add code for data validation in src.pipeline.training pipeline
    - app.py/ demo.py

## Data Trasformation
- Data tranformation workflow: 
    - constants : All varibles and their values for data Transformation has been added already
    - config_entity : create @dataclass class to store data Transformation related only paths or orther varibles values
    - artifact_entity : store what type of values and what Data Transformation will return in the end.
    - components : code src.components.Transformation.py file.
    - pipeline : add code for data Transformation in src.pipeline.training pipeline
    - app.py/ demo.py

## Model Training
- Model trainer workflow
    - constants : All varibles and their values for **Model trainer** has been added already
    - config_entity : create @dataclass class to store **Model trainer** related only paths or orther varibles values
    - artifact_entity : store what type of values and what **Model trainer** will return in the end.
    - components : code src.components.model_trainer.py file.
    - Note: mode.yaml file is not used in this project.
    - pipeline : add code for data Transformation in src.pipeline.training pipeline
    - app.py/ demo.py

# Last Push for the year 2025

# First push for the year **2026**
_[Embedded Image Removed]_

##

# Model Evaluation and pushing

1. Before moving to next component of Model Evaluation, some AWS services setup is needed:
      * Login to AWS console.
      * Keep region set as - us-east-1
      * Go to IAM >> Create new user (name: firstproj)
      * Attach policy >> select AdministratorAccess >> next >> create user
      * Go to the user >> Security Credentials >> Access Keys >> Create access key
      * Select CLI >> agree to condition >> next >> Create Access Key >> download csv file
      * Set env variables with above csv values using below method:
      ====================================================================================
         >> Set env var from bash terminal: <<
         export AWS_ACCESS_KEY_ID="AWS_ACCESS_KEY_ID"
         export AWS_SECRET_ACCESS_KEY="AWS_SECRET_ACCESS_KEY"
         >> Check env var from bash terminal: <<
         echo $AWS_ACCESS_KEY_ID
         echo $AWS_SECRET_ACCESS_KEY

         >> Set env var from powershell terminal: <<
         $env:AWS_ACCESS_KEY_ID="AWS_ACCESS_KEY_ID"
         $env:AWS_SECRET_ACCESS_KEY="AWS_SECRET_ACCESS_KEY"
         >> Check env var from powershell terminal: <<
         echo $env:AWS_ACCESS_KEY_ID
         echo $env:AWS_SECRET_ACCESS_KEY
      ====================================================================================
      * Now add the access key, secret key, region name to constants.__init__.py
      * Add code to src.configuration.aws_connection.py file (To work with AWS S3 service)
      * Ensure below info in constants.__init__.py file:
            MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
            MODEL_BUCKET_NAME = "my-model-mlopsproj"
            MODEL_PUSHER_S3_KEY = "model-registry"
      * Go to S3 service >> Create bucket >> Region: us-east-1 >> General purpose >>
        Bucket Name: "my-model-mlopsproj" >> uncheck: "Block all public access" and acknowledge >>
        Hit Create Bucket
      * Now inside "src.aws_storage" code needs to be added for the configurations needed to pull 
        and push model from AWS S3 bucket. 
      * Inside "entity" dir we will have an "s3_estimator.py" file containing all the func to pull/push
        data from s3 bucket.

2. Model Evaluation.

- Model Evaluation and pushs workflow: 
    - constants : add the code
    - config_entity : create @dataclass class to store model evaluation & push related only paths or orther varibles values
    - artifact_entity : store what type of values and what  model evaluation & push will return in the end.
    - components : code src.components.model_evaluation.py  & model_pusher.py file.
    - cloude_storage : add code in aws.storagepy  : manage s3 like file reading, upload etc
    - entity.s3_estimator.py : to save and load model from s3 bucket.
    - pipeline : add code for model_evaluation and model pusher in src.pipeline.training pipeline
    - app.py/ demo.py

  Note: The code is compare performance between s3 and recently trainned model.

# **Prediction pipeline and Model Deployement**

- Prediction pipeline : Handle the data caming from the website and precting
    - Code prediction_pipeline.py
    - code app.py
    - config entity: stored some variables
    - used LLM to generate rendering files like html and css accordinng to our code structure and app.py file

# Some important crash courses 

## Corss origin resource sharing (CORS)

Here is an explanation of CORS (Cross-Origin Resource Sharing) in FastAPI, using simple terms and analogies.

### What is CORS? (The Simple Explanation)

Imagine your website's **Frontend** (what the user sees, e.g., React/Vue running on `localhost:3000`) and your **Backend** (FastAPI running on `localhost:8000`) are two different houses.

**The Rule:** Web browsers (Chrome, Firefox) are like strict security guards. By default, they **do not allow** a person from "House A" to walk into "House B" to take things. This is for safety, to stop strangers from stealing data.

**The Solution (CORS):** CORS is a way for "House B" (FastAPI) to tell the security guard (Browser): *"It's okay! I know House A. Let them in."*

---

### Why do you need it?

If you try to connect your frontend to your FastAPI backend without configuring CORS, you will see a big red error in your browser console that says something like:

> *"Access to fetch has been blocked by CORS policy."*

This happens because they are on different **"Origins"**:

* **Origin 1:** `http://localhost:3000` (Your Frontend)
* **Origin 2:** `http://localhost:8000` (Your API)

Even though they are both on your computer (`localhost`), the different ports (`3000` vs `8000`) make the browser treat them as strangers.

---

### How to Fix it in FastAPI

FastAPI has a built-in tool called `CORSMiddleware` that handles this for you. It essentially creates a "Guest List" of who is allowed to talk to your API.

Here is the standard code to fix it:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. Define the "Guest List" (Allowed Origins)
# These are the URLs of your frontend apps that you trust.
origins = [
    "http://localhost:3000",
    "https://my-react-app.com",
]

# 2. Add the Middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Who is allowed to enter? (The Guest List)
    allow_credentials=True,       # Can they bring cookies/auth tokens?
    allow_methods=["*"],          # What actions can they do? (GET, POST, PUT, DELETE)
    allow_headers=["*"],          # What special info can they send?
)

@app.get("/")
def main():
    return {"message": "Hello! The security guard let you in."}

```

### Breakdown of the Configuration

1. **`allow_origins` (The Guest List):**
* This is the most important part. You list exactly which domains are allowed.
* *Lazy way:* You can set this to `["*"]` to allow **everyone**. This is okay for development, but dangerous for production (you don't want hacker sites talking to your API).

2. **`allow_methods` (The Actions):**
* Methods are HTTP verbs like `GET` (read), `POST` (create), `DELETE`.
* `["*"]` means they can do anything.

3. **`allow_headers`:**
* Headers are extra bits of info sent with the request (like `Authorization: Bearer...` or `Content-Type`).
* `["*"]` allows any standard headers.

### The "Preflight" Request (The Polite Knock)

Sometimes, before your browser sends the *actual* data (like a POST request with a file), it sends a tiny "test" message first called an **OPTIONS** request.

Think of this as the browser knocking on the door and asking: *"Hey, are you accepting packages from localhost:3000 today?"*

* **If FastAPI says "Yes":** The browser sends the real data.
* **If FastAPI says "No" (or doesn't answer):** The browser blocks the request immediately.

`CORSMiddleware` handles this "knock" (Preflight) automatically for you so you don't have to write code for it.

# **async and await keyword in python**

### 1. The Core Concept: The Event Loop

Python runs on a single thread called the **Main Thread**. Inside this thread, there is a mechanism called the **Event Loop**.

* **Role:** The Event Loop manages tasks. It executes code line-by-line.
* **The Problem:** In standard code (synchronous), if a line takes 5 seconds (like a network request), the Event Loop is blocked. The entire application freezes for 5 seconds.

### 2. `async` and `await` keywords

These keywords allow non-blocking execution.

* **`async def`**: Defines a "Coroutine." It tells Python this function will not run immediately when called. Instead, it returns a coroutine object that creates a task for the Event Loop.
* **`await`**: This is the yield point. It tells the Event Loop: *"Pause this specific function, release control back to the loop, and go execute other pending tasks. Come back here only when this I/O operation is finished."*

### 3. Execution Flow

**Synchronous (`def`)**

```python
# Thread is BLOCKED during IO
data = requests.get(url)  # Code stops here. CPU sits idle waiting for network.
process(data)             # Runs only after get() finishes.

```

**Asynchronous (`async def`)**

```python
# Thread is NOT blocked during IO
data = await client.get(url) # Code pauses locally. Event Loop switches to other requests.
# ... (Event Loop handles other API calls here) ...
# When network response arrives, Event Loop jumps back here.
process(data)

```

### 4. FastAPI Specifics (Concurrency)

FastAPI handles `async def` and `def` differently to optimize performance.

**Case A: I/O Bound (Database, External APIs)**

* **Use:** `async def`
* **Behavior:** The function runs directly on the Main Thread. When it hits `await`, it yields control, allowing the server to handle thousands of concurrent requests on that single thread.

**Case B: CPU Bound (ML Inference, Pandas, Heavy Math)**

* **Use:** `def` (Standard function)
* **Behavior:** FastAPI detects this is not `async`. It automatically runs this function in a separate thread from a **Thread Pool** (using `anyio`).
* **Why:** If you used `async def` for a CPU-heavy task, you would block the Main Thread/Event Loop because there is no `await` (no I/O) to yield control.

### Summary Rule for ML

* If your code waits for a database or API: Use `async def` + `await`.
* If your code calculates (Inference/Processing): Use `def`.

-------------------------------------------------------------------------------------------

### async def ---> means this function have ability to paused

When Python sees your code:

1. **`async def my_function()`**
* **Python thinks:** "Okay, `my_function` is a 'coroutine'. It allows multitasking. I will look for `await` keywords inside it."

2. **`await database.get_data()`**
* **Python thinks:** "Aha! The function told me to wait here. I will freeze `my_function` right now, go handle a request for User B, and come back here when the database replies."

### Visual Summary

| Keyword | What it tells Python | Real-world Analogy |
| --- | --- | --- |
| **`async def`** | "I am capable of multitasking." | The waiter puts on running shoes. He is *ready* to move fast, but he hasn't moved yet. |
| **`await`** | "Pause me, I'm waiting for data." | The waiter sends an order to the kitchen and immediately walks away to serve another table. |

# **CIIC on AWS**         
##                             ----> on next project will try to aplply it on both github actions and amazon ecr too

- Workflow
    - setup docker image----> Dcokerfile & add unnecessary files to .dockerignore
    - setup the .github/workflows dir and aws.yaml( script of cicd for github action to deploy docker image on application on aws ECR instance.

    - Assign ECR service to the IAM user on aws if not created IAM user then create it and assign it a ECR service.

    - Now create a ECR repo to store the docker image.( make sure the region is us-east-1)

* Now create EC2 Ubuntu server 
  >> AWS console 
  >> EC2 
  >> Launch Instance 
  >> name: vehicledata-machine

>> Image: Ubuntu 
   >> AMI: Ubuntu Server 24.04 (free tier)
   >> Instance type: t2.medium (chargeable ~3.5rs/hr)

>> Create new key pair (name: proj1key)
>> Allow HTTPS and HTTP traffic
>> Storage: 30GB
>> Launch

>> Go to instance 
   >> Click on "Connect"
   >> Connect using EC2 Instance Connect

>> Connect (Terminal will be launched)

Now you have EC2 server machine terminal opened now install docker on it
      ## Optinal
      sudo apt-get update -y
      sudo apt-get upgrade
      ## Required (Because Docker is'nt there in our EC2 server - [docker --version])
      curl -fsSL https://get.docker.com -o get-docker.sh
      sudo sh get-docker.sh
      sudo usermod -aG docker ubuntu
      newgrp docker

Next step is to connect Github with EC2(Self hosted runner):
      * select your project on Github >> go to settings >> Actions >> Runner >> New self hosted runner
        >> Select OS (Linux) >> Now step by step run all "Download" related commands on EC2 server 
        >> run first "Configure" command (hit enter instead of setting a runner group, runner name: self-hosted)
        >> enter any additional label (hit enter to skip) >> name of work folder (again hit enter)
        >> Now run second "Configure" command (./run.sh) and runner will get connected to Github
        >> To crosscheck, go back to Github and click on Runner and you will see runner state as "idle"
        >> If you do ctrl+c on EC2 server then runner will shut then restart with "./run.sh"

30. Setup your Github secrets: (Github project>Settings>SecretandVariable>Actions>NewRepoSecret)
      AWS_ACCESS_KEY_ID
      AWS_SECRET_ACCESS_KEY
      AWS_DEFAULT_REGION : us-east-1
      ECR_REPO: name of ecr repo  : vehicledata-machine
      MONGODB_URL : if wanted that train model button should work on web UI then add mongodb url.

31. CI-CD pipeline will be triggered at next commit and push.

32. Now we need to activate the 5000 port of our EC2 instance, because by default on aws EC2 the 5000 port is not exposed:
      * Go to the instance > Security > Go to Security Groups > Edit inbound rules > add rule
        > type: Custom TCP > Port range: 5000 > 0.0.0.0/0 > Save rules   
33. Now paste the public ip address of running EC2 instance then append ":5000" , like "http://<public_ip>:5000" and your app will be launched.
34. You can also do model training on /training route.

------------------------------------------------------------------------------------------------------------------------------------

It seems that the self-hosted runner stopped because it's designed to run in the foreground of the terminal when executed with `./run.sh`. This means that if you closed the terminal session or the EC2 instance restarted, the runner would have stopped. To ensure it runs persistently in the background and starts automatically, you should set it up as a service.

Here’s how to do that on your EC2 instance:

### 1. Navigate to the Runner Directory

First, make sure you’re in the `actions-runner` directory on your EC2 instance:

```bash
cd ~/actions-runner
```

### 2. Set Up the Runner as a Service

To run the self-hosted GitHub runner as a background service, GitHub provides a built-in script to install it as a service.

Run the following command in the `actions-runner` directory:

```bash
sudo ./svc.sh install
```

This command will install the runner as a service, making it easier to start, stop, or restart it.

### 3. Start the Service

After installing the service, start it using the following command:

```bash
sudo ./svc.sh start
```

### 4. Check the Status

You can check the status of the runner service to ensure it’s running:

```bash
sudo ./svc.sh status
```

### 5. Enable the Service to Start on Boot (Optional)

To ensure that the runner service starts automatically when the EC2 instance reboots, you can use the following command:

```bash
sudo systemctl enable actions.runner.<your-runner-name>.service
```

### Additional Notes

- **Replace `<your-runner-name>`**: When checking the status or enabling the service, replace `<your-runner-name>` with the specific name of your runner service. You can find the name of the service by running `systemctl list-units | grep actions.runner`.

- **Re-register the Runner**: If you’re still experiencing issues, there may have been an issue during setup. You might need to re-register the runner. To do this, stop the service, remove the runner, and start the configuration process again with a new registration token from your GitHub repository's settings.

### Example Commands

```bash
# Stop and remove the service (if needed)
sudo ./svc.sh stop
sudo ./svc.sh uninstall

# Re-configure the runner
./config.sh --url https://github.com/vikashishere/MLOps-Test-Proj --token <NEW_TOKEN>

# Re-install and start the service
sudo ./svc.sh install
sudo ./svc.sh start
```

After following these steps, the runner should be persistently running as a background service on your EC2 instance and ready to accept jobs.

There is one more thing that could be throw an error while tap on traing the model using ec2 runing server.   the aws access id and aws secret key is importing in code using os.getenv()   beacuse i export the secrects in my MLopss enviroemnt but , do docker know this in aws ec2? but i added these secrects in github action secrect , so now whal will gonna happened ?

You have absolutely nothing to worry about! Your setup is 100% correct.

How it works:

GitHub Actions has the secrets stored securely.
In your aws.yaml file, we are explicitly passing these secrets to the Docker container when we start it. Look at this line in your aws.yaml:
yaml
docker run ... -e AWS_ACCESS_KEY_ID="${{ secrets.AWS_ACCESS_KEY_ID }}" ...
The -e flag stands for "environment variable". It takes the secret from GitHub and "injects" it into the Docker container as an environment variable.
Inside the container, your Python code calling os.getenv("AWS_ACCESS_KEY_ID") will see the value just as if it were exported locally.
So, Docker "knows" these secrets because your GitHub Action manually handed them over during the docker run command.

You are good to go! Just push your latest changes (app.py, removal of demo.py, etc.), and everything should work perfectly.

