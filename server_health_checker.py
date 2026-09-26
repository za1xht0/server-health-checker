import sys
import psutil
import platform
import argparse
from pathlib import Path
import yaml
import logging


logging.basicConfig(filename='server_health_checker.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(description='Server Health Checker')
    parser.add_argument('-c', '--config', 
                        type=str, 
                        required=True, 
                        help='path to configuration file'
                        )
    parser.add_argument('-o', '--once', 
                        action='store_true', 
                        help='run a single health check and exit'
                        )
    args = parser.parse_args()
    once = args.once
    cfg_path = Path(args.config)
    return cfg_path, once 

def load_config(cfg_path):
    if not cfg_path.exists():
        logging.error(f"Configuration file '{cfg_path}' not found")
        sys.exit(4) 

    with open(cfg_path, 'r') as file:
        config = yaml.safe_load(file)
        return config

def validate_config(config):
    if not {'resources', 'disk'}.issubset(config):
        return False
    if not {'warning', 'critical'}.issubset(config['resources']):
        return False
    if not {'warning', 'critical'}.issubset(config['disk']):
        return False
    if not isinstance(config['resources']['warning'], (int, float)) or \
        not isinstance(config['resources']['critical'], (int, float)) or \
        not isinstance(config['disk']['warning'], (int, float)) or \
        not isinstance(config['disk']['critical'], (int, float)):
        return False
    if config['resources']['warning'] <= 0 or config['resources']['warning'] > 100 or \
        config['resources']['critical'] <= 0 or config['resources']['critical'] > 100 or \
        config['disk']['warning'] <= 0 or config['disk']['warning'] > 100 or \
        config['disk']['critical'] <= 0 or config['disk']['critical'] > 100:
        return False
    if config['resources']['warning'] >= config['resources']['critical'] or \
        config['disk']['warning'] >= config['disk']['critical']:
        return False
    return True

def get_disk_path():
    if platform.system() == 'Linux':
        return '/home'
    elif platform.system() == 'Windows':
        return 'C:\\'
    elif platform.system() == 'Darwin':
        return '/Users'
    else:
        logging.error('Unsupported operating system')
        sys.exit(1)

def cpu_check(cpu, resources_warning, resources_critical):
    if cpu < resources_warning:
        return 'OK'
    elif cpu <= resources_critical:
        return 'WARNING'
    else:
        return 'CRITICAL'

def ram_check(ram, resources_warning, resources_critical):
    if ram < resources_warning:
        return 'OK'
    elif ram <= resources_critical:
        return 'WARNING'
    else:
        return 'CRITICAL'

def disk_check(disk, disk_warning, disk_critical):
    if disk < disk_warning:
        return 'OK'
    elif disk <= disk_critical:
        return 'WARNING'
    else:
        return 'CRITICAL'

def overall_status(crd):
    if 'CRITICAL' in crd.values():
        return 'CRITICAL'
    elif 'WARNING' in crd.values():
        return 'WARNING'
    else:
        return 'OK'

def log_result(name, value, result):
    if result == 'CRITICAL':
        logging.error(f'{name} usage: {value}% - {result}')
    elif result == 'WARNING':
        logging.warning(f'{name} usage: {value}% - {result}')
    else:
        logging.info(f'{name} usage: {value}% - {result}')

def get_exit_code(status):
    if status == 'OK':
        return 0
    elif status == 'WARNING':
        return 1
    elif status == 'CRITICAL':
        return 2
    elif status == 'UNKNOWN':
        return 3

def process_checks(cpu, ram, disk, thresholds):
    cpu_result = cpu_check(cpu, thresholds['resources_warning'], thresholds['resources_critical'])
    ram_result =  ram_check(ram, thresholds['resources_warning'], thresholds['resources_critical'])
    disk_result =  disk_check(disk, thresholds['disk_warning'], thresholds['disk_critical'])
    crd = {
            "cpu": cpu_result,
            "ram": ram_result,
            "disk": disk_result
        }
    log_result("CPU", cpu, cpu_result)
    log_result("RAM", ram, ram_result)
    log_result("DISK", disk, disk_result)
    status = overall_status(crd)
    exit_code = get_exit_code(status)
    return f'\nCPU: {cpu}% ---- {cpu_result}\nMemory: {ram}% ---- {ram_result}\nDisk: {disk}% ---- {disk_result}\n\nOverall status: {status}\n', exit_code

def get_system_metrics(disk_path):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage(disk_path).percent
    return cpu, ram, disk

def main():
    print('\n================================\n      Server Health Checker      \n================================\n')
    cfg_path, once = parse_args()
    config = load_config(cfg_path)
    if not validate_config(config):
        logging.error('Invalid configuration')
        sys.exit(5)
    logging.info('Running health check...\n')
    disk_path = get_disk_path()
    thresholds = {
    'resources_warning': config['resources']['warning'],
    'resources_critical': config['resources']['critical'],
    'disk_warning': config['disk']['warning'],
    'disk_critical': config['disk']['critical']
    }

    while True:
        cpu, ram, disk = get_system_metrics(disk_path)
        res, exit_code = process_checks(cpu, ram, disk, thresholds)
        print(res)
        if once:
            break
        else:
            is_on = input('Run another check? [y/n]: ').lower()
            if is_on == 'n':
                break
    sys.exit(exit_code)

if __name__ == '__main__':
    main()



