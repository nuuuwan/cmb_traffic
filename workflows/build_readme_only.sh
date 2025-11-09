# !/bin/zsh
MSG="🤖-local [build_readme_only.py] $(date '+%Y-%m-%d-%H%M')"
echo $MSG
python3 workflows/build_readme_only.py ; 
git add images; 
git add README.md; 
git commit -m $MSG
echo '---"
