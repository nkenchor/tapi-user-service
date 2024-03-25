import socket


def get_server_ip():
    """Attempt to find the server's IP address (best guess)."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # This doesn't actually create a connection
            # 8.8.8.8 is Google's public DNS server
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"