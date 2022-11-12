FROM python:3.9
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN python3.9 -m pip install -r /app/requirements.txt
RUN python3.9 -m nltk.downloader stopwords
RUN python3.9 -m spacy download en_core_web_sm
COPY . /app
EXPOSE $PORT
CMD ["waitress-serve", "server:app"]