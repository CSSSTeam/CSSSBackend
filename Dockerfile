FROM python
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . .

ENV PORT = 8000
EXPOSE 8000
