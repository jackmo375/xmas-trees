#!/usr/bin/env bash

starting_file=$(ls -1 results | grep -E '^[0-9]+' | sort -n | tail -1)

echo "./results/$starting_file"

until ./main.py --start ./results/$starting_file; do
    echo "Command failed — retrying..."
    sleep 1
done