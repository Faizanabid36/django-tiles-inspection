#!/bin/sh

echo "**************************************************"
echo "CERAMIC TILES QUALITY INSPECTION(FYP)"
echo "**************************************************"


echo "Enter message to commit:"
read commitName

echo "**************************************************"
echo "Staging files"
git add .
echo "**************************************************"

echo "Committing Files.."
git commit -m "$commitName"
echo "**************************************************"

echo "Pulling from master branch"
git pull origin master
echo "**************************************************"

echo "Pushing to master branch"
git push origin master
echo "**************************************************"

echo "Done. Press Any Button"
read