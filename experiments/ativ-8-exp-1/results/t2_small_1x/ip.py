import os

directory = './'

ip = []
num_rank = []
i = 0
for file in os.listdir(directory):
  if file.endswith(".slave"):
    i = i + 1
    num_rank.append(str(i))
    with open(file) as f:
      ip.append(f.read())
      
ip = sorted(ip)
      
#file = open('./ip_slaves',"w")
#for x in ip:
#  file.write(x) 
#file.close()
#
#file = open('./rank_slaves',"w")
#for x in num_rank:
#  file.write(x + ' \n') 
#file.close()
   

file = open('./rank_number',"w")
j = 0
for x in ip:
  j = j + 1
  file.write(str(j) + ' ') 
  file.write(x) 
file.close()
   

