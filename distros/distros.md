# Packages
This folder contains JSON files related to every distro,graphics vendor,display manager and desktop environment.These files follow this structure:

```
{
    "name":"",
    "installer": "",
    "services" : "",
    "identify" : "",
    "base" : [],
    "pre" : [],
    "post" : [],
    "GD" : [
        {
            "name" : "",
            "packages" : []
        }
    ],
    "DM":[
        {
            "name":"",
            "service":"",
            "packages":[]
        }
    ],
    "DE":[
        {
            "name":"",
            "DM":"",
            "packages": [],
            "preconf": []
        }
    ]
}

```