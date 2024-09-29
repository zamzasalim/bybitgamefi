import os
import json
import time
import requests
import crayons
import sys
import re
import hmac
import hashlib
import random
import pytz
import math
from datetime import datetime
import urllib.parse


def calc(i, s, a, o, d, g):
    st = (10 * i + max(0, 1200 - 10 * s) + 2000) * (1 + o / a) / 10
    return math.floor(st) + value(g)


def generate_hash(key, message):
    try:
        hmac_obj = hmac.new(key.encode(), message.encode(), hashlib.sha256)
        return hmac_obj.hexdigest()
    except Exception as e:
        print(f"Hash generation error: {str(e)}")
        return None


def url_decode(encoded_url):
    return urllib.parse.unquote(encoded_url)


def value(input_str):
    return sum(ord(char) for char in input_str) / 1e5


def print_banner():
    banner = [
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
    for line in banner:
        print(crayons.blue(line))


class ByBit:
    def __init__(self):
        self.session = requests.session()
        self.headers = {
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
        self.info = {"score": 0}

    def log(self, description, details, level="INFO"):
        levels = {
            "INFO": crayons.cyan,
            "ERROR": crayons.red,
            "SUCCESS": crayons.cyan,
            "WARNING": crayons.yellow,
            "YOU WIN": crayons.cyan,
            "YOU LOSE": crayons.red
        }
        level_color = levels.get(level, crayons.cyan)(level)
        
        if level in ["YOU WIN", "YOU LOSE"]:
            details_colored = levels[level](details)
        else:
            details_colored = levels.get(level, crayons.cyan)(details)
        
        print(f"| {level_color} | {description} | {details_colored}")

    def wait(self, seconds):
        level = "INFO"
        description = "Waiting Play"

        levels = {
            "INFO": crayons.cyan,
            "ERROR": crayons.red,
            "SUCCESS": crayons.cyan,
            "WARNING": crayons.yellow
        }
        level_color = levels.get(level, crayons.cyan)(level)

        message_prefix = f"| {level_color} | {description} | "

        sys.stdout.write(message_prefix + f"{seconds} Seconds")
        sys.stdout.flush()

        for i in range(seconds, 0, -1):
            time.sleep(1)
            sys.stdout.write('\r' + message_prefix + f"{i} Seconds")
            sys.stdout.flush()

        print()

    def login(self, init_data):
        try:
            self.headers["tl-init-data"] = init_data
            response = self.session.post("https://api.bybitcoinsweeper.com/api/auth/login", json={"initData": init_data}, headers=self.headers)
            if response.status_code == 201:
                data = response.json()
                self.headers['Authorization'] = f"Bearer {data['accessToken']}"
                return {
                    "success": True,
                    "accessToken": data['accessToken'],
                    "refreshToken": data['refreshToken'],
                    "userId": data['id']
                }
            else:
                error_message = response.json().get('message', 'Unexpected error')
                self.log("Login Failed", error_message, "ERROR")
                return {"success": False, "error": error_message}
        except requests.RequestException as error:
            self.log("Request Error During Login", str(error), "ERROR")
            return {"success": False, "error": str(error)}

    def userinfo(self):
        try:
            user = self.session.get("https://api.bybitcoinsweeper.com/api/users/me", headers=self.headers).json()
            return user
        except requests.RequestException as error:
            self.log("Request Error During Fetching User Info", str(error), "ERROR")
            return {"success": False, "error": str(error)}

    def score_win(self):
        try:
            min_game_time = 60
            max_game_time = 110
            game_time = random.randint(min_game_time, max_game_time)
            playgame = self.session.post("https://api.bybitcoinsweeper.com/api/games/start", json={}, headers=self.headers).json()
            if "message" in playgame:
                if "expired" in playgame["message"]:
                    self.log("Query Expired Sir", "Terminating script.", "ERROR")
                    sys.exit(0)
            gameid = playgame["id"]
            rewarddata = playgame["rewards"]
            started_at = playgame["createdAt"]
            userdata = self.userinfo()
            total_score = userdata.get('score', 0) + userdata.get('scoreFromReferrals', 0)
            self.log("Total Score", str(total_score), "INFO")
            unix_time_started = datetime.strptime(started_at, '%Y-%m-%dT%H:%M:%S.%fZ')
            unix_time_started = unix_time_started.replace(tzinfo=pytz.UTC)
            starttime = int(unix_time_started.timestamp() * 1000)
            self.log("Starting Game", "Success!!", "INFO")
            self.log("Play Time Game", f"{game_time} Seconds", "INFO")
            self.wait(game_time)
            i = f"{userdata['id']}v$2f1"
            first = f"{i}-{gameid}-{starttime}"
            last = f"{game_time}-{gameid}"
            score = calc(45, game_time, 54, 9, True, gameid)
            game_data = {
                "bagCoins": rewarddata["bagCoins"],
                "bits": rewarddata["bits"],
                "gifts": rewarddata["gifts"],
                "gameId": gameid,
                'gameTime': game_time,
                "h": generate_hash(first, last),
                'score': float(score)
            }
            res = self.session.post('https://api.bybitcoinsweeper.com/api/games/win', json=game_data, headers=self.headers)
            if res.status_code == 201:
                self.info["score"] += score
                self.log("Game Status", "YOU WIN", "INFO")
            elif res.status_code == 401:
                self.log("Token Expired", "Need to log in again.", "ERROR")
                return False
            else:
                self.log("Error Occurred", f"Code {res.status_code}", "ERROR")
            self.wait(5)
        except requests.RequestException:
            self.log("Too Many Requests", "Waiting.", "WARNING")
            self.wait(60)

    def score_lose(self):
        try:
            min_game_time = 70
            max_game_time = 120
            game_time = random.randint(min_game_time, max_game_time)
            playgame = self.session.post("https://api.bybitcoinsweeper.com/api/games/start", json={}, headers=self.headers).json()
            if "message" in playgame:
                if "expired" in playgame["message"]:
                    self.log("Query Expired Sir", "Terminating script.", "ERROR")
                    sys.exit(0)
            gameid = playgame["id"]
            rewarddata = playgame["rewards"]
            started_at = playgame["createdAt"]
            userdata = self.userinfo()
            total_score = userdata.get('score', 0) + userdata.get('scoreFromReferrals', 0)
            self.log("Total Score", str(total_score), "INFO")
            unix_time_started = datetime.strptime(started_at, '%Y-%m-%dT%H:%M:%S.%fZ')
            unix_time_started = unix_time_started.replace(tzinfo=pytz.UTC)
            self.log("Starting Game", "Success!!", "INFO")
            self.log("Play Time Game", f"{game_time} Seconds", "INFO")
            self.wait(game_time)
            game_data = {
                "bagCoins": rewarddata["bagCoins"],
                "bits": rewarddata["bits"],
                "gifts": rewarddata["gifts"],
                "gameId": gameid
            }
            res = self.session.post('https://api.bybitcoinsweeper.com/api/games/lose', json=game_data, headers=self.headers)
            if res.status_code == 201:
                self.log("Game Status", "YOU LOSE", "ERROR")
            elif res.status_code == 401:
                self.log("Token Expired", "Need to log in again.", "ERROR")
                return False
            else:
                self.log("Error Occurred", f"Code {res.status_code}", "ERROR")
            self.wait(5)
        except requests.RequestException:
            self.log("Too Many Requests", "Please wait.", "WARNING")
            self.wait(60)

    def score(self):
        for i in range(3):
            try:
                is_win = random.random() < float(0.8)
                if is_win:
                    self.score_win()
                else:
                    self.score_lose()
            except Exception as e:
                self.log("Exception Occurred", str(e), "ERROR")
        return True

    def main(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        data_file = os.path.join(os.path.dirname(__file__), 'data.txt')
        try:
            with open(data_file, 'r', encoding='utf8') as f:
                data = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.log("Data File Error", f"'{data_file}' not found.", "ERROR")
            sys.exit(1)
        except Exception as e:
            self.log("Data File Error", str(e), "ERROR")
            sys.exit(1)

        while True:
            try:
                proxy_file = 'proxy.txt'
                if os.path.exists(proxy_file):
                    with open(proxy_file, 'r') as pf:
                        proxies = [line.strip() for line in pf if line.strip()]
                else:
                    proxies = []
            except Exception as e:
                self.log("Proxy File Error", str(e), "ERROR")
                proxies = []

            for i, init_data in enumerate(data):
                proxy = proxies[(i - 1) % len(proxies)] if proxies else None
                if proxy:
                    self.session.proxies.update({'http': proxy, 'https': proxy})
                decoded = url_decode(init_data)
                finaldat = url_decode(decoded)
                try:
                    user_data_str = finaldat.split('user=')[1].split('&')[0]
                    user_data = json.loads(user_data_str)
                except (IndexError, json.JSONDecodeError) as e:
                    self.log("Data Parsing Error", str(e), "ERROR")
                    continue
                self.log("Account", user_data.get('first_name', 'Unknown'), "INFO")
                self.log("Logging into Account", str(user_data.get('id', 'Unknown')), "INFO")
                login_result = self.login(init_data)
                if login_result["success"]:
                    self.log("Login", "Success!!", "INFO")
                    game_result = self.score()
                    if not game_result:
                        self.log("Login Reattempt", "Need to log in again, moving to the next account", "WARNING")
                else:
                    self.log("Login Failed", login_result.get('error', 'Unknown Error'), "ERROR")

                if i < len(data) - 1:
                    self.wait(3)

            self.wait(3)


if __name__ == '__main__':
    client = ByBit()
    try:
        client.main()
    except Exception as err:
        client.log("Unhandled Exception", str(err), "ERROR")
        sys.exit(1)
