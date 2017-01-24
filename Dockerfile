FROM python:latest

WORKDIR /usr/src

COPY . /usr/src

RUN pip install -r /usr/src/requirements.txt

USER nobody

CMD ["python", "-m", "unittest", "discover", "tests"]
