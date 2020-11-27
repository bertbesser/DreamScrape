FROM python:3

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /scrape
COPY scrape.sh .

CMD [ "./scrape.sh" ]
