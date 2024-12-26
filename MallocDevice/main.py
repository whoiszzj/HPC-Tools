import time
from datetime import datetime
import os
if __name__ == '__main__':
    print("Sleeping forever...")
    job_id = os.environ.get('SLURM_JOB_ID')
    content = "Master! I have malloced an instance for you!\nJob id is: {}\ncreate time: {}".format(job_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(content)
    #os.system("email -c '{}'".format(content))
    while True:
        time.sleep(60)
