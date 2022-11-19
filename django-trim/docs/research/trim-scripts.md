
Easily abstract a script into a cli function by writing a directory of assets for the script to call into.

1. create a file as a script `/home/user/restart_nginx.sh`
2. Allocate the directory to `trim`: `trim scripts add location path`
3. run the script `trim restart nginx`

A script should accept params if required


An example script: `certbot_install.sh`

```sh
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot
echo "Install by owner {owner}"
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

install:

```bash
$ trim scripts add certbot_install.sh
# installed as alias "trim certbox install"
```

run the script:

```bash
$ trim certbot install --owner derek
# Install by owner derek
```

Inline may work similar:

```sh
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot
echo "Install by owner {args[0]}"
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

```bash
$ trim certbot install samantha
# Install by owner samantha
```
