cd /home/ubuntu/IAmHarder
sleep 15
nohup python main.py risto 0 >risto.log 2>&1 &
sleep 5
nohup python main.py blas 0 >blas.log 2>&1 &