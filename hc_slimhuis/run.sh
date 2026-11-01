#!/usr/bin/with-contenv bashio
export HC_URL="$(bashio::config 'url')"
export HC_TOKEN="$(bashio::config 'token')"
exec python3 /agent.py
