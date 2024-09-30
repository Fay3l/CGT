FROM python:3.10

WORKDIR /code

COPY classes.py /code

COPY api.py /code

COPY requirements.txt /code

COPY templates /code/templates
COPY template /code/template
COPY static /code/static
COPY images /code/images
COPY fonts /code/fonts
COPY upload /code/upload
COPY config.json /code
RUN pip3.10 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY app.py /code

CMD [ "python", "app.py" ]