FROM python:3.12
WORKDIR /app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
COPY run.py .
COPY src ./src
COPY run.py alembic.ini ./
CMD ["python3", "run.py"]