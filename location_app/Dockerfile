FROM python:3.8
ENV PYTHONUNBUFFERED 1

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements
COPY ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add app
COPY . /usr/src/app

EXPOSE 8000

# Run the production server
# CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - location.wsgi:application
