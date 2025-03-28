#!/bin/bash
dt=$(date +%F_%T)
git checkout stg
git merge dev
git commit -m "merged with dev"
git tag "$dt"
git push
