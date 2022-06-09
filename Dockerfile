FROM python:3.9-slim

MAINTAINER Wang Poh Peng "wangpp1@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip

COPY ./requirements.txt src/requirements.txt
WORKDIR /src
RUN pip3 install -r requirements.txt
COPY ./scheduler.py src/scheduler.py
ENTRYPOINT [ "python3" ]
CMD [ "scheduler.py" ]
EXPOSE 5001