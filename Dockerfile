FROM python:3.11

RUN mkdir /home/evaluator

WORKDIR /home/evaluator

RUN apt-get update

COPY min_req.txt /home/evaluator/

RUN python -m pip install --upgrade pip
RUN python -m pip install -r min_req.txt


COPY Evaluation.py main.py /home/evaluator/

ENTRYPOINT ["python3", "main.py"]