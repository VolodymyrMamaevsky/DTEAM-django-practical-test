FROM python:3.12

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

RUN poetry run playwright install-deps && \
    poetry run playwright install

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
