import os

from flask import Flask, request

app = Flask(__name__)


@app.route('/status')
def status():
    program = request.args.get('program')



    return 'Hello World!'


def start_program(program_name):
    if program_name == "index":
        os.system("cd ~/index; ./index chunks 5000 2> errs 1> logs")
    elif program_name == "TestSingleCrawler":
        os.system("cd ~/crawler; THIS_CRAWLER_PORT=8000 ./TestSingleCrawler 2> err1 1> /dev/null")


if __name__ == '__main__':
    app.run()
