FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN pip install python-dotenv

ENV PATH="/app/.env:${PATH}"

CMD ["streamlit", "run", "app.py"]
