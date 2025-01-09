FROM orthancteam/orthanc:latest-full

COPY requirements.txt /run/secrets/requirements.txt

RUN apt-get update && apt-get install -y \
    python3-pip \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --break-system-packages -r /run/secrets/requirements.txt

RUN wget https://orthanc.uclouvain.be/downloads/linux-standard-base/orthanc-ohif/1.4/libOrthancOHIF.so --output-document /usr/share/orthanc/plugins/libOrthancOHIF.so

COPY orthanc.json /run/secrets/orthanc.json
COPY dicomweb.json /run/secrets/dicomweb.json
COPY credentials.json /run/secrets/credentials.json
COPY postgresql.json /run/secrets/postgresql.json
COPY worklists.json /run/secrets/worklists.json
COPY python.json /run/secrets/python.json