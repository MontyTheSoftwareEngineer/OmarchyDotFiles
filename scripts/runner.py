#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

# Color codes - Using bright/bold versions for better tmux compatibility
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[1;34m'      # Bold Blue
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[31m'       # Bold Red (bright red)
    WHITE = '\033[1;37m'     # Bold White (bright white)
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'

class Config:
    FILE = Path.home() / ".kona_config"
    PASSWORD = "3055DeerLoonPanda"
    SSH_OPTS = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    
class Paths:
    NATIVE_BUILD = "/home/hpham/MVE/builds/kona-gui-build-native"
    TARGET_BUILD = "/home/hpham/MVE/builds/kona-gui-build-target"
    MUX_REPO = "/home/hpham/MVE/repos/kona-qt/kona_mux"
    FIRMWARE_SRC = "/home/hpham/MVE/repos/kona-qt/source/Debug"
    QT_PATH = "/home/hpham/Qt/6.7.0/gcc_64/bin/qmake"
    SDK_QMAKE = "/opt/verdin6.7-all/4.0.16/sysroots/x86_64-pokysdk-linux/usr/bin/qmake"

import base64
import shutil

def _script_dir() -> Path:
    return Path(__file__).resolve().parent

def _in_tty() -> bool:
    return sys.stdout.isatty()

def _is_kitty() -> bool:
    return bool(os.environ.get("KITTY_WINDOW_ID") or os.environ.get("TERM", "").startswith("xterm-kitty"))

def _is_iterm2() -> bool:
    return os.environ.get("TERM_PROGRAM") == "iTerm.app"

def get_terminal_width() -> int:
    """Get terminal width, default to 80 if not available"""
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def center_print(text: str):
    """Print text centered in terminal"""
    term_width = get_terminal_width()
    # The banner is 65 chars wide (including the border)
    content_width = 65
    if term_width > content_width:
        padding = (term_width - content_width) // 2
        print(' ' * padding + text)
    else:
        print(text)

def center_input(prompt: str) -> str:
    """Get centered input with prompt"""
    term_width = get_terminal_width()
    content_width = 65
    if term_width > content_width:
        padding = (term_width - content_width) // 2
        # Print the prompt centered, then get input on same line
        print(' ' * padding, end='')
    return input(prompt)

def show_splash_image():
    """Best-effort splash image in terminals that support it."""
    if not _in_tty():
        return

    img = _script_dir() / "shark.png"
    if not img.exists():
        return

    # Clear a little space at top (optional)
    print("\n", end="")

    # Kitty (recommended on Linux)
    if _is_kitty() and shutil.which("kitty"):
        # Place it at the top, scaled to a reasonable size
#        subprocess.call(["kitty", "+kitten", "icat", "--align", "center", "--scale-up", str(img)])
        # Use 'direct' transfer mode for tmux compatibility
        subprocess.call([
            "kitty", "+kitten", "icat",
            "--transfer-mode", "stream",
            str(img)
        ])


        return

    # iTerm2 inline images (macOS iTerm2)
    if _is_iterm2():
        data = img.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        # width can be "auto" or e.g. "50%"
        sys.stdout.write(f"\033]1337;File=inline=1;width=50%;preserveAspectRatio=1:{b64}\a\n")
        sys.stdout.flush()
        return

    # Fallback (no image protocol available)
    # print("[splash: shark.png (terminal does not support inline images)]")

def print_banner():
    """Print a cool ASCII art banner"""
    # Each line has exactly 63 chars between the borders
    center_print(f"{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}                                                                  {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}        {Colors.RED}██████╗██████╗ ██╗   ██╗ ██████╗{Colors.ENDC}                          {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}       {Colors.RED}██╔════╝██╔══██╗╚██╗ ██╔╝██╔═══██╗{Colors.ENDC}                         {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}       {Colors.WHITE}██║     ██████╔╝ ╚████╔╝ ██║   ██║{Colors.ENDC}                         {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}       {Colors.WHITE}██║     ██╔══██╗  ╚██╔╝  ██║   ██║{Colors.ENDC}                         {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}       {Colors.BLUE}╚██████╗██║  ██║   ██║   ╚██████╔╝{Colors.ENDC}                         {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}       {Colors.BLUE} ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝{Colors.ENDC}                          {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}                                                                  {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}   {Colors.RED}██████╗ ██████╗ ███╗   ██╗███╗   ██╗███████╗ ██████╗████████╗{Colors.ENDC}  {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.RED}██╔════╝██╔═══██╗████╗  ██║████╗  ██║██╔════╝██╔════╝╚══██╔══╝{Colors.ENDC}  {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.WHITE}██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██║        ██║{Colors.ENDC}     {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.WHITE}██║     ██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║        ██║{Colors.ENDC}     {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.BLUE}╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║███████╗╚██████╗   ██║{Colors.ENDC}     {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.BLUE} ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═╝{Colors.ENDC}     {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}                                                                  {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}║{Colors.ENDC}                    Development Runner                            {Colors.BOLD}║{Colors.ENDC}")
    center_print(f"{Colors.BOLD}╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")

def print_menu(target_ip: Optional[str]):
    """Print the main menu with colors and status indicators"""
    ip_display = f"{target_ip}" if target_ip else "Not Set"
    # Calculate padding to align right border (61 total visible chars)
    ip_label = "Target IP: "
    ip_icon = "✓ " if target_ip else "✗ "
    ip_content_len = len(ip_label) + len(ip_icon) + len(ip_display)
    ip_padding = 61 - ip_content_len
    
    if target_ip:
        ip_status = f"{Colors.DIM}{ip_label}{Colors.ENDC}{Colors.GREEN}{ip_icon}{ip_display}{Colors.ENDC}"
    else:
        ip_status = f"{Colors.DIM}{ip_label}{Colors.ENDC}{Colors.RED}{ip_icon}{ip_display}{Colors.ENDC}"
    
    print()  # Newline before menu
    center_print(f"{Colors.BOLD}╔═════════════════════════════════════════════════════════════════╗")
    center_print(f"║{Colors.ENDC}  {ip_status}{' ' * ip_padding}  {Colors.BOLD}║")
    center_print(f"╠═════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
    
    menu_items = [
        ("", "COMPILATION", "header"),
        ("1", "Compile Native", "action"),
        ("2", "Compile Target", "action"),
        ("3", "Compile Mux Target", "action"),
        ("4", "Build Firmware (Customer/Manufacturing)", "action"),
        ("", "", "separator"),
        ("", "DEPLOYMENT", "header"),
        ("5", "Deploy Target", "action"),
        ("6", "Deploy Mux", "action"),
        ("7", "Deploy Firmware", "action"),
        ("8", "Deploy Test App", "action"),
        ("9", "Flash STM Firmware", "special"),
        ("", "", "separator"),
        ("", "EXECUTION", "header"),
        ("10", "Run Native", "action"),
        ("11", "Run Target", "action"),
        ("12", "Run Mux", "action"),
        ("13", "Run Test App", "action"),
        ("", "", "separator"),
        ("", "SYSTEM CONTROL", "header"),
        ("14", "Kill GUI + Mux", "danger"),
        ("15", "SSH to Target", "action"),
        ("16", "Set Target IP", "config"),
        ("", "", "separator"),
        ("0", "Exit", "exit"),
    ]
    
    for num, desc, item_type in menu_items:
        if item_type == "header":
            # Center the header text (61 total visible chars)
            padding_total = 61 - len(desc)
            padding_left = padding_total // 2
            padding_right = padding_total - padding_left
            center_print(f"{Colors.BOLD}║{Colors.ENDC}  {' ' * padding_left}{Colors.YELLOW}{Colors.BOLD}{desc}{Colors.ENDC}{' ' * padding_right}  {Colors.BOLD}║{Colors.ENDC}")
        elif item_type == "separator":
            center_print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.DIM}{'─' * 61}{Colors.ENDC}  {Colors.BOLD}║{Colors.ENDC}")
        elif item_type == "action":
            # Format: "NN │ description" (2 + 3 + desc, need to pad to 61)
            content_len = 2 + 3 + len(desc)
            padding = 61 - content_len
            center_print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.CYAN}{num:>2}{Colors.ENDC} │ {Colors.BOLD}{desc}{Colors.ENDC}{' ' * padding}  {Colors.BOLD}║{Colors.ENDC}")
        elif item_type == "special":
            content_len = 2 + 3 + len(desc)
            padding = 61 - content_len
            center_print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.HEADER}{num:>2}{Colors.ENDC} │ {Colors.BOLD}{desc}{Colors.ENDC}{' ' * padding}  {Colors.BOLD}║{Colors.ENDC}")
        elif item_type == "danger":
            content_len = 2 + 3 + len(desc)
            padding = 61 - content_len
            center_print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.RED}{num:>2}{Colors.ENDC} │ {Colors.BOLD}{desc}{Colors.ENDC}{' ' * padding}  {Colors.BOLD}║{Colors.ENDC}")
        elif item_type == "config":
            content_len = 2 + 3 + len(desc)
            padding = 61 - content_len
            center_print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.GREEN}{num:>2}{Colors.ENDC} │ {Colors.BOLD}{desc}{Colors.ENDC}{' ' * padding}  {Colors.BOLD}║{Colors.ENDC}")
        elif item_type == "exit":
            content_len = 2 + 3 + len(desc)
            padding = 61 - content_len
            center_print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.DIM}{num:>2}{Colors.ENDC} │ {Colors.DIM}{desc}{Colors.ENDC}{' ' * padding}  {Colors.BOLD}║{Colors.ENDC}")
    
    center_print(f"{Colors.BOLD}╚═════════════════════════════════════════════════════════════════╝{Colors.ENDC}")

def status_msg(msg: str, status: str = "info"):
    """Print a status message with icon"""
    icons = {
        "info": f"{Colors.BLUE}ℹ{Colors.ENDC}",
        "success": f"{Colors.GREEN}✓{Colors.ENDC}",
        "error": f"{Colors.RED}✗{Colors.ENDC}",
        "warning": f"{Colors.YELLOW}⚠{Colors.ENDC}",
        "running": f"{Colors.CYAN}▶{Colors.ENDC}",
    }
    print(f"\n{icons.get(status, icons['info'])} {msg}")

def pause():
    """Wait for user to press enter"""
    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.ENDC}")

def load_ip() -> Optional[str]:
    """Load target IP from config file"""
    if Config.FILE.exists():
        return Config.FILE.read_text().strip()
    return None

def save_ip(ip: str):
    """Save target IP to config file"""
    Config.FILE.write_text(ip)

def run_ssh_cmd(ip: str, cmd: str, interactive: bool = False) -> int:
    """Run SSH command on target"""
    ssh_cmd = f"sshpass -p '{Config.PASSWORD}' ssh {Config.SSH_OPTS} root@{ip}"
    if interactive:
        if cmd:
            return subprocess.call(f"{ssh_cmd} \"{cmd}\"", shell=True)
        else:
            return subprocess.call(f"{ssh_cmd}", shell=True)
    else:
        return subprocess.call(f"{ssh_cmd} \"{cmd}\"", shell=True)

def run_scp(ip: str, src: str, dst: str) -> int:
    """Copy file to target via SCP"""
    return subprocess.call(
        f"sshpass -p '{Config.PASSWORD}' scp {Config.SSH_OPTS} {src} root@{ip}:{dst}",
        shell=True
    )

def compile_native():
    """Compile native build"""
    status_msg("Compiling native build...", "running")
    try:
        os.chdir(Paths.NATIVE_BUILD)
        subprocess.call([
            Paths.QT_PATH,
            'DEFINES+=RESET_KEY=\\\\\\\"MVESecurityThroughSystems\\\\\\\"',
            'DEFINES+=DEVELOPER_MODE_BUILD=1',
            'DEFINES+=DEBUG_KEY=1',
            '../../repos/kona-qt/kona_gui_app'
        ])
        subprocess.call(['make', '-j12'])
        status_msg("Compilation complete!", "success")
    except Exception as e:
        status_msg(f"Compilation failed: {e}", "error")
    pause()

def compile_target():
    """Compile target build"""
    status_msg("Compiling target build...", "running")
    try:
        os.chdir(Paths.TARGET_BUILD)
        subprocess.call([
            Paths.SDK_QMAKE,
            'DEFINES+=DEVELOPER_MODE_BUILD=1',
            '../../repos/kona-qt/kona_gui_app'
        ])
        subprocess.call(['make', '-j12'])
        status_msg("Compilation complete!", "success")
    except Exception as e:
        status_msg(f"Compilation failed: {e}", "error")
    pause()

def deploy_target():
    """Deploy to target device"""
    ip = load_ip()
    if not ip:
        status_msg("Target IP not set. Please set it first.", "error")
        pause()
        return
    
    status_msg(f"Deploying to {ip}...", "running")
    os.chdir(Paths.TARGET_BUILD)
    run_ssh_cmd(ip, "systemctl stop kona-gui")
    run_ssh_cmd(ip, "killall stasis")
    run_scp(ip, "stasis", "/usr/bin/kona")
    status_msg("Deployment complete!", "success")
    pause()

def deploy_test():
    """Deploy test app to target"""
    ip = load_ip()
    if not ip:
        status_msg("Target IP not set. Please set it first.", "error")
        pause()
        return
    
    status_msg(f"Deploying test app to {ip}...", "running")
    os.chdir(Paths.TARGET_BUILD)
    run_ssh_cmd(ip, "killall test_stasis 2>/dev/null || true")
    run_scp(ip, "stasis", "/usr/bin/kona/test_stasis")
    status_msg("Test app deployed!", "success")
    pause()

def run_target():
    """Run application on target"""
    ip = load_ip()
    if not ip:
        status_msg("Target IP not set. Please set it first.", "error")
        pause()
        return
    
    status_msg(f"Running on target {ip}...", "running")
    try:
        run_ssh_cmd(ip, "/usr/bin/kona/stasis", interactive=True)
    except KeyboardInterrupt:
        status_msg("Interrupted - returning to menu", "warning")
    pause()

def run_test():
    """Run test app on target"""
    ip = load_ip()
    if not ip:
        status_msg("Target IP not set. Please set it first.", "error")
        pause()
        return
    
    status_msg(f"Running test app on {ip}...", "running")
    try:
        run_ssh_cmd(ip, "/usr/bin/kona/test_stasis", interactive=True)
    except KeyboardInterrupt:
        status_msg("Interrupted - returning to menu", "warning")
    pause()

def run_native():
    """Run native build"""
    status_msg("Starting native build...", "running")
    subprocess.Popen([f"{Paths.NATIVE_BUILD}/stasis"])
    status_msg("Native build started in background", "success")
    pause()

def set_target_ip():
    """Set target IP address"""
    print(f"\n{Colors.GREEN}{Colors.BOLD}Current IP:{Colors.ENDC} {load_ip() or 'Not set'}")
    new_ip = input(f"{Colors.CYAN}Enter new target IP:{Colors.ENDC} ").strip()
    if new_ip:
        save_ip(new_ip)
        status_msg(f"Target IP set to {new_ip}", "success")
    else:
        status_msg("IP not changed", "warning")
    pause()

def ssh_to_target():
    """SSH into target device"""
    ip = load_ip()
    if not ip:
        status_msg("Target IP not set. Please set it first.", "error")
        pause()
        return
    
    status_msg(f"Connecting to {ip}...", "running")
    try:
        run_ssh_cmd(ip, "", interactive=True)
    except KeyboardInterrupt:
        status_msg("Disconnected - returning to menu", "warning")
    pause()

def compile_mux_target():
    """Compile mux for target"""
    status_msg("Compiling mux target...", "running")
    try:
        os.chdir(Paths.MUX_REPO)
        subprocess.call(['cargo', 'build', '--target=aarch64-unknown-linux-gnu', '--release'])
        status_msg("Mux compilation complete!", "success")
    except Exception as e:
        status_msg(f"Compilation failed: {e}", "error")
    pause()

def build_firmware():
    """Build firmware (customer or manufacturing)"""
    print(f"\n{Colors.YELLOW}{Colors.BOLD}Build Type:{Colors.ENDC}")
    print(f"  {Colors.CYAN}1{Colors.ENDC} │ Manufacturing (Development)")
    print(f"  {Colors.CYAN}2{Colors.ENDC} │ Customer")
    
    choice = input(f"\n{Colors.BOLD}{Colors.CYAN}➜{Colors.ENDC} Select build type: ").strip()
    
    if choice == '1':
        build_target = 'manufacturing-build'
        status_msg("Building manufacturing firmware...", "running")
    elif choice == '2':
        build_target = 'customer-build'
        status_msg("Building customer firmware...", "running")
    else:
        status_msg("Invalid selection!", "error")
        pause()
        return
    
    try:
        os.chdir(Paths.FIRMWARE_SRC)
        subprocess.call(['make', 'clean'])
        subprocess.call(['make', build_target, '-j12'])
        status_msg("Firmware build complete!", "success")
    except Exception as e:
        status_msg(f"Build failed: {e}", "error")
    pause()

def deploy_firmware():
    """Deploy firmware to target"""
    ip = load_ip()
    if not ip:
        status_msg("Target IP not set. Please set it first.", "error")
        pause()
        return
    
    status_msg(f"Deploying firmware to {ip}...", "running")
    firmware_path = f"{Paths.FIRMWARE_SRC}/stasis_fw.bin"
    
    if not os.path.exists(firmware_path):
        status_msg(f"Firmware file not found: {firmware_path}", "error")
        pause()
        return
    
    run_scp(ip, firmware_path, "/usr/bin/kona/stasis_fw.bin")
    status_msg("Firmware deployed!", "success")
    pause()

def deploy_mux():
    """Deploy mux to target"""
    ip = load_ip()
    if not ip:
        status_msg("Target IP not set. Please set it first.", "error")
        pause()
        return
    
    status_msg(f"Deploying mux to {ip}...", "running")
    run_ssh_cmd(ip, "systemctl stop kona-mux; killall stasis_mux")
    mux_path = f"{Paths.MUX_REPO}/target/aarch64-unknown-linux-gnu/release/stasis_mux"
    run_scp(ip, mux_path, "/usr/bin/kona/stasis_mux")
    status_msg("Mux deployed!", "success")
    pause()

def kill_gui_and_mux():
    """Stop GUI and mux services"""
    ip = load_ip()
    if not ip:
        status_msg("Target IP not set. Please set it first.", "error")
        pause()
        return
    
    status_msg(f"Stopping services on {ip}...", "running")
    run_ssh_cmd(ip, "systemctl stop kona-gui; systemctl stop kona-mux; killall stasis; killall stasis_mux")
    status_msg("Services stopped!", "success")
    pause()

def run_mux():
    """Start mux service on target"""
    ip = load_ip()
    if not ip:
        status_msg("Target IP not set. Please set it first.", "error")
        pause()
        return
    
    status_msg(f"Starting mux on {ip}...", "running")
    run_ssh_cmd(ip, "systemctl start kona-mux")
    status_msg("Mux started!", "success")
    pause()

def flash_stm_firmware():
    """Flash STM firmware on target"""
    ip = load_ip()
    if not ip:
        status_msg("Target IP not set. Please set it first.", "error")
        pause()
        return
    
    status_msg(f"Flashing STM firmware on {ip}...", "running")
    
    python_script = r"""
import subprocess
import sys
import time
import serial

firmware_path = sys.argv[1]

def check_dfu():
    result = subprocess.run("lsusb", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0 and "DFU" in result.stdout:
        return 0
    return 1

def find_device_port():
    print("Looking for STM device...")
    result = subprocess.run(["ls", "-l", "/dev/serial/by-id"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        for item in result.stdout.strip().split('\n'):
            if "STM" in item:
                rPath = item.split()[-1]
                port = "/dev/" + rPath.split('/')[-1]
                print(f"Found STM device at: {port}")
                return port
        if check_dfu() == 0:
            print("Device is already in DFU mode")
            return None
        print("ERROR: No STM device found")
        return None
    else:
        if check_dfu() == 0:
            print("Device is already in DFU mode")
            return None
        print("ERROR: Could not find serial devices")
        return None

def calculate_crc(data):
    wCRCTable = [0X0000, 0XC0C1, 0XC181, 0X0140, 0XC301, 0X03C0, 0X0280, 0XC241, 0XC601, 0X06C0, 0X0780, 0XC741, 0X0500, 0XC5C1, 0XC481, 0X0440, 0XCC01, 0X0CC0, 0X0D80, 0XCD41, 0X0F00, 0XCFC1, 0XCE81, 0X0E40, 0X0A00, 0XCAC1, 0XCB81, 0X0B40, 0XC901, 0X09C0, 0X0880, 0XC841, 0XD801, 0X18C0, 0X1980, 0XD941, 0X1B00, 0XDBC1, 0XDA81, 0X1A40, 0X1E00, 0XDEC1, 0XDF81, 0X1F40, 0XDD01, 0X1DC0, 0X1C80, 0XDC41, 0X1400, 0XD4C1, 0XD581, 0X1540, 0XD701, 0X17C0, 0X1680, 0XD641, 0XD201, 0X12C0, 0X1380, 0XD341, 0X1100, 0XD1C1, 0XD081, 0X1040, 0XF001, 0X30C0, 0X3180, 0XF141, 0X3300, 0XF3C1, 0XF281, 0X3240, 0X3600, 0XF6C1, 0XF781, 0X3740, 0XF501, 0X35C0, 0X3480, 0XF441, 0X3C00, 0XFCC1, 0XFD81, 0X3D40, 0XFF01, 0X3FC0, 0X3E80, 0XFE41, 0XFA01, 0X3AC0, 0X3B80, 0XFB41, 0X3900, 0XF9C1, 0XF881, 0X3840, 0X2800, 0XE8C1, 0XE981, 0X2940, 0XEB01, 0X2BC0, 0X2A80, 0XEA41, 0XEE01, 0X2EC0, 0X2F80, 0XEF41, 0X2D00, 0XEDC1, 0XEC81, 0X2C40, 0XE401, 0X24C0, 0X2580, 0XE541, 0X2700, 0XE7C1, 0XE681, 0X2640, 0X2200, 0XE2C1, 0XE381, 0X2340, 0XE101, 0X21C0, 0X2080, 0XE041, 0XA001, 0X60C0, 0X6180, 0XA141, 0X6300, 0XA3C1, 0XA281, 0X6240, 0X6600, 0XA6C1, 0XA781, 0X6740, 0XA501, 0X65C0, 0X6480, 0XA441, 0X6C00, 0XACC1, 0XAD81, 0X6D40, 0XAF01, 0X6FC0, 0X6E80, 0XAE41, 0XAA01, 0X6AC0, 0X6B80, 0XAB41, 0X6900, 0XA9C1, 0XA881, 0X6840, 0X7800, 0XB8C1, 0XB981, 0X7940, 0XBB01, 0X7BC0, 0X7A80, 0XBA41, 0XBE01, 0X7EC0, 0X7F80, 0XBF41, 0X7D00, 0XBDC1, 0XBC81, 0X7C40, 0XB401, 0X74C0, 0X7580, 0XB541, 0X7700, 0XB7C1, 0XB681, 0X7640, 0X7200, 0XB2C1, 0XB381, 0X7340, 0XB101, 0X71C0, 0X7080, 0XB041, 0X5000, 0X90C1, 0X9181, 0X5140, 0X9301, 0X53C0, 0X5280, 0X9241, 0X9601, 0X56C0, 0X5780, 0X9741, 0X5500, 0X95C1, 0X9481, 0X5440, 0X9C01, 0X5CC0, 0X5D80, 0X9D41, 0X5F00, 0X9FC1, 0X9E81, 0X5E40, 0X5A00, 0X9AC1, 0X9B81, 0X5B40, 0X9901, 0X59C0, 0X5880, 0X9841, 0X8801, 0X48C0, 0X4980, 0X8941, 0X4B00, 0X8BC1, 0X8A81, 0X4A40, 0X4E00, 0X8EC1, 0X8F81, 0X4F40, 0X8D01, 0X4DC0, 0X4C80, 0X8C41, 0X4400, 0X84C1, 0X8581, 0X4540, 0X8701, 0X47C0, 0X4680, 0X8641, 0X8201, 0X42C0, 0X4380, 0X8341, 0X4100, 0X81C1, 0X8081, 0X4040]
    wCRCWord = 0xFFFF
    for byte in data:
        byte = byte & 0xFF
        nTemp = (byte ^ (wCRCWord & 0x00FF)) & 0x00FF
        wCRCWord = ((wCRCWord >> 8) ^ wCRCTable[nTemp]) & 0xFFFF
    return wCRCWord

def create_dfu_command():
    request = [0x53, 0x3D, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3D, 0x45]
    crc = calculate_crc(request[6:])
    request[3] = crc & 0xFF
    request[4] = (crc >> 8) & 0xFF
    return bytearray(request)

def set_dfu_mode(port):
    print(f"Sending DFU mode command to {port}...")
    try:
        ser = serial.Serial(port=port, baudrate=115200, timeout=0.5)
        ser.write(create_dfu_command())
        time.sleep(1)
        ser.close()
        print("DFU command sent")
        time.sleep(2)
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    return True

if check_dfu() == 0:
    print("Device already in DFU mode")
else:
    port = find_device_port()
    if port is None:
        sys.exit(1)
    if not set_dfu_mode(port):
        sys.exit(1)
    if check_dfu() != 0:
        print("ERROR: Device did not enter DFU mode")
        sys.exit(1)
    print("Device is now in DFU mode")

print(f"Flashing firmware: {firmware_path}")
result = subprocess.run(["dfu-util", "-d", "0483:df11", "-a", "0", "-D", firmware_path, "--dfuse-address", "0x08000000:leave"])
sys.exit(result.returncode)
"""
    
    cmd = f"sshpass -p '{Config.PASSWORD}' ssh {Config.SSH_OPTS} root@{ip} 'python3 - /usr/bin/kona/stasis_fw.bin' << 'PYTHON_SCRIPT'\n{python_script}\nPYTHON_SCRIPT"
    result = subprocess.call(cmd, shell=True)
    
    if result == 0:
        status_msg("Firmware flashed successfully!", "success")
    else:
        status_msg("Firmware flashing failed!", "error")
    pause()

def main():
    """Main menu loop"""
    while True:
        os.system('clear')
        show_splash_image()
        print_banner()
        target_ip = load_ip()
        print_menu(target_ip)
        
        try:
            choice = center_input(f"\n{Colors.BOLD}{Colors.CYAN}➜{Colors.ENDC} Choose an option: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{Colors.YELLOW}Goodbye!{Colors.ENDC}")
            sys.exit(0)
        
        actions = {
            '1': compile_native,
            '2': compile_target,
            '3': compile_mux_target,
            '4': build_firmware,
            '5': deploy_target,
            '6': deploy_mux,
            '7': deploy_firmware,
            '8': deploy_test,
            '9': flash_stm_firmware,
            '10': run_native,
            '11': run_target,
            '12': run_mux,
            '13': run_test,
            '14': kill_gui_and_mux,
            '15': ssh_to_target,
            '16': set_target_ip,
            '0': lambda: sys.exit(0),
        }
        
        if choice in actions:
            actions[choice]()
        else:
            status_msg("Invalid option!", "error")
            pause()

if __name__ == "__main__":
    main()
