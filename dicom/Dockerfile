FROM jodogne/orthanc-plugins:1.5.6

WORKDIR /app/dicom

RUN apt-get update && apt-get -y install python3 python3-pip curl postgresql-client

COPY ./requirements.txt /app/dicom/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r /app/dicom/requirements.txt

COPY . /app/dicom

ENTRYPOINT ["/bin/bash", "start.sh"]
