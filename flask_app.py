
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
from flask_apscheduler import APScheduler

import enum
import time
import typing as tp


class MachineStates(enum.Enum):
    DEFAULT = 0
    FALL = 0
    WORKING = 1


class Machine():
    def __init__(self, name: str, states: MachineStates = MachineStates):
        self.name = name
        self.states_set = states
        self.state = self.states_set.DEFAULT
        self.last_ping_ts = None

    def on_fall(self):
        return None

    def on_working(self):
        return None

    def to_fall(self):
        new_state = self.states_set.FALL
        if self.state != new_state:
            res = self.on_fall()
        res = self.on_fall()
        self.state = new_state

    def to_working(self):
        new_state = self.states_set.WORKING
        if self.state != new_state:
            res = self.on_working()
        self.state = new_state


machines: tp.Dict[str, Machine] = {}


app = Flask(__name__)
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


@scheduler.task('interval', id='Process_status', seconds=300, max_instances=1)
def process_machines_status():
    pass


@app.route('/')
def hello_world():
    return 'Hello from MROB laboratory!'

@app.route('/ping', methods=['GET'])
def ping():
    machine = request.args['machine']

    if machine not in machines:
        machines[machine] = Machine(machine)
    machines[machine].to_working()
    machines[machine].last_ping_ts = time.time()

    return machine
