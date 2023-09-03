FROM python:slim-bullseye


WORKDIR /opt/investment-portfolio
COPY . /opt/investment-portfolio


# Dependecies
RUN apt update && apt upgrade -y && \
    apt-get install -y lsb-release && \
    apt install curl -y && \
    apt-get clean all
RUN bash install-odbc.sh
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "8000", "src.api.main:app", "--reload" ]