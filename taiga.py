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

#will be important for future versions
version = 0.4

#clears screen
def clear():
    os.system("clear")

#functions for creating menus

#generic menu
def opt_menu(options,text,index=0,hint=0):
    clear()
    if hint == 1:
        menu = TerminalMenu(options,menu_cursor=(None),quit_keys=("none"),menu_highlight_style=("bg_cyan","fg_black"),title=text,skip_empty_entries=True,cursor_index=index,status_bar="\nArrow keys:Navigate options\nEnter:Select\n/:Search\nPress the key in braces to quickly select the option",status_bar_style=("fg_green","italics"),shortcut_key_highlight_style=("fg_purple","bold"))
        return menu.show()
    else:
        menu = TerminalMenu(options,menu_cursor=(None),quit_keys=("none"),menu_highlight_style=("bg_cyan","fg_black"),title=text,skip_empty_entries=True,cursor_index=index)
        return menu.show()

#configs menu
def conf_menu(items,text,skip,index=0):
    clear()
    if skip == 0:
        options = []
        sc = ["[0] ","[1] ","[2] ","[3] ","[4] ","[5] ","[6] ","[7] ","[8] ","[9] ","[a] ","[b] ","[c] ","[d] ","[e] ","[f] ","[g] ","[h] ","[i] "]
        n = 0
        for i in items:
            if len(items) < 11:
                options.append("["+str(n)+"]"+i["name"])
            else:
                options.append(sc[n]+i["name"])
            n+=1
        menu = TerminalMenu(options,menu_cursor=(None),quit_keys=("none"),menu_highlight_style=("bg_purple","fg_black"),title=text,cursor_index=index,status_bar="\nArrow keys:Navigate options\nEnter:Select\n/:Search\nPress the key in braces to quickly select the option",status_bar_style=("fg_green","italics"),shortcut_key_highlight_style=("fg_red","bold"))
        return menu.show()
    else:
        options = ["[0] Skip"]
        sc = ["[1] ","[2] ","[3] ","[4] ","[5] ","[6] ","[7] ","[8] ","[9] ","[a] ","[b] ","[c] ","[d] ","[e] ","[f] ","[g] ","[h] ","[i] ","[j] ","[k] ","[l] ","[m] ","[n] ","[o] ","[p] ","[q] ","[r] ","[s] ","[t] ","[u] ","[v] ","[w] ","[x] ","[y] ","[z] "]
        n=1
        for i in items:
            if len(items) < 11:
                options.append("["+str(n)+"]"+i["name"])
            else:
                options.append(sc[n]+i["name"])
            n+=1
        menu = TerminalMenu(options,menu_cursor=(None),quit_keys=("none"),menu_highlight_style=("bg_blue","fg_black"),title=text,cursor_index=index,status_bar="\nArrow keys:Navigate options\nEnter:Select\n/:Search\nPress the key in braces to quickly select the option",status_bar_style=("fg_green","italics"),shortcut_key_highlight_style=("fg_blue","bold"))
        return menu.show()-1

#selection menu
def select_menu(items,text,selected):
    clear()
    terminal_menu = TerminalMenu(items,menu_cursor=(None),quit_keys=("none"),menu_highlight_style=("bg_yellow","fg_black"),multi_select=True,multi_select_select_on_accept=False,multi_select_empty_ok=True,title=text,multi_select_cursor_style=("fg_red","bold"),preselected_entries=selected,status_bar="\nArrow keys:Navigate options\nTab/Space:Toggle options\nEnter:Confirm selection\n/:Search",status_bar_style=("fg_cyan","italics"),exit_on_shortcut=False)
    return terminal_menu.show()

#builds the script for execution
def script(build,distro,name = "taiga_"+str(math.ceil(time.time()))):
    file = ""
    try:
        file = open(name,"x")
    except:
        file = open("taiga_"+str(math.ceil(time.time())*2),"x")
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
            

#main menu
def main_menu(build,distros,index):
    #create base options
    options = ["[o] Distro:","[g] Graphics:","[m] Display manager:","[d] Desktop environment:","","[x] Extra tasks:"+str(len(build["tasks"])),"[a] Additional options","","[i] Install","[s] Save config to file","[b] Build script","[q] Quit installation"]
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
    #wait for choice from user
    action = opt_menu(options,"TAIGA "+str(version),index,1)
    match action:
        case 0:
            #change user distro
            choice = conf_menu(distros,"Select your distro from the list of supported distros:",0,build["distro"])
            if choice != None:
                build["distro"] = choice
                build["GD"] = get_gpu(distros[build["distro"]])
                build["DM"] = -1
                build["DE"] = -1
                build["tasks"] = []
            main_menu(build,distros,action)
        case 1:
            #change graphics driver
            choice = conf_menu(distros[build["distro"]]["GD"],"Select your graphics driver:",1,build["GD"]+1)
            
            build["GD"]=choice
            main_menu(build,distros,action)
        case 2:
            #change display manager
            choice = conf_menu(distros[build["distro"]]["DM"],"Select your display manager:",1,build["DM"]+1)
            
            build["DM"] = choice
            main_menu(build,distros,action)
        case 3:
            #change desktop emvironment
            choice = conf_menu(distros[build["distro"]]["DE"],"Select your desktop environment:",1,build["DE"]+1)
            
            build["DE"] = choice
            #autoassign display manager
            i = 0
            if build["DE"]!=-1:
                for dm in distros[build["distro"]]["DM"]:
                    if dm["name"] == distros[build["distro"]]["DE"][build["DE"]]["DM"]:
                        build["DM"] = i
                    i+=1
            main_menu(build,distros,action)
        case 5:
            #toggle tasks
            build["tasks"].sort()
            tasks = []
            for t in distros[build["distro"]]["tasks"]:
                tasks.append(t["name"])
            choice = select_menu(tasks,"Extra tasks",build["tasks"])
            build["tasks"] = list(choice or [])
            main_menu(build,distros,action)            
        case 6:
            #additional options
            build["options"].sort()
            choice = select_menu(["Base packages","Final configuration","Reboot after install"],"Select additional options",build["options"])
            build["options"] = list(choice or [])
            main_menu(build,distros,action)
        case 8:
            #install
            clear()
            #shows installation options
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
            if 0 not in build["options"]:
                msg += "Skip base packages\n"
            if 1 not in build["options"]:
                msg += "Skip final configuration\n"
            if 2 in build["options"]:
                msg += "Reboot after install\n"    
            
            msg +="\nConfirm?"
            #ask for confirmation
            ok = opt_menu(["[y] Yes","[n] No"],msg)
            if ok == 0:
                #begin install
                file = script(build,distros[build["distro"]])
                clear()
                try:
                    os.system("sh "+file)
                except:
                    print("Installation failed.")
                sys.exit()
            else:
                #return to main menu
                main_menu(build,distros,action)
        case 9:
            #save config
            clear()
            name = input("Type file name here:\n") or "config_"+str(math.ceil(time.time()))+".json"
            file = ""
            try:
                file = open(name,"x")
            except:
                file = open("config_"+str(math.ceil(time.time())*2)+".json","x")
            config = {
                "version":version,
                "distro" : distros[build["distro"]]["name"],
                "GD" :  -1,
                "DM" :  -1,
                "DE" :  -1,
                "tasks" : [],
                "options":build["options"]
            }
            if build["GD"]!=-1:
                config["GD"]=distros[build["distro"]]["GD"][build["GD"]]["name"]
            if build["DM"]!=-1:
                config["DM"]=distros[build["distro"]]["DM"][build["DM"]]["name"]
            if build["DE"]!=-1:
                config["DE"]=distros[build["distro"]]["DE"][build["DE"]]["name"]
            if len(build["tasks"]) != 0 :
                for t in build["tasks"]:
                    config["tasks"].append(distros[build["distro"]]["tasks"][t]["name"])
            file.write(json.dumps(config))
            file.close()
            opt_menu(["Press enter to continue"],"Config saved to "+file.name+".You can now load the config using:\n./taiga "+file.name)
            main_menu(build,distros,action)
        case 10:
            #save script
            clear()
            name = input("Type file name here:\n") or "taiga_"+str(math.ceil(time.time()))
            file = script(build,distros[build["distro"]],name)
            clear()
            ok = opt_menu(["Press enter to continue"],"All commands have been saved to "+ file)
            main_menu(build,distros,action)
        case 11:
            #exit
            clear()
            print("Installation aborted.")
            sys.exit()

#load configs from args
def load(distros):
    if len(sys.argv) < 2:
        return 0
    else:
        build = {}
        config = {
            "version":version,
            "distro" : -1,
            "GD" : -1,
            "DM" : -1,
            "DE" : -1,
            "tasks" : [],
            "options":[0,1]
        }
        try:
            file = open(sys.argv[1],"r") 
            build = json.loads(file.read())
            file.close()
        except:
            #config is invalid
            ok = opt_menu(["[d] Discard config","[x] Exit"],"Couldn't load the config.The config is either corrupted or doesn't exist.")
            if ok == 0:
                return 0
            else:
                clear()
                print("Installation aborted")
                sys.exit()
        #checks if the config has all the necesary options
        if "version" in build and "distro" in build and "GD" in build and "DM" in build and "DE" in build and "tasks" in build and "options" in build:
            #convert from names to indexes
            names = []
            for d in distros:
                names.append(d["name"])
            try:
                config["distro"]=names.index(build["distro"])
            except:
                config["distro"]=get_distro(distros)
            names = []
            if build["GD"]!=-1:
                for d in distros[config["distro"]]["GD"]:
                    names.append(d["name"])
                try:
                    config["GD"]=names.index(build["GD"])
                except:
                    config["GD"]=get_gpu(distros[config["distro"]])
            names = []
            if build["DM"]!=-1:
                for d in distros[config["distro"]]["DM"]:
                    names.append(d["name"])
                try:
                    config["DM"]=names.index(build["DM"])
                except:
                    config["DM"]=-1
            names = []
            if build["DE"]!=-1:
                for d in distros[config["distro"]]["DE"]:
                    names.append(d["name"])
                try:
                    config["DE"]=names.index(build["DE"])
                except:
                    config["DE"]=-1
            names = []
            if len(build["tasks"])!=0:
                for d in distros[config["distro"]]["tasks"]:
                    names.append(d["name"])
                for t in build["tasks"]:
                    try:
                        config["tasks"].append(names.index(t))
                    except:
                        print("error")
            config["options"]=build["options"]
            config["version"]=build["version"]
            return config
        else:
            ok = opt_menu(["[d] Discard config","[x] Exit"],"This config is incompatible with this version of TAIGA.")
            if ok == 0:
                return 0
            else:
                clear()
                print("Installation aborted")
                sys.exit()

#gets all data regarding distros
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

#(attempt to) get the distro
def get_distro(distros):
    clear()
    for d in distros:
        r = os.system(d["identify"])
        if r == 0:
            return d["order"]
    return -1

#(attempt to) identify GPU
def get_gpu(distro):
    os.system("lspci -v | grep VGA >> cache.file")
    file = open("cache.file","r")
    output =  file.read()
    file.close()
    os.system("rm -rf cache.file")
    i = 0
    for v in distro["GD"]:
        if search(v["name"].lower(),output.lower()):
            return i
        i+=1
    return -1

#main function
def main():
    distros = []
    try:
        distros = serialize()
    except:
        #something went wrong with collecting distro info
        print("Couldn't load info about the distros.Redownload the script and try again.")
        sys.exit(1)
    #info about current config
    build = load(distros)
    distro = {}
    if build == 0:
        #no config was loaded,loads the default config
        build = {
            "version":version,
            "distro" : -1,
            "GD" : -1,
            "DM" : -1,
            "DE" : -1,
            "tasks" : [],
            "options":[0,1]
        }
        #gets info about the system
        build["distro"] = get_distro(distros)
        if build["distro"] != -1:
            distro = distros[build["distro"]]
            build["GD"]=get_gpu(distro)
        else:
            #couldn't identify the distro
            build["distro"]= conf_menu(distros,"Your distro couldn't be recognized.Please select your distro manually",0)
            if build["distro"]==None:
                print("Installation aborted.")
                sys.exit(1)
            distro = distros[build["distro"]]
            build["GD"]=get_gpu(distro)
        clear()
    main_menu(build,distros,0)

#just some boilerplate
if __name__ == "__main__":
    main()