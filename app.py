import os
import psutil
import time

from flask import Flask, request

app = Flask(__name__)


def start_program(program_name):
    if program_name == "index":
        cmd1 = "cd ~/index"
        cmd2 = "./index chunks 5000 2> errs 1> logs"
        subprocess.run(cmd1.split())
        subprocess.run(cmd2.split())
        time.sleep(5)
    elif program_name == "TestSingleCrawler":
        cmd1 = "cd ~/crawler"
        cmd2 = "THIS_CRAWLER_PORT=8000 ./TestSingleCrawler 2> err1 1> /dev/null"
        subprocess.run(cmd1.split())
        subprocess.run(cmd2.split())
        time.sleep(5)


@app.route('/status')
def status():
    program = request.args.get('program')

    # check if program is running, if so return "success" right away
    if program in ( p.name( ) for p in psutil.process_iter( ) ):
        return "success\n"
    else:
        # if program is not running check status code of how it ended. 
        homeDir = os.getenv("HOME")
        if os.path.exists( homeDir + "/crawler/seedlist.txt" ):
            lastModTime = os.path.getmtime( homeDir + "/crawler/seedlist.txt" )
            epoch_time = int( time.time( ) )
            if epoch_time - lastModTime < 120:
                # If 0, restart it and return "success"
                start_program( program )
                return "success\n"
            else:
                # Otherwise return "fail" and restart the program
                start_program( program )
                return "fail\n"
        else:
            return "seedlist does not exist..."


if __name__ == '__main__':
    app.run( port = 6000 )
