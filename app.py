import os

from flask import Flask, request

app = Flask(__name__)


@app.route('/status')
def status():
    program = request.args.get('program')

    # check if program is running, if so return "success" right away

    # if program is not running check status code of how it ended. If 0, restart it and return "success"

    # otherwise return "fail" and restart the program

    return 'Hello World!'


def start_program(program_name):
    if program_name == "index":
        os.system("cd ~/index; ./index chunks 5000 2> errs 1> logs")
    elif program_name == "TestSingleCrawler":
        os.system("cd ~/crawler; THIS_CRAWLER_PORT=8000 ./TestSingleCrawler 2> err1 1> /dev/null")


if __name__ == '__main__':
    app.run()
