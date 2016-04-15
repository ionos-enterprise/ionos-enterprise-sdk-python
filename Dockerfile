FROM python:latest

WORKDIR /usr/src

COPY requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY profitbricks /usr/src/profitbricks
COPY live_tests /usr/src/live_tests

USER nobody

CMD ["python","-m","unittest","discover","live_tests"]
