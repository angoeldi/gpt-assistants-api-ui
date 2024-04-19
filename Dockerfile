FROM python:3.10-slim-buster
WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN apt update && apt -y upgrade
RUN apt install -y ffmpeg
RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
# Add a command to update the lock file
RUN poetry lock --no-update
RUN poetry install

EXPOSE 7888
EXPOSE 8501

COPY . /app

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
