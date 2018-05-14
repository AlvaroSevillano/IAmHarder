cd /home/ubuntu/IAmHarder
sleep 15
nohup python main.py jota 0 >jota.log 2>&1 &
sleep 5
nohup python main.py horacio 0 >horacio.log 2>&1 &
