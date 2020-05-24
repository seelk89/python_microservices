FROM python:alpine3.7
RUN pip install --upgrade pip
COPY . /customer_api
WORKDIR /customer_api
RUN pip install -r requirements.txt
ENV PYTHONPATH="$PYTHONPATH:/customer_api"
EXPOSE 5001
CMD python ./customer_controller.py