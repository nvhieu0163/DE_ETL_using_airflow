# Cài đặt Airflow trên Linux

## Window subsystem for linux

dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
</br>
</br>
// (after that, restart the computer)
</br>
</br>
// Install and open Ubuntu
</br>
</br>
sudo apt update && sudo apt upgrade
</br>
</br>

## config how the window mounted to Linux

sudo nano /etc/wsl.conf   (nano la lenh edit trong linux)
</br>
</br>

[automount]
root = /
options = "metadata"

// Ctrl S to save, Ctrl X to exit


## install pip
sudo apt install python3-pip


## Install apache-airflow using pip
</br>
</br>
pip3 install "apache-airflow[,,]==2.3.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.3.3/constraints-3.8.txt"
</br>
</br>

//trong đó:
</br>
</br>
https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt


## SET airflow-home
export AIRFLOW_HOME=~/airflow


## SET airflow_home permanent (dai han)
nano ~/.bashrc
</br>
//ben trong file bashrc
</br>
</br>
export AIRFLOW_HOME=~/airflow
</br>
</br>
//(relaunch ubuntu)


## kiem tra airflow_home
</br>
echo $AIRFLOW_HOME

## Tao tai khoan
</br>
airflow users create --username admin --firstname Hieu --lastname Nguyen --role Admin --email nguyenvuhieu2015@gmail.com

## Run webserver port 8080
</br>
airflow webserver -p 8080

## Run scheduler
</br>
airflow scheduler
------------------------------------------------------------------------------------------

IN WINDOW

*Truy cập airflow trên linux thông qua link: \\wsl$\Ubuntu\home\user_name