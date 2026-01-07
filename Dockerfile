# using light-weight python image for docker
FROM python:3.13.11-slim      

# create app directory
WORKDIR /app

# copy all files from the project into the app directory inside the docker but we will add unnecessary files to the .dockerignore
COPY . /app

#install all dependencies
RUN pip install -r requirements.txt


#Expose the port on fast api application(app.py) will run, so that we can access it from outside the docker
EXPOSE 5000

# run the application
CMD ["python", "app.py"]


