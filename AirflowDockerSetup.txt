#DOWNLOAD DOCKER DESKTOP, DOCKER COMPOSE (include in Window/MacOS)

docker --version

docker-compose --version

#DOWNLOAD DOCKER-COMPOSE FILE
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.0.1/docker-compose.yaml'

Trong file docker-compose.yaml có thể chỉnh sửa các tham số như db, executor,..

(nếu lỗi, chạy: Remove-item alias:curl trước)

#TẠO FOLDER dags, logs, plugins
mkdir ./dags ./logs ./plugins


#CHẠY CONTAINERS WITH AIRFLOW
docker-compose up airflow-init (khởi tạo)

docker-compose up -d 	(in detached mode, runnings container in background, sau đó chỉ việc mở localhost:8080)

docker-compose down -v  (có nghĩa là không chỉ tắt airflow container mà còn removes volumnes đã tạo)

docker-compose down --volumes --rmi all (To stop and delete containers, delete volumes with database data and download images)