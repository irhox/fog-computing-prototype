FROM python:3.11.9

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 1883

CMD ["python", "src/main.py"]
