#!/bin/bash

awk 'FNR==1 && NR!=1 {next} {print}' $(ls results/*-tree-configuration.csv | sort -V) > results/full_solution.csv