FROM python:3.7
COPY . /app
WORKDIR /app
RUN apt-get update -y
RUN apt-get install -y python3-dev
RUN pip install numpy==1.17.3
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["server.py"]