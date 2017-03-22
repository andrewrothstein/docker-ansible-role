#!/usr/bin/env sh
dcb \
    --upstreamgroup andrewrothstein \
    --upstreamapp docker-ansible \
    --snippetsdir . \
    --snippet snippet.j2 \
    --writeall \
    --writesubdirs
