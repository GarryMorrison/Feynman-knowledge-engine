#!/bin/sh

tr -cd '[:print:]\t\n' < "$1" > "clean-$1"
