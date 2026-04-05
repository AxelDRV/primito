#!/bin/bash
echo "Instalando primito..."

pip install -r requirements.txt --break-system-packages

cp .primito.env.example ~/.primito.env

chmod +x primito.py
sudo ln -s "$(pwd)/primito.py" /usr/local/bin/primito

echo "Pon tu API key de aistudio.google.com en ~/.primito.env"
echo "Luego escribe 'primito' en la consola para chatear con primito"
