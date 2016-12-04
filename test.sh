#!/bin/bash
set -xe

. env.sh
OS=${1:-${DEFAULT_OS}}
TARGET_CONTAINER=$TARGET_USER/${TARGET_APP}_$OS
docker images $TARGET_CONTAINER
