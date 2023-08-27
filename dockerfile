FROM python:3.10-bullseye

WORKDIR /opt/investment-portfolio
COPY . /opt/investment-portfolio
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
SHELL ["/bin/bash", "-c", ".env"] 
CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "8000", "src.api.main:app", "--reload" ]