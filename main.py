import requests
import random
import string
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque
import os
import sys

class Colors:
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    CLEAR = "\033[K"

class Config:
    WEBHOOK_URL = "https://discord.com/api/webhooks/1537992631043493918/KOFvRru8InAx6PoA79wxHDi4EUz3lw1zgmWaYqUKVmRpS33i-mXD0rbyT6QG6vsy4N98"
    SAVE_TO_FILE = False
    OUTPUT_FILE = "usernames.txt"
    THREADS = 5000
    BATCH_SIZE = 1000
    CHECK_TIMEOUT = 1
    SHOW_STATS = True
    WEBHOOK_BATCH_SIZE = 25
    WEBHOOK_FLUSH_INTERVAL = 3.0
    WEBHOOK_DELAY = 0.5

class UsernameGenerator:
    WORDLIST = [
        # Original short words
        "amb", "ark", "ash", "aur", "axe", "bad", "bag", "ban", "bar", "bat", "bay", "bed", "bee", "bet", "bid", "big",
        "bin", "bit", "blade", "blaze", "blox", "bolt", "bone", "boom", "boss", "box", "boy", "bud", "bug", "bun", "bus",
        "but", "buy", "cab", "cam", "cap", "car", "cat", "cel", "cha", "che", "chi", "cho", "chu", "civ", "clan", "claw",
        "clay", "cloud", "coast", "code", "cold", "cone", "core", "cove", "cow", "coy", "crab", "craw", "crew", "cris",
        "crow", "crux", "cub", "cup", "cur", "cut", "cyb", "dare", "dark", "dawn", "daze", "dead", "deep", "defy", "demo",
        "dev", "dex", "di", "dig", "dim", "dip", "do", "dog", "dom", "don", "doom", "dose", "dot", "dov", "down", "doz",
        "draf", "drag", "drake", "drea", "drew", "drip", "drop", "drow", "dru", "dry", "dub", "dud", "dun", "duo", "dye",

        # Gaming & Action words
        "apex", "blitz", "burst", "crush", "dash", "flash", "frost", "fury", "glow", "haze", "hype", "jinx", "jolt",
        "lurk", "maze", "neon", "nova", "omen", "prowl", "pulse", "quik", "rage", "raven", "reck", "rush", "shade",
        "slash", "smash", "spark", "storm", "surge", "swift", "thorn", "vibe", "vorn", "vortex", "wave", "zap", "zeph",

        # Tech & Modern
        "byte", "chip", "circ", "cyber", "data", "disk", "flux", "glitch", "grid", "icon", "link", "lynx", "mesh",
        "mode", "nex", "nexus", "node", "pixel", "port", "proxy", "sync", "tech", "wire", "xeno", "zone",

        # Cool-sounding / Edgy
        "drex", "dusk", "glyx", "krip", "kyro", "luxe", "myst", "nyx", "qyro", "rekt", "rune", "vekt", "vex", "vexo",
        "vyn", "wisp", "xray", "zynk", "zeal", "zest", "zint", "zolt",

        # Nature & Elemental
        "amber", "bloom", "breeze", "brook", "cedar", "coral", "creek", "ember", "fern", "flint",
        "flora", "gale", "glacier", "grove", "hail", "ivory", "jade", "lake", "leaf", "luna", "mira", "mist",
        "moon", "moss", "nara", "nyla", "onyx", "opal", "pearl", "rain", "reef", "ridge", "river", "sage", "sora",
        "star", "stone", "tide", "vale", "wind", "wren",

        # Mythic & Fantasy
        "aero", "arc", "aria", "astra", "aether", "celes", "chron", "crypt", "cyra", "drak", "echo", "elix", "elys",
        "fae", "fenix", "gaia", "glyph", "griff", "hades", "helix", "hydra", "iris", "kael", "karma", "kaze", "kryp",
        "ley", "lore", "lyra", "mage", "mana", "myth", "nix", "nymph", "odin", "oracle", "orb", "phoenix", "pyr",
        "quest", "relic", "saga", "seer", "seraph", "sigil", "siren", "soul", "spell", "sphinx", "titan",
        "valk", "veil", "venom", "void", "wraith", "wyrm", "yggd", "zeus", "zephyr",

        # Abstract & Compound-style
        "delve", "drift", "etern", "fable", "forge", "gleam", "gloom", "haven", "idle", "kin",
        "knack", "linx", "lucid", "mirth", "muse", "nip", "nock", "pact", "peak", "prism", "quirk", "reign", "rift",
        "ruse", "shine", "shroud", "sly", "snap", "soar", "spire", "sworn", "syn", "tac", "trance", "trek", "trick",
        "trine", "tryst", "vast", "verge", "vigor", "vow", "whim", "wry", "yield",

        # Additional short punchy words
        "ace", "art", "aura", "cog", "disc", "edge", "epic", "fade", "fate",
        "flick", "gear", "grip", "gust", "hero", "hop", "hub", "hue", "imp", "jab", "jag", "ken", "kite", "lash",
        "loft", "lude", "lure", "meld", "mind", "miss", "mote", "narc", "nave", "pace",
        "pane", "pike", "pip", "ploy", "pod", "quo", "raft", "ray", "seek", "silo",
        "sip", "skid", "skye", "sole", "spur", "stem", "stir", "suede", "sway", "tale", "tick",
        "tile", "tint", "tome", "trace", "trope", "vane", "view", "vise", "volt", "wade", "warp", "weave",
        "wick", "wield", "yon", "zen"
    ]

    @staticmethod
    def generate():
        word = random.choice(UsernameGenerator.WORDLIST)
        base = word[:4] if len(word) > 4 else word
        if len(base) < 4:
            base += ''.join(random.choices(string.ascii_lowercase, k=4 - len(base)))
        digit = random.choice(string.digits)

        patterns = [
            base[:3] + digit + base[3:4],
            base[:2] + digit + base[2:4],
            base[:1] + digit + base[1:4],
            base[:4] + digit,
            digit + base[:4]
        ]

        username = random.choice(patterns)
        if len(username) > 5:
            username = username[:5]
        elif len(username) < 5:
            username += random.choice(string.digits)
        return username

class WebhookBatcher:
    def __init__(self, url, batch_size=25, flush_interval=3.0, delay=0.5):
        self.url = url
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.delay = delay
        self.buffer = []
        self.lock = threading.Lock()
        self.running = True
        self.last_flush = time.time()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def send(self, username):
        if not self.url:
            return
        with self.lock:
            self.buffer.append(username)

    def _flush(self, force=False):
        with self.lock:
            if not self.buffer:
                return
            if not force and len(self.buffer) < self.batch_size and (time.time() - self.last_flush) < self.flush_interval:
                return
            batch = self.buffer[:]
            self.buffer.clear()
            self.last_flush = time.time()

        self._post_batch(batch)

    def _post_batch(self, usernames):
        if not usernames:
            return

        lines = "\n".join(f"`{u}`" for u in usernames)

        embed = {
            "title": f"Available Usernames ({len(usernames)})",
            "description": lines,
            "color": 65280
        }

        try:
            requests.post(
                self.url,
                json={"embeds": [embed]},
                timeout=5
            )
        except:
            pass

    def _run(self):
        while self.running:
            self._flush()
            time.sleep(0.5)
        self._flush(force=True)

    def stop(self):
        self.running = False
        self.thread.join(timeout=5)

class RobloxChecker:
    def __init__(self):
        self.session_pool = deque(maxlen=Config.THREADS)
        self.found_usernames = []
        self.checked_count = 0
        self.lock = threading.Lock()
        self.stop_flag = False
        self.start_time = time.time()
        self.webhook = WebhookBatcher(
            Config.WEBHOOK_URL,
            batch_size=Config.WEBHOOK_BATCH_SIZE,
            flush_interval=Config.WEBHOOK_FLUSH_INTERVAL,
            delay=Config.WEBHOOK_DELAY
        )
        self._init_session_pool()

    def _init_session_pool(self):
        for _ in range(min(Config.THREADS, 100)):
            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive"
            })
            self.session_pool.append(session)

    def _get_session(self):
        with self.lock:
            if self.session_pool:
                return self.session_pool.popleft()
        return requests.Session()

    def _return_session(self, session):
        with self.lock:
            self.session_pool.append(session)

    def _check_username(self, session, username):
        url = f"https://auth.roblox.com/v2/usernames/validate?request.username={username}&request.birthday=2003-11-07"
        try:
            response = session.get(url, timeout=Config.CHECK_TIMEOUT)
            if response.status_code == 200:
                return response.json().get("code") == 0
            return False
        except:
            return False

    def _save_username(self, username):
        if Config.SAVE_TO_FILE:
            try:
                with open(Config.OUTPUT_FILE, 'a') as f:
                    f.write(f"{username}\n")
            except:
                pass

    def _worker(self, username):
        if self.stop_flag:
            return None

        session = self._get_session()
        try:
            available = self._check_username(session, username)
        finally:
            self._return_session(session)

        with self.lock:
            self.checked_count += 1
            current = self.checked_count

        if available:
            with self.lock:
                self.found_usernames.append(username)
            print(f"{Colors.CLEAR}{Colors.GREEN}[+] {username}{Colors.RESET}")
            self.webhook.send(username)
            self._save_username(username)
            return username

        if Config.SHOW_STATS and current % 500 == 0:
            elapsed = time.time() - self.start_time
            speed = current / elapsed if elapsed > 0 else 0
            print(f"{Colors.CLEAR}{Colors.CYAN}Checked: {current:,} | Found: {len(self.found_usernames)} | {speed:.0f}/s{Colors.RESET}", end="\r", flush=True)

        return None

    def process_batch(self, batch_usernames):
        if self.stop_flag:
            return []

        results = []
        with ThreadPoolExecutor(max_workers=Config.THREADS) as executor:
            futures = {executor.submit(self._worker, username): username for username in batch_usernames}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                if self.stop_flag:
                    break
        return results

    def run(self, target=None):
        print(f"{Colors.CYAN}Starting scan with {Config.THREADS} threads...{Colors.RESET}")
        self.start_time = time.time()
        found = 0

        try:
            while True:
                if target is not None and found >= target:
                    break

                batch = [UsernameGenerator.generate() for _ in range(Config.BATCH_SIZE)]
                batch_results = self.process_batch(batch)
                found += len(batch_results)

                if target is not None and found >= target:
                    break

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Interrupted by user{Colors.RESET}")
            self.stop_flag = True

        print(f"\n{Colors.CYAN}Flushing final webhook batch...{Colors.RESET}")
        self.webhook.stop()

        elapsed = time.time() - self.start_time
        speed = self.checked_count / elapsed if elapsed > 0 else 0

        print(f"\n{Colors.CLEAR}{Colors.CYAN}Completed:{Colors.RESET}")
        print(f"  {Colors.GREEN}Found: {len(self.found_usernames)}{Colors.RESET}")
        print(f"  {Colors.CYAN}Checked: {self.checked_count:,}{Colors.RESET}")
        print(f"  {Colors.CYAN}Speed: {speed:.0f}/s{Colors.RESET}")

        if self.found_usernames and Config.SAVE_TO_FILE:
            print(f"  {Colors.GREEN}Saved to: {Config.OUTPUT_FILE}{Colors.RESET}")

        return self.found_usernames

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--config":
        print(f"\n{Colors.CYAN}Current Configuration:{Colors.RESET}")
        print(f"  Webhook: {'Enabled' if Config.WEBHOOK_URL else 'Disabled'}")
        print(f"  Save to file: {Config.SAVE_TO_FILE}")
        print(f"  Output file: {Config.OUTPUT_FILE}")
        print(f"  Threads: {Config.THREADS}")
        print(f"  Batch size: {Config.BATCH_SIZE}")
        print(f"  Webhook batch size: {Config.WEBHOOK_BATCH_SIZE}")
        return

    checker = RobloxChecker()

    target = None
    while True:
        try:
            user_input = input(f"{Colors.CYAN}Target count (Enter for unlimited, 'q' to quit): {Colors.RESET}")
            if user_input.lower() == 'q':
                return
            if user_input.strip() == "":
                break
            target = int(user_input)
            break
        except ValueError:
            print(f"{Colors.RED}Invalid input{Colors.RESET}")

    checker.run(target)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")