echo "Changing ownership to csye6225"
sudo chown -R csye6225:csye6225 /home/csye6225
sudo touch /var/log/webapp.log
sudo chown csye6225:csye6225 /var/log/webapp.log
echo "Ownership modified"
