FROM python:3.9
COPY . /app
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN python3.9 -m pip install -r /app/requirements.txt
RUN python3.9 -m nltk.downloader stopwords
EXPOSE $PORT
CMD waitress-serve --port=$PORT server:app
