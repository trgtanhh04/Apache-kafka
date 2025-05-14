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

--
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
  <img src="https://raw.githubusercontent.com/trgtanhh04/Apache-kafka/main/images/workflow.png" width="100%" alt="airflow">
</p>

