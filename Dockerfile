FROM ubuntu:20.04
RUN apt-get -y update
RUN apt-get install python3 -y
RUN apt-get install -y python3-pip

ENV PYTHONUNBUFFERED 1
#directory to store app source code
RUN mkdir /tufleur

WORKDIR /tufleur

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]