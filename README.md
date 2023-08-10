**Warning: This is the developement branch.Changes here may not be fully tested,so I recommend using the [master]([master](https://github.com/document10/taiga)) branch for more critical installs.**
# TAIGA
Taiga or Terminal Application for Installing Graphical Appliances is a terminal script for configuring a desktop environment on the system.
## Installer types
**1.Express install:** The script will detect the distro and the GPU used,and you can pick the desktop environment,which will be installed with the appropriate display manager.  
**2.Custom install:** Pick all options manually.Useful if auto-detection doesn't work or if some components are not needed  
Aditionally you can run the script in diffrent modes by adding these arguments after the script:  
- *s* : Simulation mode-no changes will be done to the system
- *l* [`filepath`]: loads configuration from the file specified in [filepath]
- *sl* / *ls* [`filepath`]: loads configuration from the file specified in [filepath] and enters Simulation mode
- *h* : shows this screen and exits
## Prerequisites
The script requires `python`,`sudo` and `pciutils` in order to run.Please check commands for installing these dependencies as well as whether they're already configured on your system or not here:  
https://github.com/document10/taiga/blob/dev/info/distros.md
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