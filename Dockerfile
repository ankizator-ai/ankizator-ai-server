FROM python

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py loaddata api/fixtures/sources.json
CMD ["python", "manage.py", "runserver", "80"]

EXPOSE 80