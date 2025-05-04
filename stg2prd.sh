#!/bin/bash
git checkout prd
git merge --squash stg
git commit -m "merged with stg"
git push
git checkout dev