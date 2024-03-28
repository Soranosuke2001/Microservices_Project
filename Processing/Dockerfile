FROM python:latest

LABEL maintainer="sschlegel1@my.bcit.ca"

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y sqlite3

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8090

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
