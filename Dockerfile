FROM python:3

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

RUN addgroup --gid 1000 user
RUN adduser --gid 1000 --uid 1000 --gecos "" --disabled-password user

USER user

WORKDIR /scrape
COPY scrape.sh .

CMD [ "./scrape.sh" ]
