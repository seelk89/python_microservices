FROM python:alpine3.7
RUN pip install --upgrade pip
COPY . /order_api
WORKDIR /order_api
RUN pip install -r requirements.txt
ENV PYTHONPATH="$PYTHONPATH:/order_api"
EXPOSE 5000
CMD python ./order_controller.py