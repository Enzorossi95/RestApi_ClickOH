FROM python:3.8

# Install base dependencies
RUN apt-get update && apt-get install -y -q --no-install-recommends \
        apt-transport-https \
        binutils \
        build-essential \
        ca-certificates \
        curl \
        gdal-bin \
        git \
        libproj-dev \
        libssl-dev \
        wget \
    && rm -rf /var/lib/apt/lists/*


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements/requirements.txt /usr/src/app/


RUN pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh /usr/src/app


COPY . /usr/src/app

RUN mkdir -p /usr/src/app/src/static/

EXPOSE 8000
WORKDIR /usr/src/app/src
ENTRYPOINT ["sh", "../docker-entrypoint.sh"]