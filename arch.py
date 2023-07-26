import os

options = {
    "graphics" : ["Skip","Mesa/VMs","Nvidia","AMD","Intel"],
    "DM" : ["Skip","GDM","SDDM","LightDM"],
    "DE" : ["Skip","Awesome","Budgie","Cinnamon","Cutefish","Deepin","Enlightenment","GNOME","KDE Plasma","LXDE","LXQT","MATE","XFCE"]
}
build = {
    "graphics" : 0,
    "DM" : 0,
    "DE" : 0
}
packages = {
    "graphics" : ["",["xf86-video-vesa"],["nvidia-dkms nvidia-utils", "lib32-nvidia-utils", "nvidia-settings", "vulkan-icd-loader", "lib32-vulkan-icd-loader"],["lib32-mesa", "vulkan-radeon" ,"lib32-vulkan-radeon" ,"vulkan-icd-loader","lib32-vulkan-icd-loader"],["lib32-mesa vulkan-intel", "lib32-vulkan-intel", "vulkan-icd-loader", "lib32-vulkan-icd-loader"]],
    "DM" : ["",["sddm"],["lightdm","lightdm-gtk-greeter"],["gdm"]],
    "DE" : ["",["awesome","pcmanfm","network-manager-applet"],["budgie","budgie-desktop-view","budgie-backgrounds","materia-gtk-theme","papirus-icon-theme"],["cinnamon","nemo-fileroller","faenza-icon-theme","nemo-preview","nemo-seahorse","nemo-share","nemo-terminal","network-manager-applet"],["cutefish"],["deepin","deepin-kwin","deepin-extra"],["enlightenment","ecrire","ephoto","evisum","rage","terminology","connman"],["gnome"],["plasma", "plasma-wayland-session", "kde-applications" ,"packagekit-qt5"],["lxde","network-manager-applet"],["lxqt","network-manager-applet","breeze-icons","oxygen-icons"],["mate","mate-extra"],["xfce4","xfce4-goodies"]],
    "base": ["xorg", "xorg-server", "xterm", "firefox","avahi" ,"xdg-user-dirs" ,"xdg-utils", "gedit", "bluez", "bluez-utils", "alsa-utils", "pipewire", "pipewire-alsa" , "pipewire-pulse" ,"pipewire-jack" ,"sof-firmware" ,"blueman" ,"arc-solid-gtk-theme", "arc-gtk-theme","arc-icon-theme"]
}

command = "sudo pacman -Syu"

services = ["","gdm.service","sddm.service","lightdm.service"]
print("Select your graphics")
for i in range(0,len(options["graphics"])):
    print(str(i)+":"+options["graphics"][i])

build["graphics"] = int(input())

print("Select your display manager")
for i in range(0,len(options["DM"])):
    print(str(i)+":"+options["DM"][i])

build["DM"] = int(input())

print("Select your desktop environment")
for i in range(0,len(options["DE"])):
    print(str(i)+":"+options["DE"][i])

build["DE"] = int(input())

print("Final options:")
print("Graphics:"+options["graphics"][build["graphics"]])
print("Display manager:"+options["DM"][build["DM"]])
print("Desktop environment:"+options["DE"][build["DE"]])
ok= input("Confirm?").lower()
if ok == "y" or ok == "yes":    
    print("To be installed:")
    print("Base packages:")
    for p in packages["base"]:
        print(p)
    print("Graphics:")
    if build["graphics"]==0:
        print("Skipped")
    else:
        for p in packages["graphics"][build["graphics"]]:
            print(p)
    print("Display manager:")
    if build["DM"]==0:
        print("Skipped")
    else:
        for p in packages["DM"][build["DM"]]:
            print(p)
    print("Desktop environment:")
    if build["DE"]==0:
        print("Skipped")
    else:
        for p in packages["DE"][build["DE"]]:
            print(p)

    for p in packages["base"]:
        command += " "+ p
    if build["graphics"]!=0:
        for p in packages["graphics"][build["graphics"]]:
            command += " "+ p
    if build["DM"]!=0:
        for p in packages["DM"][build["DM"]]:
            command += " "+ p
    if build["DE"]!=0:
        for p in packages["DE"][build["DE"]]:
            command += " "+ p

    os.system(command)

else:
    print("Installation aborted.")