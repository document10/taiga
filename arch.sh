#!/usr/bin/bash
gd=0
dm=0
de=0

echo "Select graphics driver"
echo "1.Virtualbox/VMware"
echo "2.Intel"
echo "3.AMD"
echo "4.Nvidia"
echo "0.Skip"
read gd

echo "Select display manager"
echo "1.Gnome Display Manager (GDM)"
echo "2.LightDM"
echo "3.SDDM"
echo "0.Skip"
read dm

echo "Select Desktop Environment"
echo "1.GNOME"
echo "2.KDE Plasma"
echo "3.XFCE"
echo "4.LXDE"
echo "5.LXQT"
echo "6.MATE"
echo "7.Cinnamon"
echo "8.Budgie"
echo "9.Awesome"
echo "0.Skip"
read de
