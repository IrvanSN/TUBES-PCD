FROM python:latest

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install Flask

RUN pip install Pillow

RUN pip install numpy

COPY . /app

ENTRYPOINT [ "python" ]

CMD ["app.py"]