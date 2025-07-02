#!/usr/bin/env python3
import subprocess
import os
import signal
import sys

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
TOTP_SECRET = os.environ.get("TOTP_SECRET")
VPN_CONFIG = os.environ.get("CONFIG")
CREDENTIALS_FILE = os.environ.get("CREDFILE")

def cleanup():
    if os.path.exists(CREDENTIALS_FILE):
        os.remove(CREDENTIALS_FILE)
        print("Cleaned up credentials file.")

try:
    otp_process = subprocess.run(
        ["oathtool", "--totp", "-b", TOTP_SECRET],
        capture_output=True, text=True, check=True
    )
    otp_code = otp_process.stdout.strip()

    with open(CREDENTIALS_FILE, 'w') as f:
        f.write(f"{USERNAME}\n{PASSWORD}{otp_code}\n")

    openvpn_process = subprocess.Popen(
        ["/usr/sbin/openvpn", "--config", VPN_CONFIG, "--auth-user-pass", CREDENTIALS_FILE]
    )

    def signal_handler(sig, frame):
        print("Termination signal received, stopping OpenVPN.")
        openvpn_process.terminate()
        cleanup()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)


    openvpn_process.wait()

except subprocess.CalledProcessError as e:
    print(f"Failed to generate OTP: {e}")
    cleanup()
    sys.exit(1)

except Exception as e:
    print(f"Failed to start OpenVPN: {e}")
    cleanup()
    sys.exit(1)

finally:
    cleanup()
