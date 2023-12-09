FROM python:3.8.10
WORKDIR /home/text_generator
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY main.py main.py
CMD ["python3", "main.py"]