FROM python:3.9

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
ADD /app /app

ENV FLASK_APP=server
EXPOSE 5000

ENTRYPOINT [ "flask", "run", "--host=0.0.0.0"]