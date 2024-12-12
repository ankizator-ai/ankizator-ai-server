FROM python:3.13-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN apt-get update -y && \
    apt-get install -y netcat-traditional && \
    #pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]