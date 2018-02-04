cd /home/ubuntu/IAmHarder
sleep 15
nohup python main.py alvaro 0 >alvaro.log 2>&1 &
sleep 5
nohup python main.py andoni 0 >andoni.log 2>&1 &