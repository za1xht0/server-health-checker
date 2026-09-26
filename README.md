

```
███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗     ██╗  ██╗███████╗ █████╗ ██╗  ████████╗██╗  ██╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗    ██║  ██║██╔════╝██╔══██╗██║  ╚══██╔══╝██║  ██║    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝    ███████║█████╗  ███████║██║     ██║   ███████║    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗    ██╔══██║██╔══╝  ██╔══██║██║     ██║   ██╔══██║    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║    ██║  ██║███████╗██║  ██║███████╗██║   ██║  ██║    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

```

CLI utility for monitoring basic system health metrics.

The tool checks:
- CPU usage
- RAM usage
- Disk usage

Based on configurable thresholds, it returns health status:
- OK
- WARNING
- CRITICAL

The project is built as a practical DevOps learning project and demonstrates:
- Python CLI development
- Configuration management
- System monitoring
- Linux-oriented automation practices

---

## Features

✅ Command-line interface  
✅ YAML configuration  
✅ Configuration validation  
✅ CPU/RAM/Disk monitoring  
✅ Custom warning and critical thresholds  
✅ Exit codes for automation  
✅ Single check mode (`--once`)  
✅ Cross-platform disk path detection  

---

## Requirements

- Python 3.10+
- psutil
- PyYAML

## Install dependencies:

```bash
pip install -r requirements.txt
```
## Installation
```
git clone https://github.com/za1xht0/server-health-checker.git

cd server-health-checker
```
## Configuration

Example config.yaml:
```
resources:
  warning: 80
  critical: 90

disk:
  warning: 90
  critical: 95
```
### Configuration rules:

values must be numbers
values must be between 0 and 100
warning threshold must be lower than critical threshold

## Usage

Run continuous monitoring:
```
python server_health_checker.py --config config.yaml
```
Run a single health check:
```
python server_health_checker.py --config config.yaml --once
```
Short options:
```
python server_health_checker.py -c config.yaml -o
```
Show help:
```
python server_health_checker.py --help
```
## Example output
```
================================
      Server Health Checker
================================

Running health check...


CPU: 9.1% ---- OK
Memory: 41.4% ---- OK
Disk: 23.8% ---- OK

Overall status: OK
```
## Exit codes

The program uses exit codes for automation:

| Code | Status   |	Description                   |
|------|---------:|------------------------------:|   
| 0    |	OK      | System is healthy             |
| 1	   |WARNING	  | Warning threshold exceeded    |
| 2    |	CRITICAL|	Critical threshold exceeded   |
| 4    |	ERROR	  | Configuration file not found  |
| 5    |	ERROR   |	Invalid configuration         |

## Example:
```
echo $?
```

## Project structure
```
server-health-checker/
│
├── server_health_checker.py
├── config.yaml
├── requirements.txt
└── README.md
```