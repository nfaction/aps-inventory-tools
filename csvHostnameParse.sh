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

# grab hostnames
cat inventory.csv | cut -f 3 -d ',' | tail -n +2 

# Find Mac hostnames
(cat inventory.csv | cut -f 3,16 -d ',' | tail -n +2 | grep -i "10.*" | grep -v -i "Ubuntu") >> MacHosts

# Find Linux hostnames
cat inventory.csv | cut -f 3,16 -d ',' | tail -n +2 | grep -i "10.*" | grep -v -f MacHosts >> LinuxHosts