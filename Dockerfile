FROM python:3.12

# Set the working directory
WORKDIR /app

COPY requirements.txt /app
COPY banking_api /app/banking_api

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

CMD ["python", "banking_api/src/main.py"]