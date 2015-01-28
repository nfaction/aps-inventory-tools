#!/bin/bash

usage() 
{
    echo "Usage: $0 [-h] <input file> "
    exit 2
}

if [ $# = 0 ]; then
	usage
	exit 0
fi
	
if [ $1 == "-h" ] || [ $1 == "--help" ]; then
    usage
    exit 0	
fi

inputFile=$1

cat inventory.csv | cut -f 3 -d ',' | tail -n +2 >> hostnames

# Find Mac hostnames

# Find Linux hostnames