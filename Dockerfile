FROM python:3.8-alpine
EXPOSE 5000
WORKDIR /app
COPY . .
RUN pip3 install -r ./requirements.txt
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]