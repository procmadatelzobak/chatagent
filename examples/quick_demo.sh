#!/usr/bin/env bash
# Run a minimal demo using the mock LLM and a simple scenario.
set -e
python examples/quick_demo.py
chatsim run --scenario examples/simple.json >/dev/null
