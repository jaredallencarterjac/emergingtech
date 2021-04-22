FROM python:3.7-slim

WORKDIR /app

RUN pip install -U scikit-learn numpy

COPY test-1.py ./test-1.py

ENTRYPOINT [ "python", "test-1.py" ]
