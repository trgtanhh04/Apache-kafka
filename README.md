# Apache kafka

## Giới thiệu

**Apache Kafka** là một nền tảng xử lý streaming dữ liệu phân tán, được thiết kế để xử lý các luồng dữ liệu lớn theo thời gian thực. Kafka thường được sử dụng trong các hệ thống có nhu cầu xử lý dữ liệu tốc độ cao, đảm bảo tính tin cậy và khả năng mở rộng. Một số ứng dụng phổ biến của Kafka bao gồm:
- **Truyền dữ liệu sự kiện (Event Streaming)**: Chuyển các sự kiện từ hệ thống này sang hệ thống khác.
- **Xử lý dữ liệu thời gian thực**: Phân tích dữ liệu ngay khi nó được tạo ra.
- **Hệ thống log tập trung**: Lưu trữ và xử lý log từ nhiều nguồn khác nhau.

**Thành phần chính của Kafka**:
- **Producer**: Gửi dữ liệu (messages) tới Kafka.
- **Consumer**: Đọc và xử lý dữ liệu từ Kafka.
- **Broker**: Máy chủ trung gian chịu trách nhiệm lưu trữ và gửi dữ liệu.
- **Topic**: Nơi dữ liệu được tổ chức và lưu trữ. Các Producer gửi dữ liệu vào các Topic, và các Consumer đọc dữ liệu từ các Topic.

---
## Mục tiêu của dự án
Dự án này minh họa cách sử dụng Kafka kết hợp với Spark và PostgreSQL để xây dựng một pipeline xử lý dữ liệu thời gian thực. Hệ thống sẽ:
1. Gửi dữ liệu từ Producer đến Topic Kafka.
2. Consumer đọc dữ liệu từ Topic và xử lý bằng Spark.
3. Lưu trữ dữ liệu đã xử lý vào PostgreSQL và xuất ra file CSV.
---

## Cấu trúc cây thư mục

```
KAFKA-DEMO
├── images                    # Thư mục chứa hình ảnh minh họa
│   ├── consumer.png          # Mô tả hoạt động của Consumer
│   ├── workflow.png          # Minh họa luồng hoạt động của hệ thống
├── output_data               # Thư mục chứa dữ liệu xử lý đầu ra
│   ├── part-00000-*.csv      # Dữ liệu được Spark ghi dưới dạng CSV
├── src                       # Thư mục chứa mã nguồn chính
│   ├── consumer.py           # Consumer: Đọc dữ liệu từ Kafka và xử lý
│   ├── producer.py           # Producer: Gửi dữ liệu đến Kafka
├── docker-compose.yml        # Cấu hình Docker Compose cho Kafka, Spark, PostgreSQL
├── instruction.txt           # Hướng dẫn sử dụng hoặc ghi chú dự án
├── README.md                 # Tài liệu mô tả dự án
├── requirements.txt          # Danh sách thư viện Python cần cài đặt
```

---
## Kiến trúc pipeline
<p align="center">
  <img src="https://raw.githubusercontent.com/trgtanhh04/Apache-kafka/main/images/workflow.jpg" width="100%" alt="airflow">
</p>

#### **Giải thích Workflow**
- **Web API (Nguồn dữ liệu)**:
   - Dữ liệu được lấy từ API công khai [Random User API](https://randomuser.me/api/). 
   - API này cung cấp thông tin ngẫu nhiên về người dùng như tên, địa chỉ, email, ngày sinh, v.v.

- **Apache Kafka**:
   - Dữ liệu từ API được gửi đến **Kafka** thông qua **Producer**.
   - Kafka lưu trữ dữ liệu trong các **Topic**, cho phép các hệ thống hạ nguồn (downstream) xử lý dữ liệu.
    
- **Apache Zookeeper**:
   - Zookeeper được sử dụng để quản lý metadata và điều phối hoạt động của Kafka.
   - 
- **Apache Spark**:
   - **Spark Streaming** được sử dụng để xử lý dữ liệu thời gian thực từ Kafka.
   - Hệ thống Spark có một **Master** và nhiều **Worker**, nơi Master phân phối công việc đến các Worker để xử lý dữ liệu.

- **PostgreSQL**:
   - Sau khi dữ liệu được xử lý bởi Spark, nó được lưu trữ vào cơ sở dữ liệu **PostgreSQL** để dễ dàng truy vấn và phân tích.

---
## Cài đặt dự án

### **1. Clone Repository**
Đầu tiên, clone repository về máy của bạn:
```bash
git clone https://github.com/trgtanhh04/Apache-kafka.git
cd Apache-kafka
```


### **2. Cài đặt Docker**
Docker sẽ được sử dụng để khởi chạy các dịch vụ như Kafka, Zookeeper, PostgreSQL và Spark.

- **Tải Docker Desktop**:
  - Truy cập [Docker Desktop](https://www.docker.com/products/docker-desktop/) và tải phiên bản phù hợp với hệ điều hành của bạn.
  - Thực hiện cài đặt theo hướng dẫn trên website.

- **Kiểm tra Docker đã cài đặt**:
  - Chạy lệnh sau để đảm bảo Docker đã được cài đặt và đang hoạt động:
    ```bash
    docker --version
    ```


### **3. Khởi chạy môi trường Docker**
Sử dụng file `docker-compose.yml` để thiết lập môi trường:
1. Khởi động các dịch vụ:
   ```bash
   docker-compose up -d
   ```
   Lệnh này sẽ khởi chạy các container cần thiết, bao gồm Kafka, Zookeeper, Spark và PostgreSQL.

2. Kiểm tra các container đang chạy:
   ```bash
   docker ps
   ```

3. Nếu cần dừng các dịch vụ:
   ```bash
   docker-compose down
   ```


### **4. Cài đặt các công cụ cần thiết**
Đảm bảo các công cụ sau đã được cài đặt trên máy cục bộ của bạn:

- **Python 3.8 hoặc cao hơn**:
  - Yêu cầu để chạy các script Python.
  - Kiểm tra phiên bản Python:
    ```bash
    python --version
    ```
  - Cài đặt các thư viện Python cần thiết:
    ```bash
    pip install -r requirements.txt
    ```

- **Java 11**:
  - Yêu cầu để chạy Apache Spark.
  - Kiểm tra phiên bản Java:
    ```bash
    java -version
    ```
  - Nếu chưa cài đặt, bạn có thể tải và cài đặt từ [AdoptOpenJDK](https://adoptopenjdk.net/).


### **5. Lấy dữ liệu từ API**
- Dữ liệu người dùng sẽ được lấy từ API công khai [Random User API](https://randomuser.me/api/), sau đó đẩy vào Kafka thông qua **Producer**.
- Bạn có thể kiểm tra API bằng cách mở trình duyệt hoặc sử dụng lệnh:
  ```bash
  curl https://randomuser.me/api/
  ```


### **6. Chạy ứng dụng**
- **Producer**:
  Gửi dữ liệu từ API vào Kafka:
  ```bash
  python src/producer.py
  ```
- **Consumer**:
  Đọc dữ liệu từ Kafka, xử lý bằng Spark và lưu vào PostgreSQL:
  ```bash
  python src/consumer.py
  ```



### **7. Kiểm tra kết quả**
- File CSV đầu ra sẽ được lưu trong thư mục `output_data`.
- Dữ liệu đã xử lý được lưu trữ trong cơ sở dữ liệu **PostgreSQL**. Bạn có thể kết nối đến PostgreSQL để kiểm tra:
  ```bash
  docker exec -it <container_id_postgres> psql -U postgres -d userdb
  ```
