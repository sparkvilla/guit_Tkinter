import numpy as np
import matplotlib.pylab as plt
from glob import glob
from datetime import datetime

#############################################################
################## Text files ###############################
#############################################################

def extract_area(name):
    """Use helper functions to extract sample,time and area of a txt file.
       Handle txt file of different lengths."""
    
    li_time = []
    li_H2 = []
    li_CO2 = []
    li_CO = []
    li_CH4 = []
    
    for fi in name:
        with open(fi) as f:
            lin = f.read().splitlines()
        if len(lin)-1 == 1:
            """Get time string 1st line. Appends to li_time"""
            li_time.append(lin[0].replace('"','').split(',')[1].split(' ')[1])
        elif len(lin)-1 == 2:
            """Get time string 1st line. Appends to li_time"""
            li_time.append(lin[0].replace('"','').split(',')[1].split(' ')[1])
            """Get H2 area 2nd line. Appends to li_H2"""
            li_H2.append(float(lin[1].replace('"','').split(',')[1]))
        elif len(lin)-1 == 3:
            """Get time string 1st line. Appends to li_time"""
            li_time.append(lin[0].replace('"','').split(',')[1].split(' ')[1])
            """Get H2 area 2nd line. Appends to li_H2"""
            li_H2.append(float(lin[1].replace('"','').split(',')[1]))
            """Get CO2 area 3rd line. Appends to li_CO2"""
            li_CO2.append(float(lin[2].replace('"','').split(',')[1]))
        elif len(lin)-1 == 4:
            """Get time string 1st line. Appends to li_time"""
            li_time.append(lin[0].replace('"','').split(',')[1].split(' ')[1])
            """Get H2 area 2nd line. Appends to li_H2"""
            li_H2.append(float(lin[1].replace('"','').split(',')[1]))
            """Get CO2 area 3rd line. Appends to li_CO2"""
            li_CO2.append(float(lin[2].replace('"','').split(',')[1]))
            """Get CO area 4th line. Appends to li_CO"""
            li_CO.append(float(lin[3].replace('"','').split(',')[1]))
        elif len(lin)-1 == 5:
            """Get time string 1st line. Appends to li_time"""
            li_time.append(lin[0].replace('"','').split(',')[1].split(' ')[1])
            """Get H2 area 2nd line. Appends to li_H2"""
            li_H2.append(float(lin[1].replace('"','').split(',')[1]))
            """Get CO2 area 3rd line. Appends to li_CO2"""
            li_CO2.append(float(lin[2].replace('"','').split(',')[1]))
            """Get CO area 4th line. Appends to li_CO"""
            li_CO.append(float(lin[3].replace('"','').split(',')[1]))
            """Get CH4 area 5th line. Appends to li_CH4"""
            li_CH4.append(float(lin[4].replace('"','').split(',')[1]))
    return li_time,li_H2, li_CO, li_CO2, li_CH4
    
    
def make_datetime(lst):
    """Used as a key in lambda function"""
    date_str = lst.split('_')[1]
    return datetime.strptime(date_str, '%H-%M-%S')

def conv_inmin(lst):
    """Convert H:M:S format in minutes for a list of files. Returns a numpy array with time"""
    FMT = '%H:%M:%S'
    li_x = [(datetime.strptime(i, FMT) - datetime.strptime(lst[0], FMT)).total_seconds()/60.0 for i in lst]
    return np.array(li_x)

def ev_mis(np1, np2):
    """Even the mismatch between two numpy arrays. The second should be always time"""
    if len(np1) < len(np2):
         diff = np.zeros(len(np2)-len(np1))
         np_f = np.concatenate((diff,np1))
         return np_f
    else:
        return np1

def ref(np1, strg):
    """Takes numpy array (np1) and a string (strg) and zip them in a list
       of tuples of length = len(np1)"""
    lst = zip([strg]*len(np1),np1)
    return lst
         
if __name__ == "__main__":

    # Dump files into a list and sort them in time order
    file_txt = glob('*TrendData.txt')
    sorted_txt = sorted(file_txt, key=make_datetime)
    
    # Fill empy lists with the content of SORTED file's name
    li_time,li_H2,li_CO,li_CO2,li_CH4 = extract_area(sorted_txt)
    
    # Make up numpy arrays
    np_time = conv_inmin(li_time)
    np_H2 = np.array(li_H2)
    np_CO2 = np.array(li_CO2)
    np_CO = np.array(li_CO)
    np_CH4 = np.array(li_CH4)
    
    # Even the mismatch
    H2_f = ev_mis(np_H2, np_time)
    CO2_f = ev_mis(np_CO2, np_time)
    CO_f = ev_mis(np_CO, np_time)
    CH4_f = ev_mis(np_CH4, np_time)
    
    # Dict comprehension
    ltp1 = ref(H2_f, 'H2')
    ltp2 = ref(CO2_f, 'CO2')
    ltp3 = ref(CO_f, 'CO')
    ltp4 = ref(CH4_f, 'CH4')
    d = {v:(ltp1[i],ltp2[i],ltp3[i],ltp4[i]) for i,v in enumerate(np_time.tolist())}

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
