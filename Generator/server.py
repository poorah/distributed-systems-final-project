from flask import Flask, request, jsonify

app = Flask(__name__)

# لیست برای ذخیره داده‌های دریافت شده
data_store = []


@app.route('/ingest', methods=['POST'])
def ingest_data():
    """مدیریت درخواست POST برای دریافت داده‌ها"""
    try:
        # استخراج داده‌های JSON از درخواست
        data = request.get_json()
        if data:
            data_store.clear()
            data_store.append(data)
            return jsonify({"message": "Data ingested successfully"}), 200
        else:
            return jsonify({"error": "Invalid data"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/ingest', methods=['GET'])
def fetch_data():
    """مدیریت درخواست GET برای ارسال داده‌ها"""
    try:
        # بازگشت تمام داده‌های ذخیره‌شده
        return jsonify(data_store), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
