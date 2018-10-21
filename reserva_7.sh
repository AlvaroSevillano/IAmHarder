cd /home/ubuntu/IAmHarder
sleep 15
nohup python main.py jelen 0 >jelen.log 2>&1 &
sleep 5
nohup python main.py lucia 0 >lucia.log 2>&1 &
sleep 5
nohup python main.py leixuri 0 >leixuri.log 2>&1 &
