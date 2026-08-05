FROM python:3.10.15-alpine3.20

LABEL org.opencontainers.image.authors="cesar.sanchez@conext.com.ve"

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV TZ=America/Caracas
RUN cp /usr/share/zoneinfo/America/Caracas /etc/localtime

# Forzar a Python a no usar un buffer de memoria para los logs (esencial en Docker)
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]