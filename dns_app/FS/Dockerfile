FROM python:3.9

WORKDIR /app

COPY fs_app.py /app

RUN pip install flask

EXPOSE 9090

CMD ["python", "fs_app.py"]