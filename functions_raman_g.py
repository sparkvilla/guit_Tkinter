import numpy as np
import matplotlib.pylab as plt
from glob import glob
from datetime import datetime
import re

#############################################################
################## Text files ###############################
#############################################################

# This file can be used as standalone version or being used as module in gui_raman_g

def get_samples(li_name):
    """Takes a list of files. 
       Get the longest file (its name as a string) of the list.
       Return a list containing all samples names of the experiment"""
    samples = [] 
    d={}
    for fi in li_name: 
        with open(fi) as f:
            lin = f.read().splitlines()
            d[fi] = len(lin)-1
    # Get the key (file name) with the maximum value (length) associated
    name = max(d.iterkeys(), key=(lambda x: d[x]))
    with open(name) as nm:
        lin2 = nm.read().splitlines()
        for i in range(1, len(lin)-1):
            samples.append(lin2[i].replace('"','').split(',')[0])
    return samples
                                                             

def extract_area(li_name):
    """Take a list of files.
       Use helper function (get_samples) to extract time and area of txt files.
       Handle txt files of different length."""
    
    container = [[] for i in range(len(get_samples(li_name))+1)]
        
    for fi in li_name:
        with open(fi) as f:
            lin = f.read().splitlines()
        container[0].append(lin[0].replace('"','').split(',')[1].split(' ')[1])
        for i in range(1, len(lin)-1):
            container[i].append(float(lin[i].replace('"','').split(',')[1]))
    return container
        
def make_datetime(lst):
    """Used as a key in lambda function to sort the files"""
    reg = r'\d+\-\d+\-\d+'
    date_str=re.findall(reg, lst)[1]
    #date_str = lst.split('_')[4]
    return datetime.strptime(date_str, '%H-%M-%S')

def conv_inmin(lst):
    """Convert H:M:S format in minutes for a list of files. Returns a numpy array with time"""
    FMT = '%H:%M:%S'
    li_x = [(datetime.strptime(i, FMT) - datetime.strptime(lst[0], FMT)).total_seconds()/60.0 for i in lst]
    return np.array(li_x)

def ev_mis(lst):
    """Take the output of extract area function.
       Convert time string in seconds with the helper function (conv_inmin).
       Convert lists in numpy arrays
       Even the mismatch between numpy arrays. The time (lst[0]) is the term of comparison.
       Return a list of numpy arrays with equal size."""
       
    lst[0] = conv_inmin(lst[0])
    # Convert list of lists to list of numpy arrays
    lst_numpy = []
    for i in lst:
        lst_numpy.append(np.array(i))      
        
    for i in range(1, len(lst_numpy)):
        if len(lst_numpy[i])<len(lst_numpy[0]):
            diff = np.zeros(len(lst_numpy[0])-len(lst_numpy[i]))
            lst_numpy[i] = np.concatenate((diff,lst_numpy[i]))
        else:
            lst_numpy[i]
            #time and areas
    return lst_numpy[0], lst_numpy[1:]

def ref(lst_npareas, lst_samples):
    """Takes the list of numpy areas and the list of samples and zip them 
       in a list of tuples of length = len(np1)"""
    li1 = []
    for i in range(0,len(lst_npareas)):
        li1.append(zip([lst_samples[i]]*len(lst_npareas[i]),lst_npareas[i]))
    return li1

def normalize(lst_npareas):
    """ Takes the list containing numpy areas.
        Normalize by the maximum each numpy array.
        If max=0 do not mormalize the array.
        Return a list of normalized and not normalize numpy arrays."""
    lst_npareas_n = [np.zeros(len(lst_npareas[0])) for _ in xrange(len(lst_npareas))]
    for i in range(0,len(lst_npareas)):
        for k in range(0, len(lst_npareas[i])):
            if max(lst_npareas[i])!=0:
                lst_npareas_n[i][k] = (lst_npareas[i][k]/max(lst_npareas[i]))
            else:
                lst_npareas_n[i][k] = lst_npareas[i][k]
    return lst_npareas_n
                  
if __name__ == "__main__":

    # Dump files into a list and sort them in time order
    file_txt = glob('*TrendData.txt')
    sorted_txt = sorted(file_txt, key=make_datetime)
    samples = get_samples(sorted_txt)

    
    # Fill empy lists with the content of SORTED file's name
    areas = extract_area(sorted_txt)
    
    # Make up numpy time and numpy areas
    time_numpy, areas_numpy = ev_mis(areas)
    
    # Normalize array (if max=0 do not normalize)        
    areas_numpy_n = normalize(areas_numpy)
    
    #[[k/max(sublist) for k in sublist] for sublist in areas_numpy if max(sublist)==0]
    
    # Zip sample names with areas
    ltp = ref(areas_numpy,samples)
    
    # Dictionary
    d = {}
    for i in range(0,len(ltp)):
        for k,v in enumerate(np.round(time_numpy.tolist(),2)):
            d.setdefault(v, []).append(ltp[i][k])
    

    
#plt.figure(1)
#plt.title('Normalized Area')
#plt.plot(np_time,np_H2/max(np_H2), marker='o',label='H2')
#plt.plot(np_time,CO2_f/max(CO2_f), marker='o',label='CO2')
#plt.plot(np_time,CO_f/max(CO_f), marker='o',label='CO')
#plt.plot(np_time,CH4_f/max(CH4_f), marker='o',label='CH4')
#plt.grid()
#plt.xlabel('Time / minutes')
#plt.ylabel('Area')
#plt.legend(loc='best')
