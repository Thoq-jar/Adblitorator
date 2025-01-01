"""
Adbliterator.py: The main entrypoint for Adbliterator.
@author: Thoq
@since: December 31st, 2024
"""

import time
from mitmproxy.tools.main import mitmdump
import os
import subprocess

from service import debug
from lib import BANNER, default_config

script_dir = os.path.dirname(os.path.abspath(__file__))
service_path = os.path.join(script_dir, "service.py")


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
    print("Adbliterator booting up...")
    try:
        main()
    except KeyboardInterrupt:
        print("\nAdbliterator interrupted via ctrl+c, exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
