#!/usr/bin/python3
from pathlib import Path
from re import search
from operator import itemgetter
import time
import os
import json
import subprocess
import sys
import math
id = -1
mode = 1
sim = ""
load = 0
distros = []
distro = {}
workdir = ""
dirs = []
#Serialize all info related to distros
try:
    workdir = Path.cwd()
    dirs = os.listdir(str(workdir)+"/distros")
    dirs.remove('distros.md')
    for d in dirs:
        file = open(str(workdir)+"/distros/"+d,"r")
        j = json.loads(file.read())
        distros.append(j)
        file.close()
except:
    print("ERROR:The script couldn't load all required files propperly.This could be because some files are missing or corrupt.Reinstall the script and try again.")
    exit(1)

build = {
    "distro":-1,
    "GD":-1,
    "DM":-1,
    "DE":-1,
    "tasks":[]
}

if len(sys.argv) > 1:
    if sys.argv[1].lower() == "s":
        mode = 0
        print("Running in simulation mode,no changes will be made to your system.")
        sim = open("taiga_"+str(math.ceil(time.time())), "x")
    elif sys.argv[1].lower() == "l":
        try:
            path = sys.argv[2]
            f = open(sys.argv[2],"r")    
            build = json.loads(f.read())
        except:
            print("Configuration invalid!")
            exit(1)
        distro = distros[build["distro"]]
        load = 1
        f.close()
        print("Config loaded from :" + f.name)
    elif sys.argv[1].lower() == "sl" or sys.argv[1].lower() == "ls":
        try:
            path = sys.argv[2]
            f = open(sys.argv[2],"r")    
            build = json.loads(f.read())
        except:
            print("Configuration invalid!")
            exit(1)
        distro = distros[build["distro"]]
        load = 1
        f.close()
        print("Config loaded from :" + f.name)
        mode = 0
        print("Running in simulation mode,no changes will be made to your system.")
        sim = open("taiga_"+str(math.ceil(time.time())), "x")
    elif sys.argv[1].lower() =="h":
        print("./taiga.py [args]")
        print("python taiga.py [args]")
        print("python3 taiga.py [args]")
        print("Note:arguments are not case sensitive.")
        print("")
        print("s : Simulation mode-no changes will be done to the system")
        print("l [filepath]: loads configuration from the file specified in [filepath]")
        print("sl/ls [filepath]: loads configuration from the file specified in [filepath] and enters Simulation mode")
        print("h : shows this screen and exits")
        exit()
    else:
        print("Invalid argument")
        exit(1)


def run_comm(comm):
    if mode ==0:
        print(comm)
        sim.write(comm)
        sim.write("\n")
    elif mode == 1:
        os.system(comm)
    elif mode == 2:
        print(comm)
        os.system(comm)

distros = sorted(distros, key=itemgetter('order')) 

if load == 0:
    print("1.Express install:Automatically detect the distro,GPU and installs the desired desktop environment with the reccomended display manager")
    print("2.Custom  install:Select all options manually")
    try:
        ins_type = int(input("Select installation type(0 to abort):"))
    except:
        print("Invalid option")
        exit(1)

    if ins_type == 1:
        #Identifying the distro
        i = 0
        while id==-1 and i <len(distros):
            c = os.system(distros[i]["identify"])
            if c==0:
                id = i
            i+=1
        if id ==-1:
            print("Couldn't identify the distro.Your distro may be unsupported.Aborting")
            exit(1)
        else:
            distro = distros[id]
            build["distro"]=id
            print("Identified distro:" + distro["name"])

        #Identifying GPU
        i=0
        video =  str(subprocess.check_output(["sh", "get_gpu.sh"])).lower()
        for v in distro["GD"]:
            if search(v["name"].lower(),video):
                build["GD"] = i
            i+=1
        if build["GD"]==-1:
            print("GPU couldn't be identified.Aborting")
            exit(1)
        else:
            print("Detected GPU:"+distro["GD"][build["GD"]]["name"])
        
        i=1
        for de in distro["DE"]:
            print(str(i)+"."+de["name"])
            i+=1
        try:
            build["DE"]= int(input("Enter the desktop environment:"))-1
        except:
            print("Invalid option")
            exit(1)
        if build["DE"]>=len(distro["DE"]) or build["DE"]<0:
            print("Invalid option")
            exit(1)
        i=0

        for dm in distro["DM"]:
            if dm["name"] == distro["DE"][build["DE"]]["DM"]:
                build["DM"]=i
            i+=1
    elif ins_type==2: 
        i=1
        for d in distros:
            print(str(i)+"."+d["name"])
            i+=1
        try:
            build["distro"]=int(input("Select your distro from the list of supported distros:"))-1
        except:
            print("Invalid option")
            exit(1)
        if build["distro"]>=len(distros) or build["distro"]<0:
            print("Invalid option")
            exit(1)
        distro = distros[build["distro"]]

        i=1
        for gd in distro["GD"]:
            print(str(i)+"."+gd["name"])
            i+=1
        try:
            build["GD"]= int(input("Enter the graphics driver(0 to skip):"))-1
        except:
            print("Invalid option")
            exit(1)
        if build["GD"]>=len(distro["GD"]) or build["GD"]<-1:
            print("Invalid option")
            exit(1)

        i=1
        for dm in distro["DM"]:    
            print(str(i)+"."+ dm["name"])
            i+=1
        try:
            build["DM"]= int(input("Enter the display manager(0 to skip):"))-1
        except:
            print("Invalid option")
            exit(1)
        if build["DM"]>=len(distro["DM"]) or build["DM"]<-1:
            print("Invalid option")
            exit(1)

        i=1
        for de in distro["DE"]:
            print(str(i)+"."+de["name"])
            i+=1
        try:
            build["DE"]= int(input("Enter the desktop environment(0 to skip):"))-1
        except:
            print("Invalid option")
            exit(1)

        if build["DE"]>=len(distro["DE"]) or build["DE"]<-1:
            print("Invalid option")
            exit(1)
    else:
        print("Installation aborted.")
        exit()
    #Extra tasks
    i=0
    for t in distro["tasks"]:
        ch = input(t["name"]+"?(y/n)").lower()
        if ch == "y":
            build["tasks"].append(i)
        i+=1

print("Final options:")
print("Distro:"+distro["name"])
if build["GD"]!=-1:
    print("Graphics:"+distro["GD"][build["GD"]]["name"])
if build["DM"]!=-1:
    print("Display Manager:"+distro["DM"][build["DM"]]["name"])
if build["DE"]!=-1:
    print("Desktop Environment:"+distro["DE"][build["DE"]]["name"])
if len(build["tasks"]) != 0:
    print("Extra tasks:")
    for t in build["tasks"]:
        print(distro["tasks"][t]["name"])

print("1.Confirm and install")
print("2.Save config to file and exit")
if mode == 1:
    print("3.Simulate commands")
try:
    ok = int(input("Select action(0 to abort):"))
except:
    print("Invalid option!")
    exit(1)

if ok == 3:
    mode = 0
    print("Running in simulation mode,no changes will be made to your system.")
    sim = open("taiga_"+str(math.ceil(time.time())), "x")

if ok == 1 or ok == 3:
    print("Configuring base system")
    for c in distro["pre"]:
        run_comm(c)
    print("Installing drivers")
    if build["GD"]!=-1:
        for g in distro["GD"][build["GD"]]["comm"]:
            run_comm(g)
    else:
        print("Skipped")
    print("Installing display manager")
    if build["DM"]!=-1:
        for d in distro["DM"][build["DM"]]["comm"]:
            run_comm(d)
    else:
        print("Skipped")

    print("Installing desktop environment")
    if build["DE"]!=-1:
        for c in distro["DE"][build["DE"]]["comm"]:
            run_comm(c)
    else:
        print("Skipped")
    
    print("Performing extra tasks")
    if len(build["tasks"]) == 0:
        print("Skipped")
    else:
        for t in build["tasks"]:
            print(distro["tasks"][t]["name"])
            cmd = distro["tasks"][t]["comm"]
            for c in cmd:
                run_comm(c)

    print("Final configuration")
    for c in distro["post"]:
        run_comm(c)
    if mode ==0:
        print("All commands have been saved to " + sim.name)
        sim.close()
    else:
        print("Installation completed.Reboot the system to enter your new GUI!")
elif ok ==2:
    f = open("config_"+str(math.ceil(time.time()))+".json", "x")
    f.write(json.dumps(build))
    f.close()
    print("Config has been saved to " + f.name)
else:
    print("Installation aborted.")
    exit()

