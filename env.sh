#!/bin/bash
DEFAULT_OS=${DEFAULT_OS:-"ubuntu_xenial"}

UPSTREAM_REGISTRY=${UPSTREAM_REGISTRY:-"https://docker.io"}
UPSTREAM_USER=${UPSTREAM_USER:-"andrewrothstein"}
UPSTREAM_APP=${UPSTREAM_APP:-"docker-ansible"}

TARGET_REGISTRY=${TARGET_REGISTRY:-"https://dockerio"}
TARGET_USER=${TARGET_USER:-"andrewrothstein"}
TARGET_APP=${TARGET_APP:-"docker-ansible-role"}
