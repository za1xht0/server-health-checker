```
 ▄▄▄▄▄▄▄ ▄▄▄   ▄▄▄  ▄▄▄▄▄▄▄ 
█████▀▀▀ ███   ███ ███▀▀▀▀▀ 
 ▀████▄  █████████ ███      
   ▀████ ███▀▀▀███ ███      
███████▀ ███   ███ ▀███████ 
```

# Server Health Checker
 
CLI-утилита на Python для мониторинга состояния Linux-системы.

Проект создан для практики Python и DevOps: мониторинг, YAML-конфигурация, логирование, тестирование, Bash и systemd.

# Возможности
* Мониторинг CPU, RAM и диска
* Проверка состояния системных сервисов
* Статусы OK, WARNING, CRITICAL
* YAML-конфигурация и её валидация
* Логирование
* Коды завершения
* Однократный и непрерывный режимы
* Обработка Ctrl+C
* Автоматические тесты с pytest
* Запуск как systemd-сервис
* Автоматический перезапуск через Restart=on-failure
* Скрипты установки и удаления сервиса

# Установка

```bash
git clone https://github.com/za1xht0/server-health-checker.git 
cd server-health-checker 
pip install -r requirements.txt
```
## Требования:
* Linux
* Python 3.10+
* pip

# Конфигурация

Создать локальную конфигурацию из примера:

```bash
cp config/config.example.yaml config/config.yaml
```

# Использование

Однократная проверка:
```bash
python server_health_checker.py --config config/config.yaml --once
```

Непрерывный мониторинг:
```bash
python server_health_checker.py --config config/config.yaml
```

Короткая форма:
```bash
python server_health_checker.py -c config/config.yaml -o
```

Для остановки непрерывного режима используется Ctrl+C.

# Коды завершения

| Код   | Значение                             |
| ----- | ------------------------------------ |
| `0`   | OK                                   |
| `1`   | WARNING                              |
| `2`   | CRITICAL                             |
| `4`   | Конфигурационный файл не найден      |
| `5`   | Некорректная конфигурация            |
| `130` | Программа остановлена через `Ctrl+C` |

# systemd

Установить сервис:
```
sudo ./scripts/install.sh
```

Проверить состояние:
```
systemctl status server-health-checker.service
```

Посмотреть логи:
```
journalctl -u server-health-checker.service
```

Удалить сервис:
```
sudo ./scripts/uninstall.sh
```

Сервис использует:
```
Restart=on-failure
RestartSec=5
```