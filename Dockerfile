FROM python:3.8-slim

RUN export DEBIAN_FRONTEND=noninteractive && apt-get update \
  && apt-get install --no-install-recommends --no-install-suggests --assume-yes \
    curl \
    unzip \
    gnupg \
    xvfb \
    wget
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# # set display port to avoid crash
ENV DISPLAY=:99

# setup env
WORKDIR /usr/src/app
ADD ./Dockerfile /usr/src/app/Dockerfile
ADD ./run.py /usr/src/app/run.py
ADD ./requirements.txt /usr/src/app/requirements.txt
ADD ./script /usr/src/app/script
ADD ./bin /usr/src/app/bin
ADD ./conf /usr/src/app/conf

RUN mkdir -p /usr/src/app/bin/linux
RUN cp /usr/local/bin/chromedriver /usr/src/app/bin/Linux/chromedriver

# upgrade pip
RUN pip install --upgrade pip

# install requirements
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
CMD [ "python", "/usr/src/app/run.py"]
