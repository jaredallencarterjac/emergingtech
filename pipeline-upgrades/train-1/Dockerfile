FROM python:3.7-slim

WORKDIR /app

RUN pip install -U scikit-learn numpy

COPY train-1.py ./train-1.py

ENTRYPOINT [ "python", "train-1.py" ]
