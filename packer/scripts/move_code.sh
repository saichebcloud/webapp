echo "Moving source code"
sudo unzip /tmp/Archive.zip -d /home/csye6225
sudo mv /tmp/.env /home/csye6225
sudo mv /tmp/webapp.service /etc/systemd/system/

echo "code staged succesfully"