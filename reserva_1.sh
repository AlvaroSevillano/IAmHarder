cd /home/ubuntu/IAmHarder
sleep 15
nohup python main.py leixuri 0 >leixuri.log 2>&1 &
sleep 5
nohup python main.py antonio 0 >antonio.log 2>&1 &
