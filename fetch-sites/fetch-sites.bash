#!/bin/bash

netemFolder=$(realpath $(dirname $0)/..)
thisFolder=$netemFolder/fetch-sites
#webRoot=$netemFolder/webroot
webRoot=~/Downloads/measureData
urlFile=$netemFolder/config/urls.txt

mkdir -p $webRoot
# Save all sites
echo "Starting!"
echo "----------------"
for url in $(cat $urlFile)
do
    wget --no-check-certificate --page-requisites --html-extension --convert-links --span-hosts --no-clobber --tries=2 --timeout=10 --directory-prefix=$webRoot/$url --random-wait --wait 1 http://localhost/$url
done
echo "----------------"
echo ""
