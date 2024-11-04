#!/bin/bash

source /opt/digimeter/venv/bin/activate

set -a
source /opt/digimeter/environment.env
set +a

python /opt/digimeter/read_data.py