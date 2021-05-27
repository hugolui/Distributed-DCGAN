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
  

### Work directories ###
directory = []
directory.append('./t2_small_1x/')
directory.append('./t2_small_2x/')
directory.append('./t2_small_4x/')


### Get mean iteration time #
mean_it = {} # Store mean iteration time for each machine
for i in range(len(directory)):
  num_outfiles = len(glob.glob1(directory[i],"*.out"))
  it_values = []
  for file in os.listdir(directory[i]):
    if file.endswith(".out"):
      output_file = os.path.join(directory[i], file)

      for j in range(1,19):
        it_info = search_string_in_file(output_file, 'iteration: '+ str(j) +'/')
        result = re.search('iteration time: (.*)s', it_info[0][1])
        it_values.append(float(result.group(1)))
        
  mean_it[directory[i]] = np.mean(it_values)
  
iter_time = np.zeros(len(directory))
for i in range(len(directory)):
  iter_time[i] =  mean_it[directory[i]]

### Plot results ###
num_nodes = np.array([1,2,4])
fig, ax = plt.subplots()
ax.plot(num_nodes, iter_time, 'k-s')
ax.set_xlabel('Number of nodes', fontsize='large')
ax.set_ylabel('Mean iteration time (s)',fontsize='large')
ax.set_xticks(np.array([1,2,4]))
plt.show()
plt.savefig('mean_iteration.png', dpi = 300)
        
