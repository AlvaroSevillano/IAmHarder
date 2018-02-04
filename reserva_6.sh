cd /home/ubuntu/IAmHarder
sleep 15
nohup python main.py alberto 0 >alberto.log 2>&1 &
sleep 5
nohup python main.py jonas 0 >jonas.log 2>&1 &