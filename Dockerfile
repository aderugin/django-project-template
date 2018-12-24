FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install uuid-dev
{% if XAPIAN %}
RUN apt-get install -y python-xapian
RUN cd /tmp \
    && wget http://oligarchy.co.uk/xapian/1.2.18/xapian-core-1.2.18.tar.xz \
    && tar xpvf xapian-core-1.2.18.tar.xz \
    && wget http://oligarchy.co.uk/xapian/1.2.18/xapian-bindings-1.2.18.tar.xz \
    && tar xpvf xapian-bindings-1.2.18.tar.xz \
    && cd xapian-core-1.2.18 \
    && ./configure \
    && make \
    && make install \
    && cd /tmp/xapian-bindings-1.2.18 \
    && ./configure --with-python \
    && make \
    && make install
{% endif %}
ARG ENV=develop

RUN mkdir -p /webapp
COPY ./requirements /webapp/requirements
WORKDIR /webapp

RUN pip install --upgrade pip && \
    pip install -r requirements/${ENV}.txt && \
    pip install ipdb
