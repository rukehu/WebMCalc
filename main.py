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
                #print(getRates)

                for key, value in rates.items():
                    if key in getRates:
                        value["price"] = getRates[key]
                break

            else:
                print(f"Error: {response.status_code}")

        except:
            print("fialed to requests rates")
        
        if requestCnt > 5:
            print("requests rates timeout ...")
            break
        time.sleep(3)


class WebMoney(object):
    FEE_FIXED_COST = 0
    FEE_RATE_COST = 1
    
    def __init__(self, config):
        self.root = tk.Tk()
        self.root.title("WebMoney")
        self.exchangeRate = config["ExchangeRate"]
        self.record = config["Record"]
        self.timeRegion = dict()

        rates = self.exchangeRate ["rates"]
        rateList_1 = list()
        rateList_2 = list()

        for key, value in rates:
            data = key + " " + value["name"]
            self.timeRegion[value["country"]] = value["area"]

            if key == self.record["rate"][0]:
                rateList_1.insert(0, data)
            else:
                rateList_1.append(data)
                
            if key == self.record["rate"][1]:
                rateList_2.insert(0, data)
            else:
                rateList_2.append(data)

        self.combox_rate1 = ttk.Combobox(self.root, values=rateList_1)
        self.combox_rate2 = ttk.Combobox(self.root, values=rateList_2)


        
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
        
        try:
            with open("config.json", 'r', encoding='utf-8') as fr:
                fdata = json.load(fr)
                break
        except Exception as e:
            print("Loading data config ERROR, reload after 10s", e)
            time.sleep(10)
        
        print("Config data loading [{}] ...".format(loadcnt))
        if loadcnt > 10:
            break

    return fdata

if __name__ == '__main__':

    cfgData = loadConfig()
    # print(cfgData)
    real_time_rate(cfgData["ExchangeRate"]["url"], cfgData["ExchangeRate"]["rates"])

    print (cfgData["ExchangeRate"]["rates"])


    # wm = WebMoney(config)
    # wm.running()

    


    