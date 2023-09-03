FROM python:3.10

COPY . /app
WORKDIR /app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 wget -y
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR /app/challenge
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]