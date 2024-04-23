#!/bin/sh

IMAGE_NAME=graph
CONTAINER_NAME=graph_container

docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME
docker rmi -f $IMAGE_NAME
