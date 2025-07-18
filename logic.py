import sqlite3
from datetime import datetime
from config import DATABASE, TOKEN
import os


class DatabaseManager:
    def __init__(self, database):
        self.database = database

    def add_user(self, user_id, user_name):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('INSERT INTO users VALUES (?, ?)', (user_id, user_name))
            conn.commit()

    def add_prize(self, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany('''INSERT INTO prizes (image) VALUES (?)''', data)
            conn.commit()

    def add_winner(self, user_id, prize_id):
        win_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor() 
            cur.execute("SELECT * FROM winners WHERE user_id = ? AND prize_id = ?", (user_id, prize_id))
            if cur.fetchall():
                return 0
            else:
                conn.execute('''INSERT INTO winners (user_id, prize_id, win_time) VALUES (?, ?, ?)''', (user_id, prize_id, win_time))
                conn.commit()
                return 1

  
    def mark_prize_used(self, prize_id):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''UPDATE prizes SET used = 1 WHERE prize_id = ?''', (prize_id,))
            conn.commit()


    def get_users(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor() 
            cur.execute("SELECT * FROM users")
            return cur.fetchall()
        
    def get_good_games(self, Sales):
        #Mengambil data image dari tabel prize dimana prize_id = prize_id
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor() 
            cur.execute("SELECT Name, Sales FROM games WHERE Sales > '10'",(Sales))
            return cur.fetchall()

    def get_random_games(self):
        #Mendapatkan data image dari table prize dimana used = 0 dan diurutkan secara acak
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor() 
            cur.execute("SELECT Name FROM games ORDER BY RANDOM() LIMIT 3 ")
            return cur.fetchall()

    def get_winners_count(self, prize_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute('SELECT count(*) as total_winner FROM winners WHERE prize_id = ?', (prize_id, ))
            return cur.fetchall()
        
    def get_rating(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute('''
    SELECT users.user_name, COUNT(*) as total_wins
FROM users
INNER JOIN winners ON users.user_id = winners.user_id
GROUP BY users.user_id
ORDER BY total_wins DESC
LIMIT 10
    ''')
            return cur.fetchall()
        
    def get_winners_img(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(''' 
SELECT image FROM winners 
INNER JOIN prizes ON 
winners.prize_id = prizes.prize_id
WHERE user_id = ?''', (user_id, ))
        return cur.fetchall()


if __name__ == '__main__':
    manager = DatabaseManager(DATABASE)
    manager.create_tables()
    prizes_img = os.listdir('img')
    data = [(x,) for x in prizes_img]
    manager.add_prize(data)