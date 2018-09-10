#!/usr/bin/env bash

NAWANO_PATH=$(dirname $(realpath $0))

cd ${NAWANO_PATH} && python3 -m nawano.cli

