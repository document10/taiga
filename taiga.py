from pathlib import Path
from re import search
import os
import json
import subprocess

#Serialize all info related to distros
distros = []
distro = {}
id = -1
mode = 0
workdir = Path.cwd()
dirs = os.listdir(str(workdir)+"/distros")
dirs.remove('distros.md')
for d in dirs:
    file = open(str(workdir)+"/distros/"+d)
    j = json.loads(file.read())
    distros.append(j)
    file.close() #Closing the file prevents any errors after we're done with the file.

#Check if the user is logged in as root
if os.getuid() != 0:
    print("WARNING!")
    print("The script is not running as root.Therefore,the script will run in \"simulation mode\",which will only show you the commands that would be executed.")
    mode = 0
else:
    print("Running as root.")
    mode = 1

build = {
    "distro":-1,
    "GD":-1,
    "DM":-1,
    "DE":-1,
    "base_pkgs":0
}

def run_task(task):
    if mode == 1:
        os.system(task)
    else:
        print(task)

print("1.Express install:Automatically detect the distro,GPU and installs the desired desktop environment with the reccomended display manager")
print("2.Custom  install:Select all options manually")
ins_type = input("Select installation type(0 to abort):")

if ins_type == "1":
    #Identifying the distro
    i = 0
    for d in distros:
        c = os.system(d["identify"])
        if c==0:
            id = i
        i+=1
    if id ==-1:
        print("Couldn't identify the distro.Your distro may be unsupported.Aborting")
        exit()
    else:
        distro = distros[id]
        build["distro"]=id
        print("Identified distro:" + distro["name"])

    #Identifying GPU
    i=0
    video =  str(subprocess.check_output(["sh", "get_gpu.sh"]))
    for v in distro["GD"]:
        if search(v["name"],video):
            build["GD"] = i
        i+=1
    if build["GD"]==-1:
        print("GPU couldn't be identified.Aborting")
        exit()
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
        exit()
    i=0
    for dm in distro["DM"]:
        if dm["name"] == distro["DE"][build["DE"]]["DM"]:
            build["DM"]=i
        i+=1
elif ins_type=="2":
    i=0
    for d in distros:
        print(str(i)+"."+d["name"])
        i+=1
    try:
        build["distro"]=int(input("Select your distro from the list of supported distros:"))
    except:
        print("Invalid option")
        exit()
    if build["distro"]>=len(distros) or build["distro"]<0:
        print("Invalid option")
        exit()
    distro = distros[build["distro"]]

    i=1
    for gd in distro["GD"]:
        print(str(i)+"."+gd["name"])
        i+=1
    try:
        build["GD"]= int(input("Enter the graphics driver(0 to skip):"))-1
    except:
        print("Invalid option")
        exit()
    if build["GD"]>=len(distro["GD"]) or build["GD"]<-1:
        print("Invalid option")
        exit()

    i=1
    for dm in distro["DM"]:    
        print(str(i)+"."+ dm["name"])
        i+=1
    try:
        build["DM"]= int(input("Enter the display manager(0 to skip):"))-1
    except:
        print("Invalid option")
        exit()
    if build["DM"]>=len(distro["DM"]) or build["DM"]<-1:
        print("Invalid option")
        exit()

    i=1
    for de in distro["DE"]:
        print(str(i)+"."+de["name"])
        i+=1
    try:
        build["DE"]= int(input("Enter the desktop environment(0 to skip):"))-1
    except:
        print("Invalid option")
        exit()

    if build["DE"]>=len(distro["DE"]) or build["DE"]<-1:
        print("Invalid option")
        exit()

else:
    print("Installation aborted.")
    exit()

print("Final options:")
print("Distro:"+distro["name"])
if build["GD"]!=-1:
    print("Graphics:"+distro["GD"][build["GD"]]["name"])
if build["DM"]!=-1:
    print("Display Manager:"+distro["DM"][build["DM"]]["name"])
if build["DE"]!=-1:
    print("Desktop Environment:"+distro["DE"][build["DE"]]["name"])
ok = input("Confirm?(y/n/yes/no)").lower()
if ok == "y" or ok=="yes":
    services = ""
    print("Preconfiguring system")
    for c in distro["pre"]:
        run_task(c)
    install = distro["installer"]
    for b in distro["base"]:
        install += " " + b
    print("Installing base packages")
    run_task(install)
    print("Installing drivers")
    install = distro["installer"]
    if build["GD"]!=-1:
        for g in distro["GD"][build["GD"]]["packages"]:
            install += " " + g
        run_task(install)
    else:
        print("Skipped")
    print("Installing display manager")
    install = distro["installer"]
    if build["DM"]!=-1:
        for d in distro["DM"][build["DM"]]["packages"]:
            install += " " + d
        run_task(install)
        services = distro["services"]+ distro["DM"][build["DM"]]["service"]
        run_task(services)
    else:
        print("Skipped")

    print("Installing desktop environment")
    install = distro["installer"]
    if build["DE"]!=-1:
        for e in distro["DE"][build["DE"]]["packages"]:
            install += " " + e
        run_task(install)
    else:
        print("Skipped")
    
    print("Final configuration")
    for c in distro["post"]:
        run_task(c)
    
    print("Installation completed.Reboot the system to enter your new GUI!")
else:
    print("Installation aborted.")