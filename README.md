# Ankizator AI Server

## Description

This project is the backend server for Ankizator AI, a tool for generating Anki flashcards using AI.

## Docker Setup

To run the application using Docker, follow these steps:

1.  **Build the Docker image:**

    ```bash
    docker compose build
    ```

2.  **Run the Docker containers in development mode:**

    ```bash
    docker compose up --watch
    ```

3.  **Run database migrations:**

    ```bash
    docker compose run web python manage.py migrate
    ```

## Production

To run the application in production, follow these steps:

1.  **Build the Docker image:**

    ```bash
    docker compose -f docker-compose.prod.yaml up --build
    ```

2.  **Run the Docker containers:**

    ```bash
    docker compose -f docker-compose.prod.yaml up -d
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

4.  **Start the development server:**

    ```bash
    python manage.py runserver --watch
    ```
