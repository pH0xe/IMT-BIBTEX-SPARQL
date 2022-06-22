#!/bin/bash

ARG_1=$1

if [ $# -gt 1 ]
then
	echo "Too many arguments (expected at most one argument)"
	echo "Run $0 --help to get the list of possible arguments"
	exit
elif [ $# -eq 1 ] && [ "$ARG_1" == "--help" ]
then
	echo "Launch both the back-end and the front-end of the application"
	echo "Possible arguments"
	echo "  --help: see the list of possible arguments"
	echo "  --quickly: skip re-build phases"
	exit
elif [ $# -eq 1 ] && [ "$ARG_1" != "--quickly" ]
then
	echo "Unknown argument: $ARG_1"
	echo "Run $0 --help to get the list of possible arguments"
	exit
fi

function start_backend {
	if [ "$ARG_1" != "--quickly" ]
	then
		PARAMS="--build --remove-orphans"
	else
		PARAMS="--no-recreate"
	fi

	sudo docker-compose up --detach $PARAMS
}

function start_frontend {
	(
		cd webapp

		if [ "$ARG_1" != "--quickly" ]
		then
			rm -rf node_modules
		fi

		yarn install
		yarn dev
	)
}

function stop {
	sudo docker-compose stop
}

trap stop EXIT

start_backend
start_frontend
