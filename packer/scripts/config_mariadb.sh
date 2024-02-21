echo "Starting and configuring mariadb"
sudo systemctl start mariadb

sudo mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'saisid123'; CREATE DATABASE TEST;"
