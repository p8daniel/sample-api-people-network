FROM python:3.11

ENV PYTHONUNBUFFERED 1

ENV APP_HOME /source
WORKDIR $APP_HOME

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"
RUN poetry config virtualenvs.create false

# Install Deps
COPY poetry.lock pyproject.toml /source/
RUN poetry install --no-dev --extras "prod"

# Copy Application Code
COPY . ./
RUN poetry install --no-dev --extras "prod"

ENTRYPOINT ["python", "-m", "app"]