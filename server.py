# listens for bytes, then sends data to the http parser (decoder/encoder)

import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 5000))
    s.listen()
    print("Waiting for connection...")
    conn, addr = s.accept()

    with conn:
        print(f"Connection recieved at {addr}")
        while True:
            data = conn.recv(8192)
            text = str(data, "utf-8")
            conn.sendall(bytes(text, "utf-8"))
