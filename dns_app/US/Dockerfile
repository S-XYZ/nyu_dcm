FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install flask requests

EXPOSE 8080

CMD ["python", "us_app.py"]