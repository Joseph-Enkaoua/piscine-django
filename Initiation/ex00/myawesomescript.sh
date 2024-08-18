#!/bin/bash

curl -sI -L $1 | grep -m 1 "Location" | cut -d' ' -f2-