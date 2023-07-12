# No need for history of commits :)

if [[ -n $(git status --porcelain) ]]; then
    git config user.name '-'
    git config user.email '-'
    git checkout --orphan temp
    git add -A
    git commit -am "Update sieve"
    git branch -D main
    git branch -m main
    git push -f origin main
else
    echo "There are no changes in the repository"
fi