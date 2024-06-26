
import sqlite3
from sqlite3 import DataError

class Leaderboard:
    def __init__(self, db):
        if not db:
            raise ValueError("Database cannot be None or empty.")
        
        self.db = db
        
    def connection(self):
    
        conn = sqlite3.connect(self.db)
        return conn
        
            
    def insert_score(self, player_name, score):
        conn = self.connection()
        sql = '''INSERT INTO scores (player_name, score) VALUES (?, ?)'''
        cur = conn.cursor()
        cur.execute(sql, (player_name, score))
        conn.commit()
        conn.close()
         
    def generate_leaderboard(self, current_player=None):
        conn = self.connection()
        sql_top_10 = '''
            SELECT player_name, SUM(score) AS total_score
            FROM scores
            GROUP BY player_name
            ORDER BY total_score DESC
            LIMIT 10
        '''
        sql_player_rank = '''
            SELECT player_name, SUM(score), RANK () OVER (ORDER BY SUM(score) DESC)
            FROM scores
            GROUP BY player_name
        '''
        
        cur = conn.cursor()
        cur.execute(sql_top_10)
        top_players = cur.fetchall()
    
        print("Top 10 Leaderboard\n------------------")
        print(f"{'Rank':<5}{'Player':<10}{'Score':>6}")
        for index, (player, score) in enumerate(top_players, start=1):
            print(f"{index:<5}{player:<10}{score:>6}")
        
        if current_player:
            cur.execute(sql_player_rank)
            all_players = cur.fetchall()
            
            player_rank = next((i for i in all_players if i[0] == current_player), None)

            if player_rank:
                rank = int(player_rank[2]) 
                if rank >= 10:
                    print(f".........")
                    print(f".........")
                    print(f"{player_rank[2]:<5}{player_rank[0]:<10}{player_rank[1]:>6}")
    
        conn.close()