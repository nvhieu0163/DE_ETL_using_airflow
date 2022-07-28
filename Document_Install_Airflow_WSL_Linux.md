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
</br>
root = /
</br>
options = "metadata"

// Ctrl S to save, Ctrl X to exit
</br>
</br>
## install pip
sudo apt install python3-pip
</br>
</br>

## install apache-airflow using pip
pip3 install "apache-airflow[,,]==2.3.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.3.3/constraints-3.8.txt"
</br>
</br>

//trong đó:
</br>
</br>
<pre>https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt </pre>
</br>
</br>

## SET airflow-home
export AIRFLOW_HOME=~/airflow
</br>
</br>

## SET airflow_home permanent (dai han)
nano ~/.bashrc
</br>
</br>
//ben trong file bashrc
</br>
export AIRFLOW_HOME=~/airflow
</br>
</br>
//(relaunch ubuntu)
</br>
</br>

## kiem tra airflow_home
echo $AIRFLOW_HOME
</br>
</br>

## Tao tai khoan
airflow users create --username admin --firstname Hieu --lastname Nguyen --role Admin --email nguyenvuhieu2015@gmail.com
</br>
</br>

## Run webserver port 8080
airflow webserver -p 8080
</br>
</br>

## Run scheduler
airflow scheduler
</br>
</br>

------------------------------------------------------------------------------------------
</br>

## IN WINDOW
</br>
*Truy cập airflow trên linux thông qua link: \\wsl$\Ubuntu\home\user_name