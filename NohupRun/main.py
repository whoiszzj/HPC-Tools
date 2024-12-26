import os
import sys
from pathlib import Path
import time


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: nrun [cmd] [arg1] [arg2] ...")
        sys.exit(1)
    
    # get current path
    current_path = Path.cwd()
    print("Current path: ", current_path)
    cmd_args = sys.argv[1:]
    log_name = "nrun_" + str(os.getpid()) + ".log"
    log_path = os.path.join(current_path, log_name)
    redirect = " > "
    if os.path.exists(log_path):
        redirect = " >> "
    # get current time
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    cmd = "nohup " + " ".join(cmd_args) + redirect + log_path + " 2>&1 &"
    print("Command line: ", cmd)
    sys.exit(os.system(cmd))
