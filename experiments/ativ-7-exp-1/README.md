# Passos necessários para execução do experimento

## 1) Escolhendo a imagem da máquina

Escolheu-se a imagem "Ubuntu Server 20.04 LTS (HVM), SSD Volume Type" como mostrado na figura abaixo.

![Figura 1](./screenshots/imagem.png)

## 2) Escolhendo o tipo da instância

No experimento foram usadas as intâncias: "c5.large", "m5.large", "m4.large", "m4.xlarge", "t2.large"

## 3) Configurar detalhes da instância

Todas as instâncias foram configuradas de acordo com as imagens abaixo, onde-se utilizou 4 instâncias para cada máquina nos experimentos. A opção "add instance to placement group" foi selecionada para tirar proveito de uma rede como melhor desempenho. Para instalar os pacotes necessários nas máquina para realização dos experimentos, na opção "User Data", foi adicionado o seguinte texto:

```
#!/bin/bash
sudo apt-get update
sudo apt-get install -y \
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
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
```

![Figura 2](./screenshots/instancia1.png)
![Figura 3](./screenshots/instancia2.png)

## 4) Adicionando o dispostivo de armazenamento

## 5) Configurando o grupo de segurança
