# Dockerfile

FROM python:3.8.5-buster

# copy source and install dependencies
RUN mkdir -p /dsktool
WORKDIR /dsktool
COPY . /dsktool
RUN pip install --no-cache-dir -r requirements.txt

RUN ls -a

# start server
EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "DSKTOOL.wsgi:application"]
