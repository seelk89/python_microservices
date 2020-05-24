FROM python:alpine3.7

COPY . /product_api

WORKDIR /product_api

RUN pip install -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:/product_api"

EXPOSE 5002

CMD python ./product_controller.py