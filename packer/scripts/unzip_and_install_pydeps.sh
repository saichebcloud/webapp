echo "Unzipping source code"

cd /tmp
unzip Archive.zip

echo "Installing python dependencies"
sudo python3 -m pip install -r requirements.txt

echo "Installed all dependencies"

cd -