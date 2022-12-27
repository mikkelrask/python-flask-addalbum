FROM python:3.10.0-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR app

RUN pip3 install -r requirements.txt

COPY . /app


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
