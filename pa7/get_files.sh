#!/bin/bash

echo "Getting files..."

wget -nv -O pa7.tgz https://www.classes.cs.uchicago.edu/archive/2020/fall/12100-1/pa-data/pa7.tgz

echo "Unbundling files..."

tar -xzf pa7.tgz

rm pa7.tgz



