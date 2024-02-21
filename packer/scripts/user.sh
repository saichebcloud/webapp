echo "Creating group and user csye6225"

sudo groupadd csye6225

sudo useradd -s /usr/sbin/nologin -g csye6225 csye6225

echo "Finished creating user"