FROM python:3.13-alpine

RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN chmod +x /app/entrypoint.sh

RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /var/cache/ankizator-ai && chmod 770 /var/cache/ankizator-ai

RUN apk update && apk add netcat-openbsd

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]