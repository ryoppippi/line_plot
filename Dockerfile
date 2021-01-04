FROM python:3.8-slim
RUN pip install \
    pandas \
    plotly \
    click
WORKDIR /app
CMD ["python3", "plot.py", "-t", "bar", "-i", "line.txt"]
