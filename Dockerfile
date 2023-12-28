FROM python:3.12-slim
WORKDIR /app
COPY ./requirements.lock .
RUN sed '/-e/d' requirements.lock > requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app
CMD ["python3", "plot.py", "-t", "bar", "-i", "line.txt"]
