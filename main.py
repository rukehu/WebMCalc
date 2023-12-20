#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import json
import tkinter as tk
from tkinter import ttk
import requests

def real_time_rate(url, rates):
    requestCnt = 0
    while True:
        requestCnt += 1
        try:
            response = requests.get(url)
            if response.status_code == 200:
                json_data = response.json()
                getRates = json_data["rates"]

                break
            else:
                print(f"Error: {response.status_code}")
        except:
            print("fialed to requests rates")
        
        if requestCnt > 3:
            break
        time.sleep(3)



class WebMoney(object):
    FEE_FIXED_COST = 0
    FEE_RATE_COST = 1
    
    def __init__(self, config):
        self.root = tk.Tk()
        self.root.title("WmCalc")

        self.dropdown1 = ttk.Combobox(self.root, values=["Option 1", "Option 2", "Option 3"])
        self.dropdown2 = ttk.Combobox(self.root, values=["Choice A", "Choice B", "Choice C"])
        
    def running(self):
        self.root.mainloop()
    
    def exchange(self, rate, fee, feepay, cost):
        
        num = None
        
        if fee > 0:
            if feepay == self.FEE_RATE_COST:
                num = cost * (1 - fee) / rate 
            elif feepay == self.FEE_FIXED_COST:
                num = (cost - fee) / rate
        else:
            num = cost / rate
        
        return num
        
    def calcCost(self, rate, fee, feepay, num):
        cost = 0
        
        if fee > 0:
            if feepay == self.FEE_RATE_COST:
                cost = num * rate / (1 - fee)
            elif feepay == self.FEE_FIXED_COST:
                cost = num * rate + fee
        else:
            cost = num * rate
            
        return cost

def loadConfig():
    fdata = None
    loadcnt = 0
    while True:
        loadcnt += 1
        print("Config data loading [{}] ...".format(loadcnt))
        try:
            with open("config.json", 'r', encoding='utf-8') as fr:
                fdata = json.load(fr)
                break
        except Exception as e:
            print("Loading data config ERROR, reload after 10s", e)
            time.sleep(10)
        if loadcnt > 10:
            break

    return fdata

if __name__ == '__main__':

    cfgData = loadConfig()

    # wm = WebMoney(config)
    # wm.running()

    


    