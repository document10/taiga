This folder contains JSON files related to every distro,graphics vendor,display manager and desktop environment.These files follow this structure:

```
{
    "name":"",
    "identify" : "",
    "order" : 0,
    "pre" : [],
    "post" : [],
    "GD" : [
        {
            "name" : "",
            "comm" : []
        }
    ],
    "DM":[
        {
            "name":"",
            "comm":[]
        }
    ],
    "DE":[
        {
            "name":"",
            "DM":"",
            "comm": [],
        }
    ]
}

```