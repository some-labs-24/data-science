FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install tweepy pandas python-dotenv emoji spacy gensim wordcloud psycopg2-binary

RUN python -m spacy download en_core_web_sm

ENV TIMEOUT=36000

ENV GRACEFUL_TIMEOUT=36000

COPY ./app /app

EXPOSE 80