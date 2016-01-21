import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg

import Tkinter as tk
import tkFileDialog
import os
import re

import functions_raman_g as rt
from glob import glob
from datetime import datetime

# This file has to be used together with functions_raman_g (in the same folder)

class Plot(object):

    def __init__(self, window):
        self.window = window
        window.title('Raman txt')
        #window.geometry('800x800')
        self.fig =  plt.figure(figsize=(6,6), dpi=100)
        self.ax = self.fig.add_subplot(211)
        self.ax1 = self.fig.add_subplot(212)
        self.ax.grid()
        self.ax1.grid()
        self.ax1.set_xlabel('time / minute')

        self.bu1 = tk.Button(window,text='Load',command=self.Open,fg='red').grid(row=0,column=0)
        self.bu2 = tk.Button(window,text='Clear',command=self.Clear,fg='red').grid(row=1,column=0)
        self.bu3 = tk.Button(window,text='Save',command=self.Save,fg='red').grid(row=2,column=0)
        self.bu4 = tk.Button(window,text='Quit',command=self.Quit,fg='red').grid(row=3,column=0)
        
        self.lb1 = tk.Label(window,text='Time / min')
        self.lb1.grid(row=14,column=0)
          
        self.listbox = tk.Listbox(window, height=20, width=15)
        self.listbox.grid(row=15,column=0)#, rowspan=10, columnspan=2)
        self.listbox.bind("<Button-1>", self.Print_area)                

        self.canvas = FigureCanvasTkAgg(self.fig, window)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=1,column=5,columnspan=25, rowspan=25)
        
        toolbar_frame = tk.Frame(window)
        toolbar_frame.grid(row=0,column=5,columnspan=25)
        toolbar = NavigationToolbar2TkAgg(self.canvas, toolbar_frame)
                                                                                                                    
    def Open(self):

        file_txt = glob(tkFileDialog.askdirectory()+os.sep+'*TrendData.txt')
        
        def make_datetime(lst):
           """Used as a key in lambda function"""
           reg = r'\d+\-\d+\-\d+'
           date_str=re.findall(reg, lst)[1]
           #date_str = lst.split('_')[4]
           return datetime.strptime(date_str, '%H-%M-%S')
        
        sorted_txt = sorted(file_txt, key=make_datetime)
        self.samples = rt.get_samples(sorted_txt)
        # Fill empy lists with the content of SORTED file's name
        areas = rt.extract_area(sorted_txt)
        # Make up numpy time and numpy areas
        self.time_numpy, self.areas_numpy = rt.ev_mis(areas)
        # Normalized numpy areas
        self.areas_numpy_n = rt.normalize(self.areas_numpy)
        # Listbox
        for item in np.round(self.time_numpy,2):
            self.listbox.insert(tk.END,item)
        # Plot original data
        for i in range(0, len(self.areas_numpy)):
            self.ax.plot(self.time_numpy,self.areas_numpy[i],label=i)
            self.ax.legend(prop={'size':8})
        # Plot normalized data
        for i in range(0, len(self.areas_numpy_n)):
            self.ax1.plot(self.time_numpy,self.areas_numpy_n[i])
        
        ######## Create sample labels ###########################################
        self.lbl_samples = []
        for i,v in enumerate(self.samples):
            self.lbl_samples.append(tk.Label(self.window, text=v))
        for i,v in enumerate(self.lbl_samples):
            v.grid(row=20+i,column=0,sticky=tk.W)
        
        ######## Create default labels values for original area #################
        self.lbl_areas = []
        for i in range(0, len(self.samples)):
            self.lbl_areas.append(tk.Label(self.window,text="0"))
        for i,v in enumerate(self.lbl_areas):
            v.grid(row=20+i,column=1,sticky=tk.W) 
        
        ######## Create default zero values for normalized area #################
        self.lbl_areas_n = []
        for i in range(0, len(self.samples)):
            self.lbl_areas_n.append(tk.Label(self.window,text="0"))
        for i,v in enumerate(self.lbl_areas_n):
            v.grid(row=20+i,column=2,sticky=tk.W)
         
        self.canvas.draw()

    def Print_area(self, event):
        
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        #print "selection:", selection, ": '%s'" % value
        
        # Zip sample names with areas
        ltp = rt.ref(self.areas_numpy,self.samples)
        
        # Zip sample names with normalized areas
        ltp_n = rt.ref(self.areas_numpy_n,self.samples)
        
        ########## Original data ####################################
        self.d = {}
        for i in range(0,len(ltp)):
            for k,v in enumerate(np.round(self.time_numpy.tolist(),2)):
                self.d.setdefault(v, []).append(ltp[i][k])
        
        lbl_areas_val = [0]*len(self.samples)
        for i in range(0, len(self.samples)):
            lbl_areas_val[i] = self.d[value][i][1]
        
        for i in range(0, len(self.samples)):
            self.lbl_areas[i].configure(text=np.round(lbl_areas_val[i],2))    
        
        ########## Normalized data ####################################
        self.d_n = {}
        for i in range(0,len(ltp_n)):
            for k,v in enumerate(np.round(self.time_numpy.tolist(),2)):
                self.d_n.setdefault(v, []).append(ltp_n[i][k])
                
        lbl_areas_n_val = [0]*len(self.samples)
        for i in range(0, len(self.samples)):
            lbl_areas_n_val[i] = self.d_n[value][i][1]

        for i in range(0, len(self.samples)):
            self.lbl_areas_n[i].configure(text=np.round(lbl_areas_n_val[i],2))   
    
    def Clear(self):
        self.ax.clear()
        self.ax1.clear()
        self.ax.grid()
        self.ax1.grid()
        self.canvas.draw()
        
        for i in range(0, len(self.samples)):
            self.lbl_samples[i].destroy()
        
        for i in range(0, len(self.samples)):
            self.lbl_areas[i].destroy()
        
        for i in range(0, len(self.samples)):
            self.lbl_areas_n[i].destroy() 
        
        self.listbox.delete(0, tk.END)
    
    def Save(self):
        f = tkFileDialog.asksaveasfilename()
        if f is None:
            return
        out_o = np.asarray(self.areas_numpy)
        out_n = np.asarray(self.areas_numpy_n)

        out = np.column_stack((self.time_numpy,out_o.T,out_n.T))
        np.savetxt(f, out, fmt='%1.6f',delimiter=" ")
    
    def Quit(self):
        self.window.destroy()
        
        
def main():
    root = tk.Tk()
    app = Plot(root)
    tk.mainloop()

if __name__ == '__main__':
    main()
