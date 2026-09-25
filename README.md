

```
███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗     ██╗  ██╗███████╗ █████╗ ██╗  ████████╗██╗  ██╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗    ██║  ██║██╔════╝██╔══██╗██║  ╚══██╔══╝██║  ██║    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝    ███████║█████╗  ███████║██║     ██║   ███████║    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗    ██╔══██║██╔══╝  ██╔══██║██║     ██║   ██╔══██║    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║    ██║  ██║███████╗██║  ██║███████╗██║   ██║  ██║    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝


A simple Python CLI utility for monitoring system health.

The program automatically collects **CPU, RAM, and disk usage**, compares the results against predefined thresholds, and determines the overall system status.
```
## Features

* Automatically collects CPU usage
* Automatically collects RAM usage
* Automatically collects disk usage
* Determines the overall system status:

  * `OK`
  * `WARNING`
  * `CRITICAL`
* Returns an exit code based on the overall system status
* Allows multiple health checks during a single run
* Uses `psutil` to collect system metrics

## How It Works

The program checks three main system resources:

| Resource |    OK | WARNING | CRITICAL |
| -------- | ----: | ------: | -------: |
| CPU      | < 80% |  80–90% |    > 90% |
| RAM      | < 80% |  80–90% |    > 90% |
| Disk     | < 90% |  90–95% |    > 95% |

The overall system status is determined by the status of each resource:

* All resources are `OK` → `OK`
* At least one resource is `WARNING` → `WARNING`
* At least one resource is `CRITICAL` → `CRITICAL`

## Exit Codes

The program returns an exit code based on the overall system status:

| Exit Code | Status     |
| --------: | ---------- |
|       `0` | `OK`       |
|       `1` | `WARNING`  |
|       `2` | `CRITICAL` |

## Example

```text
================================
      Server Health Checker
================================

Running health check...


CPU: 20.4% ---- OK
Memory: 36.8% ---- OK
Disk: 18.9% ---- OK

Overall status: OK

Run another check? [y/n]:
```

## Requirements

* Python 3
* `psutil`

Install the dependency:

```bash
pip install psutil
```

## Usage

```bash
python3 server_health_checker.py
```

## Technologies

* Python
* psutil
* Linux
* Git


