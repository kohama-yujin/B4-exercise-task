#!/bin/bash

for ((i=-180; i<=180; i+=10)); do
    python3 omni_to_persp_converter.py "input/omni.jpg" $i 0 0 "size" 2000 1800
done