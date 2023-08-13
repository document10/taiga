#!/usr/bin/python3
from pathlib import Path
from re import search
from operator import itemgetter
from simple_term_menu import TerminalMenu
import time
import os
import json
import subprocess
import sys
import math

version = 0.4
def clear():
    os.system("clear")

def opt_menu(options,text):
    clear()
    menu = TerminalMenu(options,menu_cursor=(None),menu_highlight_style=("bg_cyan","fg_black"),title=text)
    return menu.show()

def conf_menu(items,text,skip):
    clear()
    if skip == 0:
        options = []
        for i in items:
            options.append(i["name"])
        menu = TerminalMenu(options,menu_cursor=(None),menu_highlight_style=("bg_blue","fg_black","bold"),title=text)
        return menu.show()
    else:
        options = ["Skip"]
        for i in items:
            options.append(i["name"])
        menu = TerminalMenu(options,menu_cursor=(None),menu_highlight_style=("bg_blue","fg_black"),title=text)
        return menu.show()-1

def select_menu(items,text,selected):
    clear()
    print(text)
    terminal_menu = TerminalMenu(items,menu_cursor=(None),menu_highlight_style=("bg_yellow","fg_black","bold"),multi_select=True,multi_select_select_on_accept=False,multi_select_empty_ok=True,title="Press tab/space to select,enter to exit",preselected_entries=selected)
    return terminal_menu.show()

def script(build,distro):
    file = open("taiga_"+str(math.ceil(time.time())),"x")
    if 0 in build["options"]:
        file.write("echo Configuring base system\n")
        for b in distro["pre"]:
            file.write(b+"\n")
    if build["GD"]!=-1:
        file.write("echo Installing graphics drivers\n")
        for g in distro["GD"][build["GD"]]["comm"]:
            file.write(g+"\n")
    if build["DM"]!=-1:
        file.write("echo Installing display manager\n")
        for d in distro["DM"][build["DM"]]["comm"]:
            file.write(d+"\n")
    if build["DE"]!=-1:
        file.write("echo Installing desktop environment\n")
        for e in distro["DE"][build["DE"]]["comm"]:
            file.write(e+"\n")
    if len(build["tasks"])>0:
        file.write("echo Configuring extra tasks\n")
        for t in build["tasks"]:
            file.write("echo " + distro["tasks"][t]["name"]+"\n")
            for c in distro["tasks"][t]["comm"]:
                file.write(c+"\n")
    if 1 in build["options"]:
        file.write("echo Final configuration\n")
        for f in distro["post"]:
            file.write(f+"\n")
    if 2 in build["options"]:
        file.write("echo Installation complete!Rebooting...\n")
        cmd = os.system("which systemctl")
        if cmd == 0:
            file.write("sudo systemctl reboot\n")
        else:
            file.write("sudo reboot\n")
    else:
        file.write("echo Installation complete!")
    file.close()
    return file.name
            


def main_menu(build,distros):
    options = ["Distro:","Graphics:","Display manager:","Desktop environment:"]
    if build["distro"]==-1:
        for o in options:
            o+=" None"
    else:
        options[0]+=distros[build["distro"]]["name"]
        if build["GD"]==-1:
            options[1]+=" None"
        else:
            options[1]+=distros[build["distro"]]["GD"][build["GD"]]["name"]
        
        if build["DM"]==-1:
            options[2]+=" None"
        else:
            options[2]+=distros[build["distro"]]["DM"][build["DM"]]["name"]
        
        if build["DE"]==-1:
            options[3]+=" None"
        else:
            options[3]+=distros[build["distro"]]["DE"][build["DE"]]["name"]
        i=0
    options.append("Extra tasks:"+str(len(build["tasks"])))
    options.append("Additional settings")
    options.append("Install")
    options.append("Save config to file")
    options.append("Build script")
    options.append("Exit")
    action = opt_menu(options,"TAIGA 0.4")
    match action:
        case 0:
            build["distro"] = conf_menu(distros,"Select your distro from the list of supported distros:",0)
            build["GD"] = -1
            build["DM"] = -1
            build["DE"] = -1
            build["tasks"] = []
            build["base"] = 1
            main_menu(build,distros)
        case 1:
            build["GD"] = conf_menu(distros[build["distro"]]["GD"],"Select your graphics driver:",1)
            main_menu(build,distros)
        case 2:
            build["DM"] = conf_menu(distros[build["distro"]]["DM"],"Select your display manager:",1)
            main_menu(build,distros)
        case 3:
            build["DE"] = conf_menu(distros[build["distro"]]["DE"],"Select your desktop environment:",1)
            i = 0
            if build["DE"]!=-1:
                for dm in distros[build["distro"]]["DM"]:
                    if dm["name"] == distros[build["distro"]]["DE"][build["DE"]]["DM"]:
                        build["DM"] = i
                    i+=1
            main_menu(build,distros)
        case 4:
            build["tasks"].sort()
            tasks = []
            i=0
            for t in distros[build["distro"]]["tasks"]:
                tasks.append(t["name"])
                i+=1
            choice = select_menu(tasks,"Extra tasks",build["tasks"])
            build["tasks"] = []
            if choice!=None:
                build["tasks"] = list(choice)
            main_menu(build,distros)            
        case 5:
            build["options"].sort()
            choice = select_menu(["Base packages","Final configuration","Reboot after install"],"Select additional options",build["options"])
            build["options"]= []
            if choice != None:
                build["options"] = list(choice)
            main_menu(build,distros)
        case 6:
            clear()
            msg ="Final options:\nOS:"+ distros[build["distro"]]["name"]+"\n"
            if build["GD"]!=-1:
                msg += "Graphics:"+distros[build["distro"]]["GD"][build["GD"]]["name"]+"\n"
            if build["DM"]!=-1:
                msg += "Display manager:"+distros[build["distro"]]["DM"][build["DM"]]["name"]+"\n"
            if build["DE"]!=-1:
                msg += "Desktop environment:"+distros[build["distro"]]["DE"][build["DE"]]["name"]+"\n"
            if len(build["tasks"])>0:
                msg +="\nExtra tasks:\n"
                for t in build["tasks"]:
                    msg += distros[build["distro"]]["tasks"][t]["name"]+"\n"
            msg += "\nAdditional settings:\n"
            msg += "\nBase packages:"
            if 0 in build["options"]:
                msg += " yes\n"
            else:
                msg += " no\n"
            msg += "\nFinal configuration:"
            if 1 in build["options"]:
                msg += " yes\n"
            else:
                msg += " no\n"
            msg += "\nReboot after install"
            if 1 in build["options"]:
                msg += " yes\n"
            else:
                msg += " no\n"
            msg +="\nConfirm?"
            ok = opt_menu(["Yes","No"],msg)
            if ok == 0:
                file = script(build,distros[build["distro"]])
                clear()
                os.system("sh "+file)
                sys.exit()
            else:
                main_menu(build,distros)
        case 7:                
            file = open("config_"+str(math.ceil(time.time()))+".json","x")
            file.write(json.dumps(build))
            file.close()
            opt_menu(["Press enter to continue"],"Config saved to "+file.name+".You can now load the config using:\n./taiga "+file.name)
            main_menu(build,distros)
        case 8:    
            file = script(build,distros[build["distro"]])
            clear()
            ok = opt_menu(["Return","Exit"],"All commands have been saved to "+ file)
            if ok == 0:
                main_menu(build,distros)
            else:
                print("Installation aborted.")
                sys.exit()
        case 9:
            clear()
            print("Installation aborted.")
            sys.exit()

def load():
    if len(sys.argv) < 2:
        return 0
    else:
        try:
            file = open(sys.argv[1],"r") 
            build = json.loads(file.read())
            file.close()
        except:
            ok = opt_menu(["Discard config","Exit"],"Couldn't load the config.The config is either corrupted or doesn't exist.")
            if ok == 0:
                return 0
            else:
                clear()
                print("Installation aborted")
                sys.exit()
        if "version" in build:
            return build
        else:
            ok = opt_menu(["Discard config","Exit"],"This config is incompatible with this version of TAIGA.")
            if ok == 0:
                return 0
            else:
                clear()
                print("Installation aborted")
                sys.exit()

def serialize():
    distros = []
    workdir = Path.cwd()
    files = os.listdir(str(workdir)+"/distros")
    for f in files:
        file = open(str(workdir)+"/distros/"+f,"r")
        j = json.loads(file.read())
        distros.append(j)
        file.close()
    distros = sorted(distros, key=itemgetter('order'))
    return distros

def get_distro(distros):
    clear()
    for d in distros:
        r = os.system(d["identify"])
        if r == 0:
            return d["order"]
    return -1

def get_gpu(distro):
    output =  str(subprocess.check_output(["sh", "get_gpu.sh"])).lower()
    i = 0
    for v in distro["GD"]:
        if search(v["name"].lower(),output):
            return i
        i+=1
    return -1

def main():
    distros = []
    try:
        distros = serialize()
    except:
        print("Couldn't load info about the distros.Redownload the script and try again.")
        sys.exit(1)
    build = load()
    distro = {}
    if build == 0:
        build = {
            "version":version,
            "distro" : -1,
            "GD" : -1,
            "DM" : -1,
            "DE" : -1,
            "tasks" : [],
            "options":[0,1]
        }
        build["distro"] = get_distro(distros)
        if build["distro"] != -1:
            distro = distros[build["distro"]]
            build["GD"]=get_gpu(distro)
        else:
            build["distro"]= conf_menu(distros,"Your distro couldn't be recognized.Please select your distro manually",1)
            if build["distro"]==-1:
                print("Installation aborted")
                sys.exit()
            else:
                distro = distros[build["distro"]]
                build["GD"]=get_gpu(distro)
        clear()
    else:
        print(str(build)) 
    main_menu(build,distros)

if __name__ == "__main__":
    main()