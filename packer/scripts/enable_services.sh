echo "Enabling Services"

sudo systemctl daemon-reload

sudo systemctl enable mariadb
sudo systemctl enable webapp

echo "Completed enabling services"
echo "Template setup complete."