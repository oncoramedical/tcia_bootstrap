# TCIA Bootstrap

## Introduction

A small docker set up to pull TCIA collections into a DICOM server.

## Pre-requisites

Make sure that the following are installed:

1. [Docker](https://docs.docker.com/v17.12/install/)
2. [Docker compose](https://docs.docker.com/compose/install/)

## Directions

### TL;DR

```
docker-compose up
bash bootstrap.sh -h
bash bootstrap.sh -c <COLLECTION>
```


### Running containers

Start the docker containers using the following:

```sh
docker-compose up
```

Running this command for the first time will build the DICOM server image.
The resulting image will then be used when starting up containers.

To stop the containers either `Ctrl-C` or run the following:

```sh
docker-compose stop
```

### Load collections

To see a full list of available collections run `bash bootstraph.sh -h`. There are two
ways to load these [collections](https://www.cancerimagingarchive.net):

1. Specify the collection as the `COLLECTION` environment variable in `docker-compose.yml`
   for the DICOM container, restart: `docker-compose restart dicom`, and
   run `bash bootstrap.sh`

2. Supply a collection name: `bash bootstrap.sh --collection <COLLECTION>`.

### A few things to note

- Loading a collection may take awhile
  - You can limit the number of series loaded using `--limit <NUMBER>`.
- Multiple collections can be loaded
  - Just run the instructions for loading collections with new collection names
- Loaded studies are accessible via DICOM messages or requests sent the DICOM container
  [REST API](https://api.orthanc-server.com)
  - You can also view the studies via the [Orthanc web explorer](http://localhost:8042/)
