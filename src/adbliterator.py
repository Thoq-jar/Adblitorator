"""
Adbliterator.py: The main entrypoint for Adbliterator.
@author: Thoq
@since: December 31st, 2024
"""

import argparse
import os
import subprocess
import threading
import time

from flask import Flask, render_template
from mitmproxy.tools.main import mitmdump

from lib import BANNER, default_config
from lib import debug

blocking = True
script_dir = os.path.dirname(os.path.abspath(__file__))
service_path = os.path.join(script_dir, "service.py")
template_dir = os.path.join(script_dir, "../.webui")

app = Flask(__name__, template_folder=template_dir)
STATE_FILE = os.path.join(script_dir, "../adbliterator/state_management.btr")


@app.route("/webui")
def hello_world():
    return render_template("index.html")


@app.route("/webui/v1/disable", methods=["POST"])
def disable():
    set_blocking_state(False)
    return f"<p>Blocking is disabled.</p>", 200


@app.route("/webui/v1/enable", methods=["POST"])
def enable():
    set_blocking_state(True)
    return f"<p>Blocking is enabled.</p>", 200


@app.route("/webui/v1/status", methods=["GET"])
def status():
    state = get_blocking_state()
    return f"<p>Blocking is {'enabled' if state else 'disabled'}.</p>", 200


def run_flask_app():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


def set_blocking_state(state: bool):
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'w') as f:
            f.write("enabled" if state else "disabled")
    else:
        with open(STATE_FILE, 'w') as f:
            f.write("enabled")


def get_blocking_state() -> bool:
    with open(STATE_FILE, 'r') as file:
        return file.read().strip() == "enabled"


def main():
    print(BANNER)
    print("Welcome to Adbliterator!")
    print("The proxy will start in ~1s...")
    if debug:
        print("Debug mode may reduce performance!")
    if default_config:
        print("To modify the default settings, edit adbliterator/config.yaml in the directory")
        print("To silence the message above, disable 'default' in adbliterator/config.yaml")
    time.sleep(0.5)
    if debug:
        print("Adbliterator booted up successfully!")
        time.sleep(0.5)
        mitmdump(["-s", service_path, "--set", "loglevel=info"])
    else:
        print("Adbliterator booted up successfully!\nRunning on :8080")
        subprocess.run(["mitmdump", "-s", service_path],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", help="increase output verbosity")
    args = parser.parse_args()
    if args.debug:
        debug = True

    print("Adbliterator booting up...")

    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    try:
        main()
    except KeyboardInterrupt:
        print("\nAdbliterator interrupted via ctrl+c, exiting...")
    except Exception as e:
        print(f"An exception occurred: {e}")
