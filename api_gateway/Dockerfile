FROM python:alpine3.7

COPY . /api_gateway

WORKDIR /api_gateway

RUN pip install -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:/api_gateway"

EXPOSE 5003

CMD python ./api_gateway.py