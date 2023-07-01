FROM python:3.9.7

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

RUN mkdir fastapi

WORKDIR /fastapi

COPY ./poetry.lock ./pyproject.toml ./ 

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-ansi


COPY . .

ENV PYTHONPATH=/app/:/usr/local/lib/python3.7/site-packages/

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]