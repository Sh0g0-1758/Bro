sudo apt install softflowd
sudo softflowd -i wlo1 -n 127.0.0.1:9995
mkdir netflow
sudo nfcapd -D -w ./netflow -p 9995
echo "Data collection started, please check netflow folder for data after five minutes"
