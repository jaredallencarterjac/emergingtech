FROM python:3.7-slim

WORKDIR /app

RUN pip install -U scikit-learn numpy

COPY train-2.py ./train-2.py

ENTRYPOINT [ "python", "train-2.py" ]
