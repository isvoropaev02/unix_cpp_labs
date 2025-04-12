#!/bin/bash
git checkout stg
git merge dev
git commit -m "merged with dev"
git push
git checkout dev