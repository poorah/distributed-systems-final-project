# انتخاب ایمیج پایه Apache Spark با نسخه 3.5.3 و پشتیبانی Kafka
FROM bitnami/spark:3.5.3

# نصب کتابخانه‌های مورد نیاز برای Kafka
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean

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

# دستور پیش‌فرض برای اجرا (در زمان اجرا مشخص می‌شود)
CMD ["bash"]
