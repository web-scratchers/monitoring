import os
import psutil
import subprocess
import time

from flask import Flask, request

app = Flask(__name__)


def start_program(program_name):
    if program_name == "index":
        os.system("cd ~/index; ./index chunks 5000 2> errs 1> logs")
    elif program_name == "TestSingleCrawler":
        os.system("cd ~/crawler; THIS_CRAWLER_PORT=8000 ./TestSingleCrawler 2> err1 1> /dev/null")


@app.route('/status')
def status():
    program = request.args.get('program')
    print( int( time.time( ) ) )

    # check if program is running, if so return "success" right away
    if program in ( p.name( ) for p in psutil.process_iter( ) ):
        return "success"
    else:
        # if program is not running check status code of how it ended. 
        lastModTime = os.path.getmtime( "~/crawler/seedlist.txt" )
        epoch_time = int( time.time( ) )
        if epoch_time - lastModTime < 120:
            # If 0, restart it and return "success"
            start_program( program )
            return "success"
        else:
            # Otherwise return "fail" and restart the program
            start_program( program )
            return "fail"


if __name__ == '__main__':
    app.run()
