FROM python:3.7

RUN apt-get update \
    && apt-get install -y \
        build-essential \
        git \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev \
        libopencv-* \
        xterm \
    && rm -rf /var/lib/apt/lists/*

COPY req.txt .
RUN pip install --upgrade pip
RUN pip install -r req.txt

WORKDIR /app

COPY /app .
