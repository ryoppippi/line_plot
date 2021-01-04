#!/bin/bash
docker build -t line_plot . 
docker run -v $(pwd):/app --rm -it line_plot
