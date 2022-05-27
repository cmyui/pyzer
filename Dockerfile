FROM python:3.9

COPY pyzer/ /pyzer

# RUN pip install -U pip setuptools

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY scripts/ /scripts
RUN chmod 755 /scripts/*

CMD ["/scripts/start_server.sh"]
