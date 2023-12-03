FROM python:3.8.10
WORKDIR .
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_DEBUG=True
ENV CUDA_VISIBLE_DEVICES=0
CMD ["python3", "main.py"]