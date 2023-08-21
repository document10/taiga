# TAIGA
Taiga or Terminal Application for Installing Graphical Appliances is a terminal program for configuring a desktop environment,sound server and other useful components on the system.The application is controlled using the keyboard and you will see what keys to press for performing actions in the app.
## Running TAIGA
For running the program you will need `sudo` and `pciutils` installed on the system.Guides for installing and checking if these components are installed are available on the wiki.  
### Running from binary
The `master` or `dev` branches won't include binaries by default,instead those are included on the `bin` branches which contain only the binary specific to the platform.To get the `Linux` binary run:
```
git clone https://github.com/document10/taiga -b bin_linux
```
And for the `FreeBSD` binary run:
```
git clone https://github.com/document10/taiga -b bin_fbsd
```
The binaries are also avalaible on the [Releases](https://github.com/document10/taiga/releases) page.  
After getting the binary relevant to your system,ensure you have enough rights to run the binary using:

```sh
sudo chmod 777 taiga
```
Running the script is pretty straightforward:
```sh
./taiga
```
You can also load a config created with the script using:
```sh
./taiga [configfile]
```
where [configfile] is the path to the config. 
### Running from source
You will additionally need the latest version of python as well as `simple-term-menu` as a `pip` library.Instructions on setting up those are on the wiki.