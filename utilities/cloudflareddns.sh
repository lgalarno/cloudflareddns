#!/bin/bash
UV_PATH=/home/USERNAME/.local/bin/
SCRIPT_PATH=/path/to/cloudflareddns/
API_TOKEN=
ZONE_ID=
LOG_FILE=/path/to/log/logs.txt
LOGGING=1

${UV_PATH}uv run --project ${SCRIPT_PATH} ${SCRIPT_PATH}/src/main.py -t ${API_TOKEN} -z ${ZONE_ID} -f ${LOG_FILE} -l ${LOGGING}
