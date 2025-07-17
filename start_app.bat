@echo off

:wait_docker
docker info >nul 2>&1
if errorlevel 1 (
    timeout /t 5 >nul
    goto wait_docker
)

cd /d C:\Users\user\PycharmProjects\EventsReminder
docker-compose -f standalone.yml stop

docker-compose -f standalone.yml up -d
