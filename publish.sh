#!/bin/sh
##################################
# Function:
# Author: Chen Bear<chenll7@outlook.com>
##################################
cd "$(git worktree list | awk '$3=="[master]"{print $1}')"
git merge --no-ff --no-edit dev
