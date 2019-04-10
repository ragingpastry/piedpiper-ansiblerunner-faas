FROM python:3.7-alpine

# Alternatively use ADD https:// (which will not be cached by Docker builder)
RUN apk --no-cache add curl linux-headers gcc musl-dev libffi-dev openssl-dev make git \
    && echo "Pulling watchdog binary from Github." \
    && curl -sSLf https://github.com/openfaas-incubator/of-watchdog/releases/download/0.4.6/of-watchdog > /usr/bin/fwatchdog \
	&& curl -sSLf https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz | tar -xzvf - -C /tmp/ \
	&& mv /tmp/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc /usr/bin/ \
    && chmod +x /usr/bin/fwatchdog \
    && apk del curl --no-cache

RUN apk --no-cache add musl-dev gcc make

WORKDIR /root/

COPY requirements.txt   .
RUN pip install -r requirements.txt

RUN mkdir -p function
RUN touch ./function/__init__.py
WORKDIR /root/function/
COPY function/requirements.txt	.
RUN pip install -r requirements.txt

WORKDIR /root/
COPY function           function

COPY index.py           .
ENV fprocess="gunicorn index:app --worker-class gevent --bind 127.0.0.1:5000"

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
