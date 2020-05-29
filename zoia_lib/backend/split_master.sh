#!/bin/bash
i=0
for f in *; do
  d=dir_$(printf % 03d $((i / 64 + 1)))
  mkdir -p "$d"
  mv "$f" "$d"
  ((i++))
done
