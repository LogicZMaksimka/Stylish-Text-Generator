FROM python:3.8.10
COPY ./requirements.txt .
RUN pip install -r requirements.txt
WORKDIR .
COPY . .
RUN python3 download_models.py
EXPOSE 5000
ENV FLASK_DEBUG=True
ENV CUDA_VISIBLE_DEVICES=0
CMD ["python3", "main.py"]