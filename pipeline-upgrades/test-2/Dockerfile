FROM python:3.7-slim

WORKDIR /app

RUN pip install -U scikit-learn numpy

COPY test-2.py ./test-2.py

ENTRYPOINT [ "python", "test-2.py" ]
