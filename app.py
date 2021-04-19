import os
import psutil
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route('/status')
def status():
    program = request.args.get('program')

    # check if program is running, if so return "success" right away
    if ( program in ( p.name( ) for p in psutil.process_iter( ) ) ):
        return "success"
    else:
        # if program is not running check status code of how it ended. 
        bashCommand = "echo $?"
        result = subprocess.check_output( bashCommand, shell=True )
        if ( result == 0 ):
            # If 0, restart it and return "success"
            start_progam( program )
            return "success"
        else:
            # Otherwise return "fail" and restart the program
            start_progam( program )
            return "fail"

def start_program(program_name):
    if program_name == "index":
        os.system("cd ~/index; ./index chunks 5000 2> errs 1> logs")
    elif program_name == "TestSingleCrawler":
        os.system("cd ~/crawler; THIS_CRAWLER_PORT=8000 ./TestSingleCrawler 2> err1 1> /dev/null")

if __name__ == '__main__':
    app.run()
