import psutil

def kill_python():
    for proc in psutil.process_iter():
        if proc.name() == "python3":
            proc.kill()

kill_python()