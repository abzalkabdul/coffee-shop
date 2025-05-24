FROM python:3.13

WORKDIR /app

RUN apt-get update && pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN pip install --upgrade pip poetry 
RUN poetry config virtualenvs.create false 
RUN poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0:8000"]



