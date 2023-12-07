FROM python:3.8.10
WORKDIR /home/data
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY download_models.py download_models.py
CMD ["python3", "download_models.py"]