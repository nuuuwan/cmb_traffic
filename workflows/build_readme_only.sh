# !/bin/zsh

python3 workflows/build_readme_only.py ; 
git add images; 
git add README.md; 
git commit -m "Ran build_readme_only.py locally"
