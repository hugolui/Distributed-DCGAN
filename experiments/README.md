Para realizar a execução da DCGAN no Amazon web service elastic computing 2 (AWS EC2) foi realizado os seguintes passos:

1) No serviço EC2, acessa-se a opção "Launch instance" e depois definiu-se a imagem como "Ubuntu Server 20.04 LTS (HVM), SSD Volume Type".
2) Escolheu-se a máquina virtual "m5.large" (2 CPUs e 8GB de RAM) com 1 instância.
3) Definiu-se um storage com 16 GB do tipo "General Purpose SSD (gp2)".
4) Configurou-se as regras de acesso as máquinas virtuais da seguinte forma, Type: SSH; Protocol: TCP; Port range: 22; Source: anywhere. Desse modo, o usuário possui acesso as máquinas virtuais via SSH.
5) Depois de criado a imagem, connectou-se a máquina virtual via SSH e executou-se os seguintes commandos:
  
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io

git clone https://github.com/eborin/Distributed-DCGAN.git

cd Distributed-DCGAN

mkdir cifar10 && cd cifar10
wget --no-check-certificate https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
tar -xvf cifar-10-python.tar.gz
cd ..

sudo docker build -t dist_dcgan .
  
6) Uma vez tudo configurado, criou-se uma imagem base a partir da máquina virtual obtida pelos passos anteriores.
7) Executou-se os passos 1 a 4 novamente ("Launch instance"), no entanto no passo 1, escolheremos a image base recém criada e no passo 2, utilizaremos 4 instâncias ao invés de uma, além disso, adicionaremos um "placement group" para obter um melhor desempenho de rede.
8) Criou-se um grupo de segurança com as seguintes regras, Type: All trafic; Protocol: ALL. Dessa maneira todas as portas entre as máquinas pertencentes a esse grupo estão liberadas, permitindo assim a comunicação entre elas.
9) As 4 máquinas virtuais são acessadas na máquina local via SSH utilizando um terminal para cada instância. Uma dessas quatro instâncias será a master, onde será necessário obter o seu número do "Private IPv4 addresses".
10) Para cada terminal, executa-se o seguinte comando:
  Onde o parâmetro "--master_addr" deve ser igual ao número do "Private IPv4 addresses" da instância escolhida como master, no exemplo abaixo temos --master_addr="172.31.71.56".
  
  Terminal 1:
  sudo docker run --env OMP_NUM_THREADS=2 --rm --network=host -p 1234:1234  -v=$(pwd):/root dist_dcgan:latest python -m torch.distributed.launch --nproc_per_node=2 --nnodes=4 --node_rank=0 --master_addr="172.31.71.56" --master_port=1234 dist_dcgan.py --dataset cifar10 --dataroot ./cifar10   --num_epochs 1 --batch_size 16 --max_workers 2
  
  Terminal 2:
  sudo docker run --env OMP_NUM_THREADS=2 --rm --network=host -p 1234:1234  -v=$(pwd):/root dist_dcgan:latest python -m torch.distributed.launch --nproc_per_node=2 --nnodes=4 --node_rank=1 --master_addr="172.31.71.56" --master_port=1234 dist_dcgan.py --dataset cifar10 --dataroot ./cifar10  --num_epochs 1 --batch_size 16 --max_workers 2
  
  Terminal 3:
  sudo docker run --env OMP_NUM_THREADS=2 --rm --network=host -p 1234:1234  -v=$(pwd):/root dist_dcgan:latest python -m torch.distributed.launch --nproc_per_node=2 --nnodes=4 --node_rank=2 --master_addr="172.31.71.56" --master_port=1234 dist_dcgan.py --dataset cifar10 --dataroot ./cifar10  --num_epochs 1 --batch_size 16 --max_workers 2
  
  Terminal 4:
  sudo docker run --env OMP_NUM_THREADS=2 --rm --network=host -p 1234:1234  -v=$(pwd):/root dist_dcgan:latest python -m torch.distributed.launch --nproc_per_node=2 --nnodes=4 --node_rank=3 --master_addr="172.31.71.56" --master_port=1234 dist_dcgan.py --dataset cifar10 --dataroot ./cifar10  --num_epochs 1 --batch_size 16 --max_workers 2
