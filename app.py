import os
import psutil
import subprocess
import time

from flask import Flask, request

app = Flask(__name__)


def start_program(program_name):
    if program_name == "index":
        subprocess.Popen("cd ~/index; ulimit -c unlimited; ulimit -n 8192; ./index chunks 5000 2> errs 1> /dev/null ", shell=True)
    elif program_name == "TestSingleCrawler":
        index_host = os.environ['INDEX_HOST']
        index_port = os.environ['INDEX_PORT']
        crawler_port = os.environ['THIS_CRAWLER_PORT']
        total_crawlers = os.environ['TOTAL_CRAWLERS']
        this_crawler_id = os.environ['THIS_CRAWLER_ID']
        # TODO: forward the entire environment
        # my_env = os.environ.copy()
        # my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]
        # subprocess.Popen(my_command, env=my_env)

        subprocess.Popen("cd ~/crawler; ulimit -c unlimited; ulimit -n 8192; export INDEX_HOST=" + index_host + "; export INDEX_PORT=" + index_port +
                         "; THIS_CRAWLER_PORT=" + crawler_port + " ./TestSingleCrawler " + this_crawler_id + " " + 
                         total_crawlers + " 800 2> err1 1> /dev/null",
                         shell=True)


def kill_process(process_name):
    sp = subprocess.Popen("ps aux | grep TestSingleCrawler", shell=True, stdout=subprocess.PIPE)
    output, error = sp.communicate()
    for line in output.splitlines():
        if process_name in str(line) and "/bin/sh" not in str(line):
            pid = int(line.split()[1])
            os.kill(pid, 9)


@app.route('/status')
def status():
    program = request.args.get('program')
    home_dir = os.getenv("HOME")
    epoch_time = int(time.time())
    # check if program is running, if so return "success" right away
    if program in (p.name() for p in psutil.process_iter()):
        if program == "TestSingleCrawler":
            if os.path.exists(home_dir + "/crawler/seedlist_temp.txt"):
                last_mod_time = os.path.getmtime(home_dir + "/crawler/seedlist_temp.txt")
                if epoch_time - last_mod_time >= 600:
                    kill_process(program)
                    start_program(program)
                    os.remove(home_dir + "/crawler/seedlist_temp.txt")
                    return "fail\tthe seedlist has been writing > 10 mins (restarted crawler)\n", 408
            if os.path.exists(home_dir + "/crawler/already_crawled_urls_temp"):
                last_mod_time = os.path.getmtime(home_dir + "/crawler/already_crawled_urls_temp")
                if epoch_time - last_mod_time >= 600:
                    kill_process(program)
                    start_program(program)
                    os.remove(home_dir + "/crawler/already_crawled_urls_temp")
                    return "fail\tthe alreadyCrawledUrls has been writing > 10 mins (restarted crawler)\n", 408
        return "success\n"
    else:
        # if program is not running check status code of how it ended.
        if ( program == "index" ):
            start_program(program)
            return "fail\n", 404
        if os.path.exists(home_dir + "/crawler/seedlist.txt"):
            last_mod_time = os.path.getmtime(home_dir + "/crawler/seedlist.txt")
            if epoch_time - last_mod_time < 120:
                # If 0, restart it and return "success"
                start_program(program)
                return "success\n"
            else:
                # Otherwise return "fail" and restart the program
                start_program(program)
                return "fail\n", 404
        else:
            return "fail\nNo seed list\n", 403
            # return "seedlist does not exist..."


if __name__ == '__main__':
    app.run(port=6000, host='0.0.0.0')
