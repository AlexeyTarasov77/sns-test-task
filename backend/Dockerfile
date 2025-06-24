FROM python:3.12.8-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME=/opt/poetry \
    PATH=${POETRY_HOME}/bin:${PATH} \ 
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml poetry.lock .

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-root --without=dev

RUN apt update && apt install -y libpq-dev build-essential

COPY . .

RUN adduser --disabled-password www

RUN chown -R www ./

USER www

ENTRYPOINT [ "poetry", "run" ]

CMD ["python", "src/main.py"]

