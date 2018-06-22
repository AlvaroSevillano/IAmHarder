cd /home/ubuntu/IAmHarder
sleep 15
nohup python main.py leixuri 0 >leixuri.log 2>&1 &
sleep 5
nohup python main.py jaime 0 >jaime.log 2>&1 &
