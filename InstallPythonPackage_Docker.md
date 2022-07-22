# DOCKER INSTALL PYTHON PACKAGE
</br>
</br>

# Cách 1: Extending Image in Docker

## Tạo file 'requirements.txt'

**Thêm các package cần thiết**

scikit-learn==x.x.x
</br>
matplotlib==x.x.x

## Tạo file Docker 'Dockerfile' ngay trong folder chính
**paste this:**

FROM apache/airflow:2.0.1 </br>
COPY requirements.txt /requirements.txt </br>
RUN pip install --user --upgrade pip  (update pip version to get the lastest version) </br>
RUN pup install --no-cache-dir --user -r /requirements.txt </br>

## Chạy command interminal
**Docker xây một image sử dụng Dockerfile ngay trong thư mục hiện tại, đặt tên là extending_airflow, version: latest**
</br>
docker build . --tag extending_airflow:latest

## rename tên trong file docker-compose.yaml
Trong mục Airflow_image Name: 
đặt thành tên đã đặt build trên kia, trong trường hợp này là extending_airflow:lastest. 
lastest là tên version

## rebuild the image 
**mỗi khi change trong requirements.txt, chúng ta cần phải rebuild the image**
</br>
docker-compose up -d --no-deps --build airflow-webserver airflow-scheduler
</br>
</br>
# Cách 2: Build Apache airflow with python dependencies từ đầu.

## Ra vị trí thư mục cha.

## clone Apache Airflow source code git hub: 
git clone https://github.com/apache/airflow.git

**vào thư mục docker-context-files, thêm file 'requirements.txt' đã có các python dependencies cần thiết**

## Build airflow image: 
**đặt tên là customizing_airflow, version: latest**
docker build . --build-arg AIRFLOW_VERSION='2.0.1' --tag customizing_airflow:latest

## Chỉnh sửa tên như tên vừa đặt trong docker-compose.yaml

## chạy và build các airflow-webserver và scheduler
docker-compose up -d --no-deps --build airflow-webserver airflow-scheduler


