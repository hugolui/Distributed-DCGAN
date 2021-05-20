import os
import re
import glob
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams.update({'font.size': 12, 'font.family': 'serif', 'text.usetex': True})

def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers
    https://thispointer.com/python-search-strings-in-a-file-and-get-line-numbers-of-lines-containing-the-string/
    """
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

### Renting price ###
price = {}
price['./m5.large/'] = 0.096 # USD per hour
price['./m4.large/'] = 0.1 # USD per hour
#price['./m4.xlarge/'] = 0.2 # USD per hour
price['./c5.xlarge/'] = 0.17 # USD per hour
price['./t2.large/'] = 0.0928 # USD per hour

### Work directories ###
directory = []
directory.append('./m5.large/')
directory.append('./m4.large/')
#directory.append('./m4.xlarge/')
directory.append('./c5.xlarge/')
directory.append('./t2.large/')

epoch_time = {} # Store epoch time for each machine and rank
first_iteration = {} # Store first iteration time for each machine and rank
second_iteration = {} # Store second iteration time for each machine and rank
mean_it_2to11 = {} # Store mean iteration (2th to 11th) time for each machine
for i in range(len(directory)):
  num_outfiles = len(glob.glob1(directory[i],"*.out"))
  epoch_values = []
  first_it_values = []
  second_it_values = []
  it_values = []
  for file in os.listdir(directory[i]):
    if file.endswith(".out"):
      output_file = os.path.join(directory[i], file)
      epoch_time_info = search_string_in_file(output_file, 'Epoch time')
      first_it_info = search_string_in_file(output_file, 'iteration: 0/')
      second_it_info = search_string_in_file(output_file, 'iteration: 1/')
      result = re.search('Epoch time:(.*)s,', epoch_time_info[0][1])
      epoch_values.append(float(result.group(1)))
      result = re.search('iteration time: (.*)s', first_it_info[0][1])
      first_it_values.append(float(result.group(1)))
      result = re.search('iteration time: (.*)s', second_it_info[0][1])
      second_it_values.append(float(result.group(1)))
      
      for j in range(1,11):
        it_info = search_string_in_file(output_file, 'iteration: '+ str(j) +'/')
        result = re.search('iteration time: (.*)s', it_info[0][1])
        it_values.append(float(result.group(1)))
        
  mean_it_2to11[directory[i]] = np.mean(it_values)
      
  epoch_time[directory[i]] = epoch_values
  first_iteration[directory[i]] = first_it_values
  second_iteration[directory[i]] = second_it_values

### Compute mean results as we have multiples ranks ###
mean_epoch_time = {}
mean_first_iteration = {}
mean_second_iteration = {}
for i in range(len(directory)):
  mean_epoch_time[directory[i]] = np.mean(epoch_time[directory[i]])
  mean_first_iteration[directory[i]] = np.mean(first_iteration[directory[i]])
  mean_second_iteration[directory[i]] = np.mean(second_iteration[directory[i]])
  
# Cost based on 1 epoch #
cost_epoch = {}
for i in range(len(directory)):
  cost_epoch[directory[i]] = price[directory[i]]*(mean_epoch_time[directory[i]]/3600)
  
# Cost based on the first iteration #
cost_1iteration = {}
for i in range(len(directory)):
  cost_1iteration[directory[i]] = price[directory[i]]*(mean_first_iteration[directory[i]]/3600)
  
# Cost based on the second iteration #
cost_2iteration = {}
for i in range(len(directory)):
  cost_2iteration[directory[i]] = price[directory[i]]*(mean_second_iteration[directory[i]]/3600)
  
# Cost based on the 2th to 11th iteration #
cost_2to11iteration = {}
for i in range(len(directory)):
  cost_2to11iteration[directory[i]] = price[directory[i]]*(mean_it_2to11[directory[i]]/3600)
  
### Plot results ###
plt.figure()
for i in range(len(directory)): 
  plt.plot(mean_epoch_time[directory[i]]/3600, cost_epoch[directory[i]], 's', label = directory[i][2:-1])
plt.xlabel('Epoch time (hours)')
plt.ylabel('Cost (USD)')
plt.legend()
plt.show()
plt.savefig('cost_epoch.png', dpi = 300)

plt.figure()
for i in range(len(directory)): 
  plt.plot(mean_first_iteration[directory[i]]/3600, cost_1iteration[directory[i]], 's', label = directory[i][2:-1])
plt.xlabel('First iteration time (hours)')
plt.ylabel('Cost (USD)')
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
plt.legend()
plt.show()
plt.savefig('cost_1teration.png', dpi = 300)

plt.figure()
for i in range(len(directory)): 
  plt.plot(mean_second_iteration[directory[i]]/3600, cost_2iteration[directory[i]], 's', label = directory[i][2:-1])
plt.xlabel('Second iteration time (hours)')
plt.ylabel('Cost (USD)')
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
plt.legend()
plt.show()
plt.savefig('cost_2iteration.png', dpi = 300)

plt.figure()
for i in range(len(directory)): 
  plt.plot(mean_it_2to11[directory[i]]/3600, cost_2to11iteration[directory[i]], 's', label = directory[i][2:-1])
plt.xlabel('10 iterations time (hours)')
plt.ylabel('Cost (USD)')
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
plt.legend()
plt.show()
plt.savefig('cost_2to11iteration.png', dpi = 300)

# Compute cost for one epoch (391 iterations for batch size = 32 )
cost_1epoch_1it = {}
cost_1epoch_2it = {}
cost_1epoch_10it = {}
#cost_1epoch['./m5.large/']
#cost_1epoch['./m4.large/']
#cost_1epoch['./m4.xlarge/']
#cost_1epoch['./c5.xlarge/']
#cost_1epoch['./t2.large/']
for i in range(len(directory)): 
  cost_1epoch_1it[directory[i]] = cost_1iteration[directory[i]]*391
  cost_1epoch_2it[directory[i]] = cost_2iteration[directory[i]]*391
  cost_1epoch_10it[directory[i]] = cost_2to11iteration[directory[i]]*391

### Compute relative erro for one epoch (391 iterations for batch size = 32 )
error_1epoch_1it = {}
error_1epoch_2it = {}
error_1epoch_10it = {}
for i in range(len(directory)): 
  error_1epoch_1it[directory[i]] = (np.abs(cost_1epoch_1it[directory[i]] - cost_epoch[directory[i]])/cost_epoch[directory[i]])*100
  error_1epoch_2it[directory[i]] = (np.abs(cost_1epoch_2it[directory[i]] - cost_epoch[directory[i]])/cost_epoch[directory[i]])*100
  error_1epoch_10it[directory[i]] = (np.abs(cost_1epoch_10it[directory[i]] - cost_epoch[directory[i]])/cost_epoch[directory[i]])*100
  