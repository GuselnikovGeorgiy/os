import os
import sys
from datetime import datetime
import time

LOG_PATH_1 = "logs_server1.txt"
LOG_PATH_2 = "logs_server2.txt"

def makefifo_if_not_exists(fifo_path):
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)

def server_log(server_id, log_file):
    while True:
        with open(log_file, "a") as log:
            try:
                fifo_path = f"fifo_{server_id}"
                makefifo_if_not_exists(fifo_path)

                with open(fifo_path, "r") as fifo:
                    data = fifo.read()
                    if data:
                        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
                        log.write(f"{timestamp} Server {server_id}: {data}\n")
            except Exception:
                os.unlink(fifo_path)
                sys.exit(0)


def main():
    server1_pid = os.fork()

    if server1_pid > 0:
        server2_pid = os.fork()

        if server2_pid > 0:
            os.waitpid(server1_pid, 0)
            os.waitpid(server2_pid, 0)
        else:
            server_log(2, LOG_PATH_2)
    else:
        server_log(1, LOG_PATH_1)

if __name__ == "__main__":
    main()
