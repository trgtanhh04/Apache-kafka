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
### **1. Clone the Repository**
First, clone the repository to your local machine:
```bash
git clone https://github.com/trgtanhh04/Mobile-AWS-Pipeline-Engineering.git
cd Mobile-AWS-Pipeline-Engineering
```

---

### **2. Install Docker**
- **Download Docker Desktop**:
  - Go to the [Docker Desktop website](https://www.docker.com/products/docker-desktop/) and download the version suitable for your operating system.
  - Follow the instructions on the website to install Docker Desktop.
- **Verify Docker Installation**:
  - Run the following command to ensure Docker is installed and running:
    ```bash
    docker --version
    ```

---

### **3. Build the Docker Environment**
Use the `Dockerfile` and `docker-compose.yml` to set up the environment:
1. Build the Docker image:
   ```bash
   docker build -t mobile-aws-pipeline .
   ```
2. Start the services using Docker Compose:
   ```bash
   docker-compose up -d
   ```
   This will start all necessary containers, such as Apache Airflow, Kafka, and any other services defined in the `docker-compose.yml`.

---

### **4. Prerequisites**
Ensure you have the following prerequisites installed locally:
- **Java 11**:
  - Required for running Spark and other Java-based tools.
  - Verify installation:
    ```bash
    java -version
    ```
  - If not installed, download and install from [AdoptOpenJDK](https://adoptopenjdk.net/).
- **Python 3.8 or higher**:
  - Required for running the Python scripts and notebooks.
  - Verify installation:
    ```bash
    python --version
    ```
  - Install necessary Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
