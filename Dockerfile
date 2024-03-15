FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 2323

ENV FLASK_APP=app.py

CMD ["python", "app.py"]