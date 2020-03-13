echo "-> initialise git repo"
git init

echo "-> set git to follow tags on push"
git config push.followTags true

echo "-> configure git hooks"
pre-commit install -t pre-commit
pre-commit install -t pre-push

echo
echo "#################################################"
echo "REPO FULLY INITIALISED! You're set up to develop."
echo "#################################################"
