FROM python:2.7.9

RUN pip install MySQL-python \
    && pip install gunicorn \
    && pip install newrelic



RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app



COPY ./requirements.txt /usr/src/app/

RUN pip install  -r requirements.txt

ADD . /usr/src/app

ENV PROD TRUE
ENV WEB_CONCURRENCY 4
ENV NEW_RELIC_CONFIG_FILE /usr/src/app/newrelic.ini

EXPOSE 3000

CMD [ "newrelic-admin","run-program","gunicorn","-k","gevent","--max-requests","3000","--access-logfile","-", "--error-logfile","-","-b","0.0.0.0:3000","sense_server.run_app:app"  ]
