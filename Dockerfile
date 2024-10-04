FROM python:3.11

WORKDIR /code

RUN apt update
COPY src/mnist/main.py /code/
COPY run.sh /code/run.sh

RUN pip install --no-cache-dir --upgrade git+https://github.com/DE32-3rd-team2/fastapi@0.0.1

CMD ["sh", "run.sh"]
