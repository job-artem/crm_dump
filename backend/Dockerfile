FROM python:3.11-slim-buster

WORKDIR ./backend
RUN apt update && apt-get install -y postgresql-client make && apt install -y curl && rm -rf /var/cache/apt
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN chmod +x backend.sh
RUN pip3 install -r requirements.txt
#ENTRYPOINT ["./backend.sh"]

