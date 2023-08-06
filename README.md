**Warning: This is the developement branch.Changes here may not be fully tested,so I recommend using the `master` branch for more critical installs.**
# TAIGA
Taiga or Terminal Application for Installing Graphical Appliances is a terminal script for configuring a desktop environment on the system.

## Status:Alpha
The script is currrently in an alpha state.Use on a production machine is not recommended for the following reasons:
- More testing needs to be done
- Desktop Environment support is inconsistent across distros
- The script has some dependencies needed before running
- Methods for detecting distros/GPUs (for the express installer) may be inaccurate

## Installer types
**1.Express install:** The script will detect the distro and the GPU used,and you can pick the desktop environment,which will be installed with the appropriate display manager.

**2.Custom install:** Pick all options manually.Useful if auto-detection doesn't work or if some components are not needed

Aditionally you can run the script in diffrent modes by adding these arguments after the script:

**Argument 1:**
- *s* : Simulation mode-no changes will be done to the system
- *d* : Debug mode-shows the commands and then runs them
- *r* : Runs the script normally,same as with no arguments
- *h* : shows this screen and exits
## Prerequisites
The script requires `python`,`sudo` and `pciutils` in order to run.To configure sudo you can use the following guides:

Linux: https://www.linuxteck.com/steps-to-configure-sudo-in-linux/

FreeBSD: https://www.cyberciti.biz/faq/freebsd-install-sudo-command/

Here are commands for installing these dependencies on the supported distros:
### Arch Linux
```sh
sudo pacman -S python sudo pciutils
```
Aditionally make sure that the `multilib` repository is enabled,as this is where most graphics drivers are pulled from.To do that uncomment these lines (remove the `#` symbol before each line) in `/etc/pacman.conf`:
```
[multilib]
Include = /etc/pacman.d/mirrorlist
```
### Debian/Ubuntu

```sh
sudo apt install python sudo pciutils
```
### FreeBSD

```sh
sudo pkg install python sudo pciutils
```

## Running the script
Currently there are two ways to run the script:

### Method 1:Using python
```sh
python3 taiga.py [args]
```
or
```sh
python taiga.py [args]
```

### Method 2:Using shell commands
```sh
chmod +X taiga.py #only run once
./taiga.py [args]
```
Note:This method does not work on FreeBSD as all user-installed binaries are stored in `/usr/local/bin`,as opposed to `/usr/bin`.FreeBSD users must use **Method 1**.