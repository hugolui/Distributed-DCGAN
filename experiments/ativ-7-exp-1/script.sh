#!/bin/bash
git clone -b ativ-7-exp-1 https://github.com/hugolui/Distributed-DCGAN.git
cd Distributed-DCGAN/
mkdir cifar10 && cd cifar10
wget --no-check-certificate https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
tar -xvf cifar-10-python.tar.gz
cd ..
sudo docker build -t dist_dcgan .
