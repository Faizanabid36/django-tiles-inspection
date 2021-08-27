#!/bin/sh

echo "Enter message to commit:"
read commitName
git add .
echo "Staging files"
git commit -m "$commitName"
echo "Committing Files.."
git pull origin master
echo "Pulling from master branch"
git push origin master
echo "Pushing to master branch"
echo "Done. Press Any Button"
read