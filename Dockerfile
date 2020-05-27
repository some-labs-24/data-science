FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install tweepy pandas python-dotenv emoji spacy

COPY ./app /app

EXPOSE 80