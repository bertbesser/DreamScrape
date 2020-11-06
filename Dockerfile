FROM python:2

WORKDIR /scrape

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY extract.py .
RUN mkdir dreams

CMD [ "python", "extract.py" ]