#!/bin/sh

echo "Enter message to commit:"
read commitName

echo "Staging files"
git add .

echo "Committing Files.."
git commit -m "$commitName"

echo "Pulling from master branch"
git pull origin master

echo "Pushing to master branch"
git push origin master

echo "Done. Press Any Button"
read