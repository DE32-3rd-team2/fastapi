FROM python:3.11

WORKDIR /code

COPY src/age_pred/main.py /code/

RUN pip install --no-cache-dir --upgrade git+https://github.com/DE32-3rd-team2/fastapi@0.2.3

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
