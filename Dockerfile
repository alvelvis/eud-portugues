FROM python:3.7

RUN apt-get update \
    && apt-get install -y opam wget m4 unzip librsvg2-bin curl bubblewrap

RUN opam init -y \
    && opam switch create 5.2.0 \
    && eval $(opam env) \
    && opam remote add grew "https://opam.grew.fr" \
    && opam install grew

COPY . /app
RUN pip install -r /app/requirements.txt
WORKDIR /app/flask
RUN gunicorn app:app