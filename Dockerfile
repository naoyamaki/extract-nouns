FROM python:3.12

WORKDIR /usr/src
COPY ./src/requirements.txt /usr/src/requirements.txt
RUN apt-get update && apt-get -y install libmecab-dev
RUN pip install -r requirements.txt

CMD [ "flask", "run", "--host=0.0.0.0" ]
