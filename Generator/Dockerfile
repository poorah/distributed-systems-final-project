# انتخاب پایه‌ای‌ترین ایمیج
FROM python:3.12.3-slim

WORKDIR /app

COPY . /app

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir flask requests numpy psutil

EXPOSE 5000

COPY run.sh /app/run.sh

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
 
