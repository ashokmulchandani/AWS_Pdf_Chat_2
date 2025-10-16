FROM python:3.12-slim

WORKDIR /app

COPY requirements_user.txt .

RUN pip install --no-cache-dir -r requirements_user.txt

COPY . .

ENV AWS_DEFAULT_REGION=us-east-1

EXPOSE 8502

CMD ["streamlit", "run", "auser.py", "--server.address", "0.0.0.0", "--server.port", "8502"]