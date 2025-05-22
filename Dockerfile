FROM python:3.13-alpine

RUN mkdir /app
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
RUN pip install --upgrade pip 
COPY requirements.txt  /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]