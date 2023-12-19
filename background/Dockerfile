FROM python:3.10

#
RUN mkdir -p /var/background

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./ /code/

#
CMD ["python", "background.py"]
