#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 17:59:54 2018

@author: Wilson
"""

# program for parsing the json data.
import json
import csv
import os

# instance variables
general_counter = 0


# folder manipulation.
def folder_traversal (rootDir):
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            print(os.path.join(root, file))
            # filter the data file.
            if (file == "backup_data.dat" or file == ".DS_Store"):
                continue
            else:
                open_file = open(root + "/" + file)
                while 1:
                    line = open_file.readline()
                    if not line:
                        break
                    data = json.loads(line)
                    dat_manipulation(data)
                
        for dir in dirs:
            folder_traversal(dir)


# specific file manipulation.    
def dat_manipulation (data):
    global general_counter
    
    if general_counter == 0:
        keyword = 'w'
    else:
        keyword = 'a'
        
    with open('formatted_data.csv',keyword) as csvfile:
        writer = csv.writer(csvfile)
        fileHeader = ["id","lat","lon","mmac"]
        normalData = [data["id"],data["lat"],data["lon"],data["mmac"]]
        writer.writerow(fileHeader)
        writer.writerow(normalData)
        # empty row for seperating the data.
        writer.writerow("")
        
        writer.writerow(["general_counter", "sub_counter","mac","rssi","router","range"])
        sub_counter = 0
        for i in data["data"]:
            general_counter += 1
            sub_counter += 1
            rowData = [general_counter,sub_counter]
            rowData.append(i["mac"])
            rowData.append(i["rssi"])
            if "router" in i:
                rowData.append(i["router"])
            else:
                rowData.append("N/A")
                rowData.append(i["range"])
                writer.writerow(rowData)
        sub_counter = 0
        
if __name__ == "__main__":
    rootDir = "file path goes here"
    folder_traversal(rootDir)