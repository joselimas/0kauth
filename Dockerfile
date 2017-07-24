FROM ubuntu:latest
RUN apt-get update -y --fix-missing
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install Flask, pycrypto
COPY . /app
WORKDIR /app
ENTRYPOINT ["sh"]
CMD ["python auth/server.py&"]
CMD ["run.sh"]
