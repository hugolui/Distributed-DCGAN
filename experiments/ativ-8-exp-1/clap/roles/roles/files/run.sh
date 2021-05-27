#!/bin/bash
cp 172* Distributed-DCGAN/
cp ip.py Distributed-DCGAN/
cd Distributed-DCGAN/ 
ip_master=$(cat *.master)
ip=$(hostname | cut -d - -f 2,3,4,5 | sed 's/-/./g')
python3 ip.py
if [ "$ip_master" = "$ip" ]; then
    rank=0
else
    rank=$(grep "$ip" rank_number | cut -d ' ' -f 1)
fi
sudo docker run --env OMP_NUM_THREADS=1 --rm --network=host -v=$(pwd):/root dist_dcgan:latest python -m torch.distributed.launch --nproc_per_node=1 --nnodes=$1 --node_rank=$rank --master_addr="$ip_master" --master_port=1234 dist_dcgan.py --dataset cifar10 --dataroot ./cifar10 --num_epochs 1 --batch_size 32