FROM python:3.9.21-slim
LABEL authors="sen9a"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN apt-get update && apt-get install -y dfu-util && pip install poetry
RUN poetry install --no-root


COPY src ./src
COPY server.py ./
COPY README.md ./
COPY server.py /


ENTRYPOINT ["poetry", "run", "python3", "-u", "./server.py"]