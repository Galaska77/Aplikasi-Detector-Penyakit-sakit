import pymysql
from datetime import datetime, timedelta
import random


def seed_history(records_per_user: int = 100):
	config = {
		'host': 'localhost',
		'user': 'root',
		'password': '',
		'database': 'sawit_dbscan',
		'charset': 'utf8mb4'
	}

	connection = pymysql.connect(**config)
	try:
		with connection.cursor() as cur:
			# Ensure users exist
			cur.execute("SELECT id, username FROM users WHERE username IN ('admin','test')")
			rows = cur.fetchall()
			username_to_id = {row[1]: row[0] for row in rows}
			if 'admin' not in username_to_id or 'test' not in username_to_id:
				raise RuntimeError("Users 'admin' and 'test' must exist before seeding.")

			# Generate records for each user
			base_time = datetime.now() - timedelta(days=records_per_user)
			for username, user_id in username_to_id.items():
				# Count existing
				cur.execute("SELECT COUNT(*) FROM analysis_results WHERE user_id=%s", (user_id,))
				count_existing = cur.fetchone()[0]
				to_insert = max(0, records_per_user - count_existing)
				if to_insert == 0:
					continue

				batch = []
				for i in range(to_insert):
					# Create random 48-length binary input_data similar to app_simple.py features
					input_data = [1 if random.random() < 0.25 else 0 for _ in range(48)]
					cluster_result = 0
					total = sum(input_data)
					if total == 0:
						cluster_result = 0
					elif total <= 2:
						cluster_result = 1
					elif total <= 4:
						cluster_result = 2
					elif total <= 6:
						cluster_result = 3
					else:
						cluster_result = -1

					analysis_date = base_time + timedelta(minutes=i * 10 + random.randint(0, 5))
					batch.append((user_id, str(input_data), cluster_result, analysis_date))

				cur.executemany(
					"""
					INSERT INTO analysis_results (user_id, input_data, cluster_result, analysis_date)
					VALUES (%s, %s, %s, %s)
					""",
					batch,
				)

		connection.commit()
	finally:
		connection.close()


if __name__ == "__main__":
	seed_history(100)
	print("Seed riwayat analisis selesai.")












