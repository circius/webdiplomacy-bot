FROM python:slim

WORKDIR dipbot/

ADD ./ ./

RUN pip install -e ./

CMD dipbot daemon
       
