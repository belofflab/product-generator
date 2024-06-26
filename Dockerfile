FROM python:3.10

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /app

CMD ["uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "asyncio"]
EXPOSE 8000