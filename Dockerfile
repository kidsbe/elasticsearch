FROM elasticsearch:2.1.1
COPY elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml

RUN apt-get update && apt-get install -y \
                                         python-setuptools \
                                         build-essential \
                                         python-dev \
                                         duplicity ncftp

RUN easy_install pip
RUN pip install \
                tutum \
                netifaces

COPY docker-entrypoint.py /
ENTRYPOINT /docker-entrypoint.py
