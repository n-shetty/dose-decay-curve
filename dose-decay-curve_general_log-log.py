from __future__ import print_function
# coding: utf-8

# In[16]:

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rcParams
import os


# In[17]:

#%matplotlib inline
matplotlib.rcParams.update({'font.size': 10})
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']


# In[18]:

# USER MODIFIABLE PARAMETERS
#
# set material_class to the name of materials folder available in the "results" folder
# following material_class are available as of May 2017:
# aluminum, copper, CuAlFeNi, mirror-material, stainless-steel
material_class = "aluminum"
#
# ignore materials containing this string, otherwise leave the sting empty
# useful to filter out materials within the material_class
ignore_string = "ISO"


# In[19]:

# suffixes of the usrbin files that were generated using the custom "sum-all.sh" script available in the root directory
files = ["_exp_usrbin_21.txt", "_exp_usrbin_22.txt", "_exp_usrbin_23.txt", "_exp_usrbin_24.txt", "_exp_usrbin_25.txt"]


# # Start processing ...

# In[20]:

# list all the materials within the material_class
mylist = next(os.walk(material_class))[1]

# ignoring materials whose name contains the ignore_string
if ignore_string:
    mylist = [x for x in mylist if ignore_string not in x]
    print("Ignored all materials containing the string: {}".format(ignore_string))
    
mylist = sorted(mylist) # sort alphanumerically

# get the parameters (particle type and energy, and irradiation time) corresponding to all the materials
parameters = []
for i in range(0, len(mylist)):
    parameters.append(mylist[i].split("_",1)[1])
    
# identify unique set of parameters and iterate over materials
for unique in set(parameters):
    folders =  [s for s in mylist if unique in s]
    dose_decay = np.zeros((len(folders),5,2))
    
    materials = []
    for i in range(0, len(folders)):
        materials.append(folders[i].split("_",1)[0])

    print("*"*30)
    print("*"*30)
    print("Materials: ")
    print(*materials, sep='\n')
    print("Parameters: "+unique)
    print("Processing the following usrbin files:")
    
    for findex, folder in  enumerate(folders):
        for index, file in enumerate(files):
            link = material_class+"/"+folder+"/"+folder+file
            print(link)
            irrprofi = folder.split("_")[3]
            #
            # quick hack to find the value of dose and its associated error at 
            # a distance of 30 cm from the target along the beam direction
            data = np.genfromtxt(link, skip_header=9, skip_footer=4332-2171)
            values = data[2148:,:].flatten()
            index_max = values.argmax()
            dose_decay[findex,index,0] = values[index_max]
            #
            data = np.genfromtxt(link, skip_header=2172)
            errors = data[2148:,:].flatten()
            dose_decay[findex,index,1] = errors[index_max]
        
    # prepare plots
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.set_xscale('log')
    
    # generate a tuple called "ind" to hold values of different cooling times
    if irrprofi == "1year":
        ind = (1, 86400.0, 604800.0, 2419200.0, 15724800.0)
    elif irrprofi == "1month":
        ind = (1, 3600.0, 28800.0, 86400.0, 604800.0)       
    elif irrprofi == "1day":
        ind = (1, 600.0, 3600.0,10800.0, 28800.0)  
    
    # plot dose decay curves in mSv/hour for each material representing unique parameters
    for i in range(0, len(dose_decay)):
        plt.errorbar(ind, dose_decay[i,:,0]*1e-6*3600, yerr=dose_decay[i,:,1]*dose_decay[i,:,0]*1e-6*3600/100, fmt='--o', label=materials[i])
        
    #print irrprofi        
    #print "\n"
    

    plt.legend()
    legend = ax.legend(loc=3)        
    plt.grid()
    plt.xlim(np.min(ind)/2, )
    #plt.ylim(1, np.max(dose_decay[i,:,0]*1e-6*3600)*2)    
    
    if irrprofi == "1year":
        plt.xlabel("Cooling time [s] (0, 1 day, 1 week, 4 weeks, 26 weeks)")
    elif irrprofi == "1month":
        plt.xlabel("Cooling time [s] (0, 1 hour, 8 hours, 1 day, 1 week)")
    elif irrprofi == "1day":
        plt.xlabel("Cooling time [s] (0, 10 min, 1 hour, 3 hours, 8 hours)")
        
    plt.ylabel("Dose [uSv/hour] at 30 cm")
    #plt.title("Decay curve for "+material_class+" ("+unique+")" )
    fig.tight_layout()
    #plt.show()
    
    if not os.path.exists("plots"):
        os.makedirs("plots")
    plt.savefig("plots/"+material_class+"_"+unique+".eps")


# In[21]:

# list all the cases simulated so far
print("Following parameters have been processed for the available materials:")
for unique in sorted(set(parameters)):
    print(unique)


# In[ ]:



