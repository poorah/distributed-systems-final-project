FROM python:3.12.3-slim


# نصب کتابخانه‌های Python مورد نیاز
RUN pip3 install kafka-python requests

# تنظیم دایرکتوری کاری داخل کانتینر
WORKDIR /app

# کپی فایل‌های پروژه به داخل کانتینر
COPY . /app

# مشخص کردن پورت‌های Kafka و Spark
EXPOSE 9092 4040 8080

# تنظیم متغیرهای محیطی برای Spark
ENV SPARK_NO_DAEMONIZE=1
ENV SPARK_MASTER_HOST=localhost


COPY run.sh /app/run.sh

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
