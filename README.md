# python-init-template
python init template

## Setup

1. Add executable permisssion for `start.sh`, `install.sh`
   - `chmod a+x start.sh`
   - `chmod a+x install.sh`
2. To execute `./start --args` or `./start.sh --args`
   - `./start.sh --entity AU --env sit`
   - `./start --entity AU --env sit`

## Deployment + execution
You need to execute two commands after a new deployment
1. install depenencies
2. script entrance

## MongoDB script query
```
{ "hashcode": { "$eq": "3aa4159ad3c5bb47fe6de42b1ed6234f43475974ee479f126a55ab5a4baa9cdc911e8c0a1431102eccbc8a395d99591b0a66b403b6de31b107481f4fbbbf71f0" }, "update_datetime": -1 }
```