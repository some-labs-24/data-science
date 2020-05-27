FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install tweepy pandas python-dotenv emoji spacy gensim wordcloud

run python -m spacy download en_core_web_sm

COPY ./app /app

EXPOSE 80