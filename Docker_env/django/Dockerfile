FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /KataruAI_work

COPY requirements.txt /KataruAI_work/

# requirements.txtから必要なライブラリを一気にインストール
RUN pip install -r requirements.txt

COPY . /KataruAI_work/
