FROM python

WORKDIR /backend

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:backend", "--host", "0.0.0.0", "--port", "8000", "--reload"]


