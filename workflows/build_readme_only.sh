# !/bin/zsh
git reset --hard HEAD;
git clean -fd;
git status;
git pull --rebase origin main;
python3 workflows/build_readme_only.py; 
git add images; 
git add README.md; 
git commit -m "🤖-local [build_readme_only.py] $(date '+%Y-%m-%d-%H%M')";
git pull --rebase origin main;
git push origin main;

