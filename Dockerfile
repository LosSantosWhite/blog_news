FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements-docker.txt /code/
RUN pip install -r requirements-docker.txt
COPY . /code/