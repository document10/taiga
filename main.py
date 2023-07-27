from pathlib import Path
import os
import json

#Serialize all info related to distros
distros = []
id = 0
env = 'Arch Linux' #this is temporary,only arch is supported atm
workdir = Path.cwd()
dirs = os.listdir(str(workdir)+"/packages")
dirs.remove('packages.md')
for d in dirs:
    file = open(str(workdir)+"/packages/"+d)
    j = json.loads(file.read())
    distros.append(j)
    file.close() #Closing the file prevents any errors after we're done with the file.

#Check if the user is logged in as root
mode = 0
if os.getuid() != 0:
    print("WARNING!")
    print("The script is not running as root.Therefore,the script will run in \"simulation mode\",which will only show you the commands that would be executed.")
    mode = 0
else:
    print("Running as root.")
    mode = 1

###Code for identifying distros will go here

###Code for identifying distros will go here

distro = distros[id]
build = {
    "name":env,
    "GD":0,
    "DM":0,
    "DE":0
}

i=0
for gd in distro["GD"]:
    print(str(i)+"."+gd["name"])
    i+=1
try:
    build["GD"]= int(input("Enter the graphics driver:"))
except:
    print("Invalid option")
    exit()
if build["GD"]>=len(distro["GD"]) or build["GD"]<0:
    print("Invalid option")
    exit()

i=0
for de in distro["DE"]:
    print(str(i)+"."+de["name"])
    i+=1
try:
    build["DE"]= int(input("Enter the desktop environment:"))
except:
    print("Invalid option")
    exit()

if build["DE"]>=len(distro["DE"]) or build["DE"]<0:
    print("Invalid option")
    exit()
i=0
for dm in distro["DM"]:
    if dm["name"] != distro["DE"][build["DE"]]["DM"]:
        print(str(i)+"."+ dm["name"])
    else:
        print(str(i)+"."+ dm["name"]+" (recommended for " + distro["DE"][build["DE"]]["name"]+")")
    i+=1
try:
    build["DM"]= int(input("Enter the display manager:"))
except:
    print("Invalid option")
    exit()
if build["DM"]>=len(distro["DM"]) or build["DE"]<0:
    print("Invalid option")
    exit()

print("Final options:")
print("Graphics:"+distro["GD"][build["GD"]]["name"])
print("Desktop Environment:"+distro["DE"][build["DE"]]["name"])
print("Display Manager:"+distro["DM"][build["DM"]]["name"])
ok = input("Confirm?(y/n/yes/no)").lower()
if ok == "y" or ok=="yes":
    install = distro["installer"]
    for b in distro["base"]:
        install += " " + b
    for g in distro["GD"][build["GD"]]["packages"]:
        install += " " + g
    for d in distro["DM"][build["DM"]]["packages"]:
        install += " " + d
    for e in distro["DE"][build["DE"]]["packages"]:
        install += " " + e
    services = distro["services"]+ distro["DM"][build["DM"]]["service"]
    if mode == 0:
        print("Installing packages")
        print(install)
        print("Configuring "+distro["DM"][build["DM"]]["name"])
        print(services)
        print("Final configuration")
        for c in distro["extra"]:
            print(c)
        print("Simulation completed.")
    else:
        print("Installing packages")
        os.system(install)
        print("Configuring "+distro["DM"][build["DM"]]["name"])
        os.system(services)
        print("Final configuration")
        for c in distro["extra"]:
            os.system(c)
        print("Installation completed.Reboot the system to enter your new GUI!")
else:
    print("Installation aborted.")