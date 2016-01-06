import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg

import Tkinter as tk
import tkFileDialog
import os

import functions_ramantxt as rt
from glob import glob
from datetime import datetime

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
                
        self.lb2 = tk.Label(window,text='H2:')
        self.lb2.grid(row=20,column=0,sticky=tk.W)
        self.lb3 = tk.Label(window,text='CO:')
        self.lb3.grid(row=21,column=0,sticky=tk.W)
        self.lb4 = tk.Label(window,text='CO2:')
        self.lb4.grid(row=22,column=0,sticky=tk.W)
        self.lb5 = tk.Label(window,text='CH4:')
        self.lb5.grid(row=23,column=0,sticky=tk.W)
        
        self.lb6_val = tk.IntVar()
        self.lb6_val.set(0)
        self.lb6 = tk.Label(self.window,textvariable=self.lb6_val)
        self.lb6.grid(row=20,column=1,sticky=tk.W)
        self.lb7_val = tk.IntVar()
        self.lb7_val.set(0)
        self.lb7 = tk.Label(self.window,textvariable=self.lb7_val)
        self.lb7.grid(row=21,column=1,sticky=tk.W)
        self.lb8_val = tk.IntVar()
        self.lb8_val.set(0)
        self.lb8 = tk.Label(self.window,textvariable=self.lb8_val)
        self.lb8.grid(row=22,column=1,sticky=tk.W)
        self.lb9_val = tk.IntVar()
        self.lb9_val.set(0)
        self.lb9 = tk.Label(self.window,textvariable=self.lb9_val)
        self.lb9.grid(row=23,column=1,sticky=tk.W)
        
        self.lb10_val = tk.IntVar()
        self.lb10_val.set(0)
        self.lb10 = tk.Label(self.window,textvariable=self.lb10_val)
        self.lb10.grid(row=20,column=2,sticky=tk.W)
        self.lb11_val = tk.IntVar()
        self.lb11_val.set(0)
        self.lb11 = tk.Label(self.window,textvariable=self.lb11_val)
        self.lb11.grid(row=21,column=2,sticky=tk.W)
        self.lb12_val = tk.IntVar()
        self.lb12_val.set(0)
        self.lb12 = tk.Label(self.window,textvariable=self.lb12_val)
        self.lb12.grid(row=22,column=2,sticky=tk.W)
        self.lb13_val = tk.IntVar()
        self.lb13_val.set(0)
        self.lb13 = tk.Label(self.window,textvariable=self.lb13_val)
        self.lb13.grid(row=23,column=2,sticky=tk.W)         
        

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
        
        self.H2_f_n = self.H2_f/max(self.H2_f)
        self.CO2_f_n = self.CO2_f/max(self.CO2_f) 
        self.CO_f_n = self.CO_f/max(self.CO_f)
        self.CH4_f_n = self.CH4_f/max(self.CH4_f) 

        for item in np.round(self.np_time,2):
            self.listbox.insert(tk.END,item)

        self.ax.plot(self.np_time,self.H2_f, marker='o',markersize=2,label='H2')
        self.ax.plot(self.np_time,self.CO2_f, marker='o',markersize=2,label='CO2')
        self.ax.plot(self.np_time,self.CO_f, marker='o',markersize=2,label='CO')
        self.ax.plot(self.np_time,self.CH4_f, marker='o',markersize=2,label='CH4')
        self.ax.legend()
        
        self.ax1.plot(self.np_time,self.H2_f_n, marker='o',markersize=2,label='H2')
        self.ax1.plot(self.np_time,self.CO2_f_n, marker='o',markersize=2,label='CO2')
        self.ax1.plot(self.np_time,self.CO_f_n, marker='o',markersize=2,label='CO')
        self.ax1.plot(self.np_time,self.CH4_f_n, marker='o',markersize=2,label='CH4')
        self.ax1.legend()
        
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

        ltp1_n = rt.ref(self.H2_f_n, 'H2')
        ltp2_n = rt.ref(self.CO2_f_n, 'CO2')
        ltp3_n = rt.ref(self.CO_f_n, 'CO')
        ltp4_n = rt.ref(self.CH4_f_n, 'CH4')
        d_n = {v_n:(ltp1_n[i_n],ltp2_n[i_n],ltp3_n[i_n],ltp4_n[i_n]) for i_n,v_n in enumerate(np.round(self.np_time.tolist(),2))}
        
        lb6_val = d[value][0][1]
        lb7_val = d[value][1][1]
        lb8_val = d[value][2][1]
        lb9_val = d[value][3][1]
        
        lb10_val = d_n[value][0][1]
        lb11_val = d_n[value][1][1]
        lb12_val = d_n[value][2][1]
        lb13_val = d_n[value][3][1]              
        
        self.lb6_val.set(np.round(lb6_val,2))
        self.lb7_val.set(np.round(lb7_val,2))
        self.lb8_val.set(np.round(lb8_val,2))
        self.lb9_val.set(np.round(lb9_val,2))
        
        self.lb10_val.set(np.round(lb10_val,2))
        self.lb11_val.set(np.round(lb11_val,2))
        self.lb12_val.set(np.round(lb12_val,2))
        self.lb13_val.set(np.round(lb13_val,2))
            
    
    def Clear(self):
        self.ax.clear()
        self.ax1.clear()
        self.ax.grid()
        self.ax1.grid()
        self.canvas.draw()
        
        self.lb6_val.set(0)
        self.lb7_val.set(0)
        self.lb8_val.set(0)
        self.lb9_val.set(0)
        self.lb10_val.set(0)
        self.lb11_val.set(0)
        self.lb12_val.set(0)
        self.lb13_val.set(0)
        
        self.listbox.delete(0, tk.END)
    
    def Save(self):
        f = tkFileDialog.asksaveasfilename()
        if f is None:
            return
        out = np.column_stack((self.np_time,self.H2_f,self.CO2_f,self.CO_f,self.CH4_f,self.H2_f_n,self.CO2_f_n,self.CO_f_n,self.CH4_f_n))
        np.savetxt(f, out, fmt='%1.6f',delimiter=" ")
    
    def Quit(self):
        self.window.destroy()
        
        
def main():
    root = tk.Tk()
    app = Plot(root)
    tk.mainloop()

if __name__ == '__main__':
    main()
