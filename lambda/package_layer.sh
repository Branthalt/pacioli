#!/bin/bash

name=pacioli.zip

mkdir -p zipstage/python/
cp -a layer/* zipstage/python/

find zipstage/ -name *__pycache__ -type d -exec rm -rf {} \;

cd zipstage
zip -r ../pacioli.zip *
cd ..
rm -rf zipstage
