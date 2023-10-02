FROM python:3.11.5 AS builder
COPY requirements.txt .

RUN pip install --user -r requirements.txt

FROM python:3.11.5-slim
WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY ./src .

CMD ["python", "-u", "./main.py"]
