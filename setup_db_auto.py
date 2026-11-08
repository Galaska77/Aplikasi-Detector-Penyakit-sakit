import pymysql
import sys
from werkzeug.security import generate_password_hash

def setup_database():
    """Setup database MySQL untuk sistem sawit DBSCAN"""
    
    # Konfigurasi database
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Ubah sesuai password MySQL Anda
        'charset': 'utf8mb4'
    }
    
    try:
        # Koneksi ke MySQL server
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        print("✓ Terhubung ke MySQL server")
        
        # Buat database
        cursor.execute("CREATE DATABASE IF NOT EXISTS sawit_dbscan")
        print("✓ Database 'sawit_dbscan' berhasil dibuat")
        
        # Gunakan database
        cursor.execute("USE sawit_dbscan")
        
        # Buat tabel users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Tabel 'users' berhasil dibuat")
        
        # Buat tabel analysis_results
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                input_data TEXT NOT NULL,
                cluster_result INT NOT NULL,
                analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        print("✓ Tabel 'analysis_results' berhasil dibuat")
        
        # Cek apakah data sudah ada
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO users (username, email, password) VALUES 
                (%s, %s, %s)
            """, ('admin', 'admin@sawit.com', generate_password_hash('admin')))
            
            cursor.execute("""
                INSERT INTO users (username, email, password) VALUES 
                (%s, %s, %s)
            """, ('test', 'test@sawit.com', generate_password_hash('test')))
            
            print("✓ Sample data berhasil dimasukkan")
        else:
            print("✓ Sample data sudah ada")
        
        # Commit perubahan
        connection.commit()
        print("✓ Database setup selesai!")
        
    except pymysql.Error as e:
        print(f"✗ Error database: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error umum: {e}")
        sys.exit(1)
    finally:
        if 'connection' in locals():
            connection.close()
            print("✓ Koneksi database ditutup")

if __name__ == "__main__":
    print("=== Setup Database Sistem Sawit DBSCAN ===")
    print("Pastikan MySQL server sudah berjalan!")
    print()
    
    setup_database()
    
    print()
    print("=== Setup Selesai ===")
    print("Sekarang Anda bisa menjalankan aplikasi dengan: py app_simple.py")
    print("Login dengan: admin/admin atau test/test")













