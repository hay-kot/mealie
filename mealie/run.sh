#!/bin/sh

## Migrations
# TODO

## Web Server
caddy start --config ./Caddyfile

## Start API
uvicorn app:app --host 0.0.0.0 --port 9000