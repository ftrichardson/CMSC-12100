#!/bin/bash

echo "Getting files..."

wget -nv -O lab7.tgz https://www.classes.cs.uchicago.edu/archive/2020/fall/12100-1/pa-data/lab7.tgz

echo "Unbundling files..."

tar -xzf lab7.tgz

rm lab7.tgz



