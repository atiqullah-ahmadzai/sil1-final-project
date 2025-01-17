# Project Setup Guide

## Create Virtual Environment

```sh
python3.11.10 -m venv .env
```

**Note:** While you may use your preferred Python version, it is recommended to use Python 3.11.\* to ensure compatibility with dependency packages.

### Activate Virtual Environment

- **Windows**:
  ```sh
  .env\Scripts\activate
  ```
- **Linux/MacOS**:
  ```sh
  source .env/bin/activate
  ```

## Install Requirements

```sh
pip install -r requirements.txt
```

## Configure CIC Flow Meter

```sh
cd cicflowmeter
poetry install
```

## Database Migrations

### Make Migrations

From the main directory, run the following command:

```sh
python manage.py makemigrations
```

### Apply Migrations

```sh
python manage.py migrate
```

## Run Server

```sh
python manage.py runserver
```

## Manual CIC Flow Meter Testing

```sh
cicflowmeter -i "WiFi 2" -u http://localhost:8000/post_flow
```

## XDP Filter Commands Examples

```shell
# xdp-filter load eth0 -f tcp,udp
# xdp-filter port 80
```

To filter all packets **except** those from IP address fc00:dead:cafe::1 issue the following commands (careful, this can lock you out of remote access!):

```shell
# xdp-filter load eth0 -f ipv6 -p deny
# xdp-filter ip fc00:dead:cafe::1 -m src
```

To allow packets from **either** IP fc00:dead:cafe::1 **or** arriving on port 22, issue the following (careful, this can lock you out of remote access!):

```shell
# xdp-filter load eth0 -f ipv6,tcp -p deny
# xdp-filter port 22
# xdp-filter ip fc00:dead:cafe::1 -m src
```

Some other commands

xdp-filter load eth0 -f ipv4 -p deny && xdp-filter port 22
xdp-filter load eth0 -f ipv4,tcp,udp -p deny && xdp-filter ip 132.231.155.116 -m src
