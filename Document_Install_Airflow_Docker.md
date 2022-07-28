## DOWNLOAD DOCKER DESKTOP, DOCKER COMPOSE (include in Window/MacOS)

### check installation
docker --version
</br>
docker-compose --version
</br>
</br>

## DOWNLOAD DOCKER-COMPOSE FILE
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.0.1/docker-compose.yaml'
</br>
</br>
//Trong file docker-compose.yaml có thể chỉnh sửa các tham số như db, executor,..
</br>
// (nếu lỗi, chạy: Remove-item alias:curl trước)
</br>
</br>

## TẠO FOLDER dags, logs, plugins
mkdir ./dags ./logs ./plugins
</br>
</br>

## CHẠY CONTAINERS WITH AIRFLOW
docker-compose up airflow-init (khởi tạo)
</br>
</br>
docker-compose up -d 	
</br>
// (in detached mode, runnings container in background, sau đó chỉ việc mở localhost:8080)
</br>
</br>
docker-compose down -v
</br>
// (có nghĩa là không chỉ tắt airflow container mà còn removes volumnes đã tạo)
</br>
</br>
docker-compose down --volumes --rmi all 
</br>
// (To stop and delete containers, delete volumes with database data and download images)