Repo Root Promoter Bundle v1

Purpose:
- promote approved files from payload/repo_root/ into actual repo-root targets
- keep staging and promotion as separate governed steps
- log every promotion operation

Initial promotion policy:
- allow README.md
- allow architecture_map.md
- allow docs/**
- do NOT auto-promote .github/workflows/**

Usage:
- python install/repo_root_promoter.py

Expected flow:
1. bundle installs staged docs into payload/repo_root/
2. promoter copies approved files into repo root
3. workflow commits the change
