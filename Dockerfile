FROM python:3.8-alpine

COPY requirements.txt requirements.txt

ENV PATH="/venv/bin:$PATH"
RUN python -m venv /venv
RUN pip install -r requirements.txt


RUN mkdir /usr/src/da-react-challenge
COPY . /usr/src/da-react-challenge/

EXPOSE 8000
WORKDIR /usr/src/da-react-challenge
RUN ["chmod", "+x", "/usr/src/da-react-challenge/docker-config/entrypoint.sh"]

ENTRYPOINT ["sh", "docker-config/entrypoint.sh"]