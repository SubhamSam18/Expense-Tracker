#The following line tells Docker which base image to use — in this case, a Python image.
FROM python:3.8-alpine

#we're telling Docker to use the same directory and name for the rest of its operations
WORKDIR /app

# copy the remainder of the files in our local working directory to the directory in the docker image.
COPY . .

RUN pip3 install -r ./requirements.txt

#This line specifically instructs Docker to run our Flask app as a module, as indicated by the "-m" tag. Then it instructs Docker to make the container available externally, such as from our browser, rather than just from within the container. We pass the host port:
CMD ["python3", "-m"]

EXPOSE 5050