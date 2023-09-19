import threading
from get_proxy import get_proxy_threads
from http_srv import run_thread_http_srv

lock = threading.Lock()


if __name__ == '__main__':
    get_proxy_threads()
    run_thread_http_srv()
