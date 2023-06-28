FROM python:3.10
WORKDIR /app
COPY requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY src/ /app
CMD ["python", "app.py"]
