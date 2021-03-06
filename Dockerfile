FROM python:3.9-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY run.py .

CMD ["python", "run.py"]