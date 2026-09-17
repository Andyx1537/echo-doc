#!/bin/sh
set -eu
if lsof -nP -iTCP:11434 -sTCP:LISTEN >/dev/null 2>&1; then
  echo '端口11434已占用；不接管其他进程。' >&2
  exit 1
fi
mkdir -p /Users/andy/Models/echo-local/models /Users/andy/Models/echo-local/runs /Users/andy/Models/echo-local/logs
export OLLAMA_MODELS=/Users/andy/Models/echo-local/models
export OLLAMA_HOST=127.0.0.1:11434
export OLLAMA_NO_CLOUD=1
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_CONTEXT_LENGTH=4096
exec /opt/homebrew/bin/ollama serve
