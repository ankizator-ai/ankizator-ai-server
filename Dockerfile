FROM python:3.13-alpine

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /var/cache/ankizator-ai && chmod 770 /var/cache/ankizator-ai

RUN apk update && apk add netcat-openbsd

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]