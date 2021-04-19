import os
import psutil
import subprocess
import time

from flask import Flask, request

app = Flask(__name__)


def start_program(program_name):
    if program_name == "index":
        subprocess.Popen("cd ~/index; ./index chunks 5000 2> errs 1> logs ")
    elif program_name == "TestSingleCrawler":
        index_host = os.environ['INDEX_HOST']
        index_port = os.environ['INDEX_PORT']
        crawler_port = os.environ['THIS_CRAWLER_PORT']
        # TODO: forward the entire environment
        # my_env = os.environ.copy()
        # my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]
        # subprocess.Popen(my_command, env=my_env)

        subprocess.Popen("cd ~/crawler; export INDEX_HOST=" + index_host + "; export INDEX_PORT=" + index_port +
                         "; THIS_CRAWLER_PORT=" + crawler_port + " ./TestSingleCrawler 2> err1 1> /dev/null",
                         shell=True)


@app.route('/status')
def status():
    program = request.args.get('program')

    # check if program is running, if so return "success" right away
    if program in (p.name() for p in psutil.process_iter()):
        return "success\n"
    else:
        # if program is not running check status code of how it ended. 
        home_dir = os.getenv("HOME")
        if os.path.exists(home_dir + "/crawler/seedlist.txt"):
            last_mod_time = os.path.getmtime(home_dir + "/crawler/seedlist.txt")
            epoch_time = int(time.time())
            if epoch_time - last_mod_time < 120:
                # If 0, restart it and return "success"
                start_program(program)
                return "success\n"
            else:
                # Otherwise return "fail" and restart the program
                start_program(program)
                return "fail\n", 404
        else:
            return "seedlist does not exist..."


if __name__ == '__main__':
    app.run(port=6000, host='0.0.0.0')
