from flask import Flask, render_template, request, jsonify
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    pengirim = request.form.get('pengirim')
    password = request.form.get('password')
    target = request.form.get('target')
    pesan = request.form.get('pesan')
    jumlah = int(request.form.get('jumlah') or 1)

    if not pengirim or not password or not target or not pesan:
        return jsonify({'status': 'error', 'message': 'Semua field harus diisi!'})

    if not target.endswith('@gmail.com'):
        return jsonify({'status': 'error', 'message': 'Gunakan email @gmail.com!'})

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(pengirim, password.replace(' ', ''))

        kirim = 0
        gagal = 0

        for i in range(jumlah):
            try:
                subject = f"Pesan dari {random.choice(['Admin', 'Support', 'Info', 'Notifikasi', 'Penting'])} #{random.randint(1000, 9999)}"
                
                msg = MIMEMultipart()
                msg['From'] = pengirim
                msg['To'] = target
                msg['Subject'] = subject
                
                body = pesan + f"\n\n---\nID: {random.randint(100000, 999999)}\nWaktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                msg.attach(MIMEText(body, 'plain'))

                server.send_message(msg)
                kirim += 1
                time.sleep(0.5)

            except Exception as e:
                gagal += 1

        server.quit()

        return jsonify({
            'status': 'success',
            'message': f'✅ {kirim} pesan terkirim ke {target} | ❌ {gagal} gagal'
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'❌ Gagal login: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
