from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'sawit_dbscan_secret_key'

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sawit_dbscan'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Sample data gejala sawit untuk demonstrasi
SAWIT_SYMPTOMS_DATA = {
    'features': [
        'daun_menguning', 'daun_bercak_coklat', 'daun_kering', 'daun_gugur',
        'batang_berlubang', 'batang_bercak', 'akar_busuk', 'akar_hitam',
        'buah_busuk', 'buah_bercak', 'pertumbuhan_lambat', 'produksi_turun'
    ],
    'data': [
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],  # Gejala ringan
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # Gejala sedang
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],  # Gejala berat
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],  # Penyakit akar
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Gejala ringan daun
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Gejala sedang daun
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Gejala berat daun
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],  # Penyakit buah
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Kombinasi ringan
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],  # Kombinasi sedang
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Penyakit parah
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Sehat
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Gejala awal
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Gejala daun ringan
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0],  # Gejala batang
    ]
}

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Password tidak cocok!', 'error')
            return render_template('register.html')
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cur.fetchone()
        
        if existing_user:
            flash('Username atau email sudah digunakan!', 'error')
            cur.close()
            return render_template('register.html')
        
        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                   (username, email, hashed_password))
        mysql.connection.commit()
        cur.close()
        
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout!', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

@app.route('/input_data')
def input_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('input_data.html', features=SAWIT_SYMPTOMS_DATA['features'])

@app.route('/process_data', methods=['POST'])
def process_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Ambil data dari form
    symptoms_data = []
    for feature in SAWIT_SYMPTOMS_DATA['features']:
        value = request.form.get(feature, 0)
        symptoms_data.append(int(value))
    
    # Tambahkan data baru ke dataset
    new_data = SAWIT_SYMPTOMS_DATA['data'] + [symptoms_data]
    
    # Konversi ke DataFrame
    df = pd.DataFrame(new_data, columns=SAWIT_SYMPTOMS_DATA['features'])
    
    # Normalisasi data
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)
    
    # Terapkan DBSCAN
    dbscan = DBSCAN(eps=0.5, min_samples=3)
    clusters = dbscan.fit_predict(df_scaled)
    
    # Analisis hasil
    n_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
    n_noise = list(clusters).count(-1)
    
    # Prediksi untuk data baru (yang terakhir)
    new_cluster = clusters[-1]
    
    # Simpan hasil ke database
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO analysis_results (user_id, input_data, cluster_result, analysis_date)
        VALUES (%s, %s, %s, %s)
    """, (session['user_id'], str(symptoms_data), int(new_cluster), datetime.now()))
    mysql.connection.commit()
    cur.close()
    
    # Buat visualisasi
    plot_url = create_visualization(df_scaled, clusters, SAWIT_SYMPTOMS_DATA['features'])
    
    # Interpretasi hasil
    interpretation = interpret_cluster_result(new_cluster, symptoms_data)
    
    return render_template('results.html', 
                         cluster=new_cluster,
                         n_clusters=n_clusters,
                         n_noise=n_noise,
                         interpretation=interpretation,
                         plot_url=plot_url,
                         symptoms_data=symptoms_data)

def create_visualization(data, clusters, features):
    plt.figure(figsize=(12, 8))
    
    # Plot 2D menggunakan PCA untuk visualisasi
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    data_pca = pca.fit_transform(data)
    
    unique_clusters = set(clusters)
    colors = plt.cm.Set3(np.linspace(0, 1, len(unique_clusters)))
    
    for i, cluster in enumerate(unique_clusters):
        if cluster == -1:
            plt.scatter(data_pca[clusters == cluster, 0], 
                       data_pca[clusters == cluster, 1], 
                       c='black', marker='x', s=100, label='Noise')
        else:
            plt.scatter(data_pca[clusters == cluster, 0], 
                       data_pca[clusters == cluster, 1], 
                       c=[colors[i]], label=f'Cluster {cluster}', s=100)
    
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title('DBSCAN Clustering Results - Sawit Symptoms')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Simpan plot ke string
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=150, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url

def interpret_cluster_result(cluster, symptoms_data):
    interpretations = {
        -1: "Data tidak masuk ke cluster manapun (Noise) - Kemungkinan gejala unik atau kombinasi gejala yang jarang terjadi",
        0: "Cluster 0 - Gejala ringan pada daun dengan sedikit dampak pada produksi",
        1: "Cluster 1 - Gejala sedang dengan kombinasi masalah daun dan batang",
        2: "Cluster 2 - Gejala berat dengan dampak signifikan pada seluruh tanaman",
        3: "Cluster 3 - Penyakit akar yang mempengaruhi sistem perakaran"
    }
    
    base_interpretation = interpretations.get(cluster, f"Cluster {cluster} - Pola gejala yang teridentifikasi")
    
    # Analisis gejala spesifik
    symptom_analysis = []
    if symptoms_data[0] == 1:  # daun_menguning
        symptom_analysis.append("Daun menguning terdeteksi")
    if symptoms_data[1] == 1:  # daun_bercak_coklat
        symptom_analysis.append("Bercak coklat pada daun terdeteksi")
    if symptoms_data[6] == 1:  # akar_busuk
        symptom_analysis.append("Gejala pembusukan akar terdeteksi")
    if symptoms_data[8] == 1:  # buah_busuk
        symptom_analysis.append("Pembusukan buah terdeteksi")
    
    if symptom_analysis:
        base_interpretation += f"\n\nGejala spesifik yang terdeteksi:\n" + "\n".join(symptom_analysis)
    
    return base_interpretation

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM analysis_results 
        WHERE user_id = %s 
        ORDER BY analysis_date DESC
    """, (session['user_id'],))
    results = cur.fetchall()
    cur.close()
    
    return render_template('history.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)



