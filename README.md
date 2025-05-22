# Ankizator AI Server

## Description

This project is the backend server for Ankizator AI, a tool for generating Anki flashcards using AI.

## Docker Setup

There are several ways of running Ankizator in docker

### Build for the first time *(note the `true` case)*

```bash
RUN_MIGRATIONS=true docker compose up --build --watch
```

### Normal usage after build

```bash
docker compose up --watch
```

### Testing

```bash
docker compose --profile test up --watch
```

### Full testing *(note the `True` case)*

```bash
RUN_HEAVY_TESTS=True docker compose --profile test up --watch
```

## Production

To run the application in production, just run:

```bash
docker compose -f docker-compose.prod.yaml up --build -d
```

## Development

For local development, you can use the following steps:

1.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the migrations:**

    ```bash
    python manage.py migrate
    ```

4.  **Run the migrations:**

    ```bash
    python manage.py loaddata api/fixtures/collections.json
    ```

5.  **Start the development server:**

    ```bash
    python manage.py runserver
    ```
