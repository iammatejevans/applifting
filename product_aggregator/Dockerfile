FROM python:3.9-rc
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get -y install cron && apt-get install python
RUN pip install -r requirements.txt
ENV BASE_URL=https://applifting-python-excercise-ms.herokuapp.com/api/v1
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py init_admin

ADD crontab /etc/cron.d/root
RUN chmod +x /etc/cron.d/root
RUN chmod 0644 /etc/cron.d/root

RUN chmod u+x /app/job.sh
CMD /app/job.sh
