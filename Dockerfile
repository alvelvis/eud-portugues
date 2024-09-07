FROM python:3.7

RUN apt-get update \
    && apt-get install -y opam wget m4 unzip librsvg2-bin curl bubblewrap

RUN opam init -y \
    && opam switch create 5.2.0 -y \
    && eval $(opam env) \
    && opam remote add grew "https://opam.grew.fr" -y \
    && opam install grew -y

RUN opam update && opam upgrade && eval $(opam env)

COPY . /app
RUN pip install -r /app/requirements.txt
WORKDIR /app/flask
EXPOSE 8000
CMD gunicorn app:app