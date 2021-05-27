# Passos necessários para execução do experimento

O objetivo deste experimento é entender o processo de automação de provisionamento e configuração de aplicações na nuvem utilizando as ferramentas ANSIBLE e CLAP.

## 1) Configuração do provedor na nuvem

No arquivo "./clap/configs/providers.yaml" é definido o provedor, as chaves de acesso e a região. A configuração utilizada nesse experimento é apresentada abaixo. 

![Figura 1](./screenshots/provider.png)

Figura 1. Configuração do provedor na nuvem utilizada nos experimentos.

## 2) Configuração de login

No arquivo "./clap/configs/logins.yaml" é definido as informações necessárias para o acesso das máquinas virtuais via SSH. A configuração utilizada nesse experimento é apresentada abaixo.

![Figura 2](./screenshots/login.png)

Figura 2. Configuração de login utilizada nos experimentos.

## 3) Configuração de template das instâncias

No arquivo "./clap/configs/instances.yaml" é definido as informações sobre a máquina virtual, como tipo de instância, tipo da imagem, tamanho do disco, grupo de segurança e entre outros.  

![Figura 3](./screenshots/instance.png)

Figura 3. Configuração de template das instâncias.

## 4) Configuração do cluster

Três configurações de cluster foram utilizadas nos experimentos. As configurações de cada cluster estão presentes na pasta "/clap/configs/clusters/".
* Uma máquina t2.small (cluster-t2_small-1x.yml)
* Duas máquinas t2.small (cluster-t2_small-2x.yml)
* Quatro máquinas t2.small (cluster-t2_small-4x.yml)

A estrutura do arquivo cluster-t2_small-xx.yml é ilustrada abaixo.

```
setups:

  ### Get master ip number ###
  setup-ip-master:
    roles:
    - name: gan

    actions:
    - role: gan
      action: run-script
      extra:
        src: ip_master.sh
        args: "0"

  ### Get slave ip numbers ####
  setup-ip-slave:
    roles:
    - name: gan

    actions:
    - role: gan
      action: run-script
      extra:
        src: ip_slave.sh
        args: "0"

  ### Download each IP number from remote machines ###      
  setup-get-ip:
    roles:
    - name: gan

    actions:
    - role: gan
      action: fetch
      extra:
        src: ~/172*
        dest: ~/Desktop/MO833/atividade8/t2_small_4x/

  ### Send all ip numbers and ip code to nodes ###      
  setup-send-ip:
    roles:
    - name: gan

    actions:
    - role: gan
      action: copy
      extra:
        src: ~/Desktop/MO833/atividade8/t2_small_4x/
        dest: ~/

  ### Install Docker and DCGAN ###
  setup-gan:
    roles:
    - name: gan

    actions:
    - role: gan
      action: run-script
      extra:
        src: setup.sh
        args: "0"

  ### Run DCGAN on all nodes ####      
  setup-run:
    roles:
    - name: gan

    actions:
    - role: gan
      action: run-script
      extra:
        src: run.sh
        args: "4" # Total number of nodes (master + slaves)

  ### Download output files from remote to local###
  setup-fetch:
    roles:
    - name: gan

    actions:
    - role: gan
      action: fetch
      extra:
        src: ~/Distributed-DCGAN/ip-*
        dest: ~/Desktop/MO833/atividade8/t2_small_4x/

  setup-fetch-png:
    roles:
    - name: gan

    actions:
    - role: gan
      action: fetch
      extra:
        src: ~/Distributed-DCGAN/*.png
        dest: ~/Desktop/MO833/atividade8/t2_small_4x/


### Cluster t2.small ###
clusters:
  t2_small:

    # These setups are executed at all cluster's nodes, after setups at nodes section
    after_all:
    - setup-send-ip
    - setup-gan
    - setup-run
    - setup-fetch
    - setup-fetch-png

    nodes:
      master-node:
        type: t2_small-ubuntu20-16gb-mpi_group
        count: 1 # Number of master nodes
        setups:
        - setup-ip-master
        - setup-get-ip

      slave-nodes:
        type: t2_small-ubuntu20-16gb-mpi_group  
        count: 3  # Number of slave nodes
        min_count: 0
        setups:                      
        - setup-ip-slave
        - setup-get-ip
```

