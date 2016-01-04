import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import Tkinter as tk
import tkFileDialog
import sys
import os

import raman_txt_new as rt
from glob import glob
from datetime import datetime

class Plot(object):

    def __init__(self, window):
        self.window = window
        window.title('My plot')
        #window.geometry('800x800')
        self.fig =  plt.figure(figsize=(6,6), dpi=100)
        self.ax = self.fig.add_subplot(211)
        self.ax1 = self.fig.add_subplot(212)
        self.ax.grid()
        self.ax1.grid()
        self.ax1.set_xlabel('time / minute')

        self.bu1 = tk.Button(window,text='Load',command=self.Open,fg='red').grid(row=0,column=0)
        self.bu2 = tk.Button(window,text='Clear',command=self.Clear,fg='red').grid(row=1,column=0)
        self.bu3 = tk.Button(window,text='Time',command=self.Clear,fg='red').grid(row=2,column=0)
        
        self.lb1 = tk.Label(window,text='Time / min')
        self.lb1.grid(row=14,column=0)
          
        self.listbox = tk.Listbox(window, height=20, width=15)
        self.listbox.grid(row=15,column=0)#, rowspan=10, columnspan=2)
        self.listbox.bind("<Double-Button-1>", self.Print_area)
                
        self.lb2 = tk.Label(window,text='H2:')
        self.lb2.grid(row=20,column=0,sticky=tk.W)
        self.lb3 = tk.Label(window,text='CO:')
        self.lb3.grid(row=21,column=0,sticky=tk.W)
        self.lb4 = tk.Label(window,text='CO2:')
        self.lb4.grid(row=22,column=0,sticky=tk.W)
        self.lb5 = tk.Label(window,text='CH4:')
        self.lb5.grid(row=23,column=0,sticky=tk.W)
        

        # Radio buttons
        self.radio1 = tk.Radiobutton(window,text='Original',value=1,variable=1)
        self.radio1.grid(row=9,column=0,sticky=tk.W)
        self.radio2 = tk.Radiobutton(window,text='Normalized',value=2,variable=1)
        self.radio2.grid(row=10,column=0,sticky=tk.W)
        
        self.canvas = FigureCanvasTkAgg(self.fig, window)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0,column=5,columnspan=25, rowspan=25)
                
    def Open(self):

        file_txt = glob(tkFileDialog.askdirectory()+os.sep+'*TrendData.txt')
        
        def make_datetime(lst):
           """Used as a key in lambda function"""
           date_str = lst.split('_')[4]
           return datetime.strptime(date_str, '%H-%M-%S')
        
        sorted_txt = sorted(file_txt, key=make_datetime)

        li_time,li_H2,li_CO,li_CO2,li_CH4 = rt.extract_area(sorted_txt)

        self.np_time = rt.conv_inmin(li_time)
        np_H2 = np.array(li_H2)
        np_CO2 = np.array(li_CO2)
        np_CO = np.array(li_CO)
        np_CH4 = np.array(li_CH4)
        
        self.H2_f = rt.ev_mis(np_H2, self.np_time)
        self.CO2_f = rt.ev_mis(np_CO2, self.np_time)
        self.CO_f = rt.ev_mis(np_CO, self.np_time)
        self.CH4_f = rt.ev_mis(np_CH4, self.np_time)

        for item in np.round(self.np_time,2):
            self.listbox.insert(tk.END,item)

        self.ax.plot(self.np_time,self.H2_f, marker='o',label='H2')
        self.ax.plot(self.np_time,self.CO2_f, marker='o',label='CO2')
        self.ax.plot(self.np_time,self.CO_f, marker='o',label='CO')
        self.ax.plot(self.np_time,self.CH4_f, marker='o',label='CH4')
        
        self.ax1.plot(self.np_time,self.H2_f/max(self.H2_f), marker='o',label='H2')
        self.ax1.plot(self.np_time,self.CO2_f/max(self.CO2_f), marker='o',label='CO2')
        self.ax1.plot(self.np_time,self.CO_f/max(self.CO_f), marker='o',label='CO')
        self.ax1.plot(self.np_time,self.CH4_f/max(self.CH4_f), marker='o',label='CH4')
        
        self.canvas.draw()

    def Print_area(self, event):
        
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        #print "selection:", selection, ": '%s'" % value
        
        # Dict comprehension
        ltp1 = rt.ref(self.H2_f, 'H2')
        ltp2 = rt.ref(self.CO2_f, 'CO2')
        ltp3 = rt.ref(self.CO_f, 'CO')
        ltp4 = rt.ref(self.CH4_f, 'CH4')
        d = {v:(ltp1[i],ltp2[i],ltp3[i],ltp4[i]) for i,v in enumerate(np.round(self.np_time.tolist(),2))}

        ltp1_n = rt.ref((self.H2_f/max(self.H2)), 'H2')
        ltp2_n = rt.ref((self.CO2_f/max(self.CO2_f)), 'CO2')
        ltp3_n = rt.ref((self.CO_f/max(self.CO_f)), 'CO')
        ltp4_n = rt.ref((self.CH4_f/max(self.CH4_f)), 'CH4')
        d_n = {v_n:(ltp1_n[i],ltp2_n[i],ltp3_n[i],ltp4_n[i]) for i_n,v_n in enumerate(np.round(self.np_time.tolist(),2))}
        
        lb6 = d_n[value][0][1]
        lb7 = d_n[value][1][1]
        lb8 = d_n[value][2][1]
        lb9 = d_n[value][3][1]
        
        print "selection:",  '%.1f, %.1f, %.1f, %.1f' % (lb6,lb7,lb8,lb9)

        #self.lb6.destroy()
        self.lb6 = tk.Label(self.window,text='%.1f' %lb6)
        self.lb6.grid(row=20,column=1,sticky=tk.W)
        #self.lb7.destroy()
        self.lb7 = tk.Label(self.window,text='%.1f'%lb7)
        self.lb7.grid(row=21,column=1,sticky=tk.W)
        #self.lb8.destroy()
        self.lb8 = tk.Label(self.window,text='%.1f'%lb8)
        self.lb8.grid(row=22,column=1,sticky=tk.W)
        #self.lb9.destroy()
        self.lb9 = tk.Label(self.window,text='%.1f'%lb9)
        self.lb9.grid(row=23,column=1,sticky=tk.W)    
    
    def Clear(self):
        self.ax.clear()
        self.ax1.clear()
        self.ax.grid()
        self.ax1.grid()
        self.canvas.draw()
    
    def Save(self):
        print np.round(self.np_time,2) 
        
def main():
    root = tk.Tk()
    app = Plot(root)
    tk.mainloop()

if __name__ == '__main__':
    main()
