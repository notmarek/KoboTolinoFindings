#!/bin/bash
python getLatestUpdate.py
git add README.md
git commit -m "New version release, auto-update"
git push 