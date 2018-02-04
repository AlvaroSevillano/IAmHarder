cd /home/ubuntu/IAmHarder
sleep 15
nohup python main.py javi 0 >javi.log 2>&1 &
sleep 5
nohup python main.py laura 0 >laura.log 2>&1 &