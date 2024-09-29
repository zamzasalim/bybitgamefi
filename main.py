import sys as system
import time as t
import json as js
import os as operating_system
import requests as req
import re as regex
import hmac as h
import hashlib as sha
import random as rnd
import pytz as timezone
import math as mth
from datetime import datetime as dtm
import urllib.parse as urlparse

def compute_score(x, y, z, p, q, r):
    intermediate = (10 * x + max(0, 1200 - 10 * y) + 2000) * (1 + q / z) / 10
    return mth.floor(intermediate) + calculate_value(r)

def generate_hmac_hash(secret_key, msg):
    try:
        hash_obj = h.new(secret_key.encode(), msg.encode(), sha.sha256)
        return hash_obj.hexdigest()
    except Exception as ex:
        print(f"Error generating HMAC: {str(ex)}")
        return None

def decode_url(encoded_str):
    return urlparse.unquote(encoded_str)

def calculate_value(text):
    return sum(ord(character) for character in text) / 1e5

def display_banner():
    art = [
        '   █████████   █████ ███████████   ██████████   ███████████      ███████    ███████████       █████████    █████████    █████████',
        '  ███░░░░░███ ░░███ ░░███░░░░░███ ░░███░░░░███ ░░███░░░░░███   ███░░░░░███ ░░███░░░░░███     ███░░░░░███  ███░░░░░███  ███░░░░░███',
        ' ░███    ░███  ░███  ░███    ░███  ░███   ░░███ ░███    ░███  ███     ░░███ ░███    ░███    ░███    ░███ ░███    ░░░  ███     ░░░',
        ' ░███████████  ░███  ░██████████   ░███    ░███ ░██████████  ░███      ░███ ░██████████     ░███████████ ░░█████████ ░███         ',
        ' ░███░░░░░███  ░███  ░███░░░░░███  ░███    ░███ ░███░░░░░███ ░███      ░███ ░███░░░░░░      ░███░░░░░███  ░░░░░░░░███░███         ',
        ' ░███    ░███  ░███  ░███    ░███  ░███    ███  ░███    ░███ ░░███     ███  ░███            ░███    ░███  ███    ░███░░███     ███',
        ' █████   █████ █████ █████   █████ ██████████   █████   █████ ░░░███████░   █████           █████   █████░░█████████  ░░█████████',
        ' ░░░░░   ░░░░░ ░░░░░ ░░░░░   ░░░░░ ░░░░░░░░░░   ░░░░░   ░░░░░    ░░░░░░░    ░░░░░           ░░░░░   ░░░░░  ░░░░░░░░░    ░░░░░░░░░  ',
        '==============================================',
        'Telegram Channel : @airdropasc               ',
        'Telegram Group   : @autosultan_group         ',
        '==============================================' 
    ]
    for line in art:
        print(line)

class ByBitClient:
    def __init__(self):
        self.connection = req.session()
        self.connection.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,vi-VN;q=0.6,vi;q=0.5",
            "Content-Type": "application/json",
            "Origin": "https://bybitcoinsweeper.com",
            "Referer": "https://bybitcoinsweeper.com/",
            "tl-init-data": None,
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.146 Mobile Safari/537.36"
        }
        self.user_info = {"score": 0}

    def log_event(self, desc, detail, lvl=""):
        print(f"{lvl}: {desc} - {detail}")

    def pause(self, sec):
        lvl = ""
        desc = "Waiting Start"
        prefix = f"{lvl}: {desc} - {sec} Sec"
        
        system.stdout.write(prefix)
        system.stdout.flush()
        
        for remaining in range(sec, 0, -1):
            t.sleep(1)
            system.stdout.write('\r' + f"{lvl}: {desc} - {remaining} Sec")
            system.stdout.flush()
        
        print()

    def authenticate(self, init_data):
        try:
            self.connection.headers["tl-init-data"] = init_data
            response = self.connection.post(
                "https://api.bybitcoinsweeper.com/api/auth/login",
                json={"initData": init_data},
                headers=self.connection.headers
            )
            if response.status_code == 201:
                data = response.json()
                self.connection.headers['Authorization'] = f"Bearer {data['accessToken']}"
                return {
                    "success": True,
                    "accessToken": data['accessToken'],
                    "refreshToken": data['refreshToken'],
                    "userId": data['id']
                }
            else:
                err_msg = response.json().get('message', 'Unexpected error')
                self.log_event("Login Failed", err_msg, "ERROR")
                return {"success": False, "error": err_msg}
        except req.RequestException as err:
            self.log_event("Request Error During Login", str(err), "ERROR")
            return {"success": False, "error": str(err)}

    def get_user_info(self):
        try:
            user_data = self.connection.get("https://api.bybitcoinsweeper.com/api/users/me", headers=self.connection.headers).json()
            return user_data
        except req.RequestException as err:
            self.log_event("Request Error During Fetching User Info", str(err), "ERROR")
            return {"success": False, "error": str(err)}

    def handle_win_score(self):
        try:
            min_time = 60
            max_time = 110
            game_duration = rnd.randint(min_time, max_time)
            game_start = self.connection.post("https://api.bybitcoinsweeper.com/api/games/start", json={}, headers=self.connection.headers).json()
            
            if "message" in game_start and "expired" in game_start["message"]:
                self.log_event("Query Expired Sir", "Terminating script.", "ERROR")
                system.exit(0)
            
            game_id = game_start["id"]
            rewards = game_start["rewards"]
            start_time_str = game_start["createdAt"]
            user_data = self.get_user_info()
            total_score = user_data.get('score', 0) + user_data.get('scoreFromReferrals', 0)
            self.log_event("Balance", str(total_score), "")
            
            start_time = dtm.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.UTC)
            start_timestamp = int(start_time.timestamp() * 1000)
            
            self.log_event("Start Game", "Success!!", "")
            self.pause(game_duration)
            
            identifier = f"{user_data['id']}v$2f1"
            first_part = f"{identifier}-{game_id}-{start_timestamp}"
            last_part = f"{game_duration}-{game_id}"
            score = compute_score(45, game_duration, 54, 9, True, game_id)
            
            game_payload = {
                "bagCoins": rewards["bagCoins"],
                "bits": rewards["bits"],
                "gifts": rewards["gifts"],
                "gameId": game_id,
                'gameTime': game_duration,
                "h": generate_hmac_hash(first_part, last_part),
                'score': float(score)
            }
            
            result = self.connection.post('https://api.bybitcoinsweeper.com/api/games/win', json=game_payload, headers=self.connection.headers)
            if result.status_code == 201:
                self.user_info["score"] += score
                self.log_event("Game Status", "YOU WIN", "SUCCESS")
            elif result.status_code == 401:
                self.log_event("Token Expired", "Need to log in again.", "ERROR")
                return False
            else:
                self.log_event("Error Occurred", f"Code {result.status_code}", "ERROR")
            
            self.pause(5)
        except req.RequestException:
            self.log_event("Too Many Requests", "Waiting.", "WARNING")
            self.pause(60)

    def handle_lose_score(self):
        try:
            min_time = 70
            max_time = 120
            game_duration = rnd.randint(min_time, max_time)
            game_start = self.connection.post("https://api.bybitcoinsweeper.com/api/games/start", json={}, headers=self.connection.headers).json()
            
            if "message" in game_start and "expired" in game_start["message"]:
                self.log_event("Query Expired Sir", "Terminating script.", "ERROR")
                system.exit(0)
            
            game_id = game_start["id"]
            rewards = game_start["rewards"]
            start_time_str = game_start["createdAt"]
            user_data = self.get_user_info()
            total_score = user_data.get('score', 0) + user_data.get('scoreFromReferrals', 0)
            self.log_event("Balance", str(balance), "")
            
            start_time = dtm.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.UTC)
            
            self.log_event("Starting Game", "Success!!", "")
            self.log_event("Play Time Game", f"{game_duration} Sec", "")
            self.pause(game_duration)
            
            game_payload = {
                "bagCoins": rewards["bagCoins"],
                "bits": rewards["bits"],
                "gifts": rewards["gifts"],
                "gameId": game_id
            }
            
            result = self.connection.post('https://api.bybitcoinsweeper.com/api/games/lose', json=game_payload, headers=self.connection.headers)
            if result.status_code == 201:
                self.log_event("Game Status", "YOU LOSE", "ERROR")
            elif result.status_code == 401:
                self.log_event("Token Expired", "Need to log in again.", "ERROR")
                return False
            else:
                self.log_event("Error Occurred", f"Code {result.status_code}", "ERROR")
            
            self.pause(5)
        except req.RequestException:
            self.log_event("Too Many Requests", "Please wait.", "WARNING")
            self.pause(60)

    def process_scores(self):
        for attempt in range(3):
            try:
                if rnd.random() < 0.8:
                    self.handle_win_score()
                else:
                    self.handle_lose_score()
            except Exception as ex:
                self.log_event("Exception Occurred", str(ex), "ERROR")
        return True

    def execute(self):
        operating_system.system('cls' if system.platform.startswith('win') else 'clear')
        display_banner()
        data_path = operating_system.path.join(operating_system.path.dirname(__file__), 'data.txt')
        
        try:
            with open(data_path, 'r', encoding='utf8') as file:
                init_data_list = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            self.log_event("Data File Error", f"'{data_path}' not found.", "ERROR")
            system.exit(1)
        except Exception as ex:
            self.log_event("Data File Error", str(ex), "ERROR")
            system.exit(1)
        
        while True:
            try:
                proxy_file_path = 'proxy.txt'
                if operating_system.path.exists(proxy_file_path):
                    with open(proxy_file_path, 'r') as proxy_file:
                        proxies_list = [line.strip() for line in proxy_file if line.strip()]
                else:
                    proxies_list = []
            except Exception as ex:
                self.log_event("Proxy File Error", str(ex), "ERROR")
                proxies_list = []
            
            for idx, init_data in enumerate(init_data_list):
                proxy = proxies_list[(idx - 1) % len(proxies_list)] if proxies_list else None
                if proxy:
                    self.connection.proxies.update({'http': proxy, 'https': proxy})
                
                decoded_once = decode_url(init_data)
                fully_decoded = decode_url(decoded_once)
                
                try:
                    user_str = fully_decoded.split('user=')[1].split('&')[0]
                    user_details = js.loads(user_str)
                except (IndexError, js.JSONDecodeError) as parse_err:
                    self.log_event("Data Parsing Error", str(parse_err), "ERROR")
                    continue
                
                self.log_event("Account", user_details.get('first_name', 'Unknown'), "")
                
                auth_result = self.authenticate(init_data)
                if auth_result.get("success"):
                    self.log_event("Login", "Success!!", "")
                    game_result = self.process_scores()
                    if not game_result:
                        self.log_event("Login Reattempt", "Need to log in again, moving to the next account", "WARNING")
                else:
                    self.log_event("Login Failed", auth_result.get('error', 'Unknown Error'), "ERROR")
                
                if idx < len(init_data_list) - 1:
                    self.pause(3)
            
            self.pause(3)

if __name__ == '__main__':
    client_instance = ByBitClient()
    try:
        client_instance.execute()
    except Exception as unexpected_error:
        client_instance.log_event("Unhandled Exception", str(unexpected_error), "ERROR")
        system.exit(1)
        
