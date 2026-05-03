#!/bin/bash
set -e
echo "Running unit tests..."
python -m pytest tests/ -v --junitxml=test-results/results.xml
echo "Tests complete."
