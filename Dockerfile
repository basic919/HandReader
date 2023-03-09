FROM python:3.9-slim-buster
COPY . /usr/share/app
WORKDIR /usr/share/app
ENV PYTHONUNBUFFERED 1
RUN pip3 install -r /usr/share/app/requirements.txt
CMD ["python","app.py"]