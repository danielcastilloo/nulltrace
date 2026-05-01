BANNER = """
██████╗ ██████╗ ██╗██╗   ██╗ █████╗  ██████╗██╗   ██╗
██╔══██╗██╔══██╗██║██║   ██║██╔══██╗██╔════╝╚██╗ ██╔╝
██████╔╝██████╔╝██║██║   ██║███████║██║      ╚████╔╝ 
██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝██╔══██║██║       ╚██╔╝  
██║     ██║  ██║██║ ╚████╔╝ ██║  ██║╚██████╗   ██║   
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝  ╚═╝ ╚═════╝   ╚═╝   
███████╗██╗  ██╗██╗███████╗██╗     ██████╗ 
██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗
███████╗███████║██║█████╗  ██║     ██║  ██║
╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║
███████║██║  ██║██║███████╗███████╗██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝ 
        [ MAC + IP + VPN — by The world is your ]

BANNER = """


BANNER = """

	 0000             0000        7777777777777777/========___________
   00000000         00000000      7777^^^^^^^7777/ || ||   ___________
  000    000       000    000     777       7777/=========//
 000      000     000      000             7777// ((     //
0000      0000   0000      0000           7777//   \\   //
0000      0000   0000      0000          7777//========//
0000      0000   0000      0000         7777
0000      0000   0000      0000        7777
 000      000     000      000        7777
  000    000       000    000       77777
   00000000         00000000       7777777
     0000             0000        777777777

BANNER = """


#!/usr/bin/env python3
# privacy_shield.py — MAC + IP + ProtonVPN en un solo comando
# Uso: sudo python3 privacy_shield.py

import subprocess
import random
import sys
import re
import os
import time
import getpass

# ─── Utilidades ───────────────────────────────────────────

def check_root():
    if os.geteuid() != 0:
        print("[!] Este script necesita permisos de root.")
        print("    Ejecuta: sudo python3 privacy_shield.py")
        sys.exit(1)

def get_real_user():
    """Obtiene el usuario real aunque se ejecute con sudo."""
    return os.environ.get("SUDO_USER") or getpass.getuser()

def get_interfaces():
    result = subprocess.run(["ip", "link", "show"], capture_output=True, text=True)
    interfaces = re.findall(r'\d+: (\w+):', result.stdout)
    return [i for i in interfaces if i != "lo"]

def get_current_mac(iface):
    result = subprocess.run(["ip", "link", "show", iface], capture_output=True, text=True)
    match = re.search(r'link/ether ([\da-f:]+)', result.stdout)
    return match.group(1) if match else None

def get_current_ip(iface):
    result = subprocess.run(["ip", "addr", "show", iface], capture_output=True, text=True)
    match = re.search(r'inet (\S+)', result.stdout)
    return match.group(1) if match else None

def generate_random_mac():
    mac = [random.randint(0x00, 0xFF) for _ in range(6)]
    mac[0] = (mac[0] & 0xFE) | 0x02
    return ':'.join(f'{b:02x}' for b in mac)

# ─── Capa 1: MAC ──────────────────────────────────────────

def change_mac(iface, new_mac):
    try:
        subprocess.run(["ip", "link", "set", iface, "down"], check=True)
        subprocess.run(["ip", "link", "set", iface, "address", new_mac], check=True)
        subprocess.run(["ip", "link", "set", iface, "up"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Error al cambiar MAC: {e}")
        return False

# ─── Capa 2: IP ───────────────────────────────────────────

def change_ip_dhcp(iface, real_user):
    try:
        subprocess.run(["nmcli", "device", "disconnect", iface], check=True)
        time.sleep(1)
        subprocess.run(["nmcli", "device", "connect", iface], check=True)
        time.sleep(2)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Error al renovar IP: {e}")
        return False

def change_ip_static(iface, new_ip, prefix="24"):
    try:
        subprocess.run(["ip", "addr", "flush", "dev", iface], check=True)
        subprocess.run(["ip", "addr", "add", f"{new_ip}/{prefix}", "dev", iface], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Error al asignar IP: {e}")
        return False

# ─── Capa 3: ProtonVPN ────────────────────────────────────

COUNTRIES = {
    "1": ("Netherlands", "NL"),
    "2": ("United States", "US"),
    "3": ("Germany", "DE"),
    "4": ("Japan", "JP"),
    "5": ("Switzerland", "CH"),
    "6": ("France", "FR"),
    "7": ("Canada", "CA"),
    "8": ("United Kingdom", "UK"),
}

def select_country():
    print("\nPaíses disponibles (plan gratuito: NL, US, JP):")
    for k, (name, code) in COUNTRIES.items():
        free = " [FREE]" if code in ["NL", "US", "JP"] else ""
        print(f"  [{k}] {name} ({code}){free}")
    choice = input("\nSelecciona país (número): ").strip()
    return COUNTRIES.get(choice, (None, None))

def connect_protonvpn(country_code, real_user):
    print(f"[*] Conectando a ProtonVPN — {country_code}...")
    try:
        user_id = subprocess.run(
            ["id", "-u", real_user],
            capture_output=True, text=True
        ).stdout.strip()

        cmd = (
            f"export DISPLAY=:0; "
            f"export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/{user_id}/bus; "
            f"eval $(gnome-keyring-daemon --start --components=secrets); "
            f"protonvpn-app &"
        )

        subprocess.Popen(["su", real_user, "-c", cmd])
        time.sleep(3)
        print(f"[✓] ProtonVPN iniciado como {real_user}")
        print(f"[i] Conéctate al servidor de {country_code} en la interfaz gráfica.")
        return True
    except Exception as e:
        print(f"[!] Error al lanzar ProtonVPN: {e}")
        return False

# ─── Main ─────────────────────────────────────────────────

def main():
    check_root()
    real_user = get_real_user()

    print(BANNER)

    # Seleccionar interfaz
    interfaces = get_interfaces()
    if not interfaces:
        print("[!] No se encontraron interfaces.")
        sys.exit(1)

    print("Interfaces disponibles:")
    for i, iface in enumerate(interfaces, 1):
        ip = get_current_ip(iface) or "sin IP"
        mac = get_current_mac(iface) or "desconocida"
        print(f"  [{i}] {iface} — IP: {ip}  MAC: {mac}")

    choice = input("\nSelecciona interfaz (número): ").strip()
    try:
        iface = interfaces[int(choice) - 1]
    except (ValueError, IndexError):
        print("[!] Selección inválida.")
        sys.exit(1)

    # Capa 1: MAC
    print(f"\n[1/3] Cambiando MAC...")
    old_mac = get_current_mac(iface)
    new_mac = generate_random_mac()
    print(f"      Anterior: {old_mac}")
    print(f"      Nueva:    {new_mac}")
    if change_mac(iface, new_mac):
        print("      [✓] MAC cambiada")
    else:
        print("      [✗] Error al cambiar MAC")

    # Capa 2: IP
    print(f"\n[2/3] Renovando IP...")
    old_ip = get_current_ip(iface) or "sin IP"
    print(f"      Anterior: {old_ip}")
    print("      [1] DHCP automático")
    print("      [2] IP estática manual")
    ip_choice = input("      Método: ").strip()

    if ip_choice == "1":
        if change_ip_dhcp(iface, real_user):
            new_ip = get_current_ip(iface) or "pendiente"
            print(f"      [✓] Nueva IP: {new_ip}")
    elif ip_choice == "2":
        new_ip = input("      IP (ej: 192.168.1.50): ").strip()
        prefix = input("      Prefijo (default 24): ").strip() or "24"
        if change_ip_static(iface, new_ip, prefix):
            print(f"      [✓] IP asignada: {new_ip}/{prefix}")

    # Capa 3: ProtonVPN
    print(f"\n[3/3] ProtonVPN")
    country_name, country_code = select_country()
    if country_code:
        connect_protonvpn(country_code, real_user)
    else:
        print("      [!] País no válido, se omite VPN.")

    print("\n[i] Cambios temporales, se revierten al reiniciar.\n")

if __name__ == "__main__":
    main()

