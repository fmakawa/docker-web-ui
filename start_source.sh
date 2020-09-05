#!/bin/bash

# set environmental variables
source $PWD/variables.txt
export $(cut -d= -f1 $PWD/variables.txt)

# Run flask server
flask run