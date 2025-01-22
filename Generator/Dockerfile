# انتخاب پایه‌ای‌ترین ایمیج
FROM python:3.9-slim
Python 3.12.3
WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# مشخص کردن پورت
EXPOSE 8000

# دستوری که هنگام اجرای کانتینر اجرا می‌شود
CMD ["python", "app.py"]
 
