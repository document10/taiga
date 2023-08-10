# TAIGA Distros
This page details information about each of the supported distros,including supported setups,dependencies and commands.
## Support
### Graphics Vendors
| | AMD | Intel | Nvidia | VMware/Virtualbox | VESA/Generic |
|-|-----|-------|--------|-------------------|------|
|Arch Linux|yes|yes|yes|yes|yes|
|Debian/Ubuntu|yes|yes|yes|yes|yes|
|OpenSUSE|yes|yes|yes|yes|yes|
|Fedora|yes|yes|yes|yes|yes|
|Void Linux|yes|yes|yes|yes|yes|
|FreeBSD|yes|yes|yes|Separate drivers for VMware and Virtualbox|VESA for BIOS systems,SCFB for UEFI systems|
### Desktop Environments
| | Arch Linux | Debian | Ubuntu | Fedora | OpenSUSE | Void Linux | FreeBSD |
|-|------------|--------|--------|--------|----------|------------|---------|
| Awesome | yes | yes | yes | yes | yes | yes | yes |
| Budgie | yes | yes | with Ubuntu-branded version | yes | yes | yes | yes |
| Cinnamon | yes | yes | with Ubuntu-branded version | yes | yes | yes | yes |
| Cutefish | yes | no | no | no | no | no | no | no |
| Deepin | yes | no | Ubuntu-branded version only | yes | yes | no | no |
| Enlightenment | yes | no | yes | yes | yes | yes | yes |
| GNOME | yes | yes | with Ubuntu-branded version |  yes | yes | yes | yes |
| KDE Plasma | yes | yes | with Ubuntu-branded version |  yes | yes | yes | yes |
| LXDE | yes | yes | yes |  yes | yes | yes | yes |
| LXQT | yes | yes | with Ubuntu-branded version |  yes | yes | yes | yes |
| MATE | yes | yes | with Ubuntu-branded version |  yes | yes | yes | yes |
| Pantheon | yes | no | no | no | no | no | no |
| XFCE | yes | yes | with Ubuntu-branded version |  yes | yes | yes | yes |
| Overall | 100% | 69% (nice) | 84% | 84% | 84% | 76% | 76% |

## Dependencies
Guides for configuring sudo:  
[Linux](https://www.linuxteck.com/steps-to-configure-sudo-in-linux/)  
[FreeBSD](https://www.cyberciti.biz/faq/freebsd-install-sudo-command/)
| | Arch Linux| Debian/Ubuntu | FreeBSD | OpenSUSE | Fedora | Void Linux |
|-|-----------|---------------|---------|----------|--------|------------|
| python | Manually | Preconfigured | Manually | Manually | Manually | Manual |
| pciutils | Preconfigured | Preconfigured | Manually | Preconfigured | Preconfigured | Preconfigured |
| sudo | Manually | Preconfigured(not on Debian) | Preconfigured | Preconfigured | Preconfigured | Preconfigured | 
| Commands | `pacman -S python sudo pciutils` | `apt install python sudo pciutils` | `pkg install python sudo pciutils` | `zypper install python sudo pciutils` | `dnf install python sudo pciutils`| `xbps-install python3 sudo pciutils` |

Notes:
- Aditionally for Arch Linux make sure that the `multilib` repository is enabled,as this is where most graphics drivers are pulled from.To do that uncomment these lines (remove the `#` symbol before each line) in `/etc/pacman.conf`:
```
[multilib]
Include = /etc/pacman.d/mirrorlist
```