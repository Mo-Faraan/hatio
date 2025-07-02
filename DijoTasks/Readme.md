## Project Structure

- [`OpenVpnMfa.py`](OpenVpnMfa.py): Main Python script that handles MFA and OpenVPN process management.
- [`openvpnmfa@.service`](openvpnmfa@.service): systemd unit template for running the script as a service.

## Prerequisites

- Python 3
- `oathtool` (for TOTP generation)
- OpenVPN 
- Systemd 

## Setup

- Copy `OpenVpnMfa.py` to `/usr/local/bin/OpenVpnMfa.py` 
  [can edit the path in the system unit file]

- Copy `openvpnmfa@.service` to `/etc/systemd/system/openvpnmfa@.service`
  

## Configuration
- Create a new folder mfa in `/etc/openvpn/` 
- Create `/etc/openvpn/mfa/client` for placing vpn config files, `/etc/openvpn/mfa/envs` for placing env files and `/etc/openvpn/mfa/credentials` for placing the dynamic credential txt files

- For each VPN instance there should be 2 files : 1 env file with username, password, totp key and a corresponding config file with same name.
- eg : `sudo systemctl openvpnmfa@<instance-name>`
  - Create `/etc/openvpn/mfa/envs/<instance-name>.env` with:
    ```
    USERNAME=your_vpn_username
    PASSWORD=your_vpn_password
    TOTP_SECRET=your_totp_secret_key
    ```
  - Place corresponding OpenVPN config file at `/etc/openvpn/mfa/client/<instance-name>.conf`

## For Starting the Service

- `sudo systemctl start/stop/status openvpnmfa@<instance-name>`



