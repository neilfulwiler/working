
import time
import datetime
from collections import defaultdict
import rlcompleter
import readline
import logging

LOG_FILENAME = 'log.log'
logging.basicConfig(filename=LOG_FILENAME,
        level=logging.DEBUG)

total_work_time = 0.
total_not_work_time = 0.

work_things = defaultdict(int)
not_work_things = defaultdict(int)

class Completer:
    def complete(self, text, state):
        logging.info('completion called')
        if state == 0:
            self.matches = [s
                            for s in work_things.keys() + not_work_things.keys()
                            if s.startswith(text)]

        logging.info('matches: %s (text %s - state %s)' % (self.matches, text, state))

        try:
            return self.matches[state]
        except IndexError:
            return None

# add autocompletion
readline.set_completer(Completer().complete)
readline.parse_and_bind('tab: complete')

def print_stats():
    print 'working: %s (%.2f%%)' % (datetime.timedelta(seconds=total_work_time), 100. * total_work_time / (total_work_time + total_not_work_time) )
    print 'not working: %s (%.2f%%) ' % (datetime.timedelta(seconds=total_not_work_time), 100. * total_not_work_time / (total_work_time + total_not_work_time))

class DoneException(Exception):
    pass

TERMINATING = ['q', 'quit', 'done', 'exit']

def check_terminating(user_input):
    if user_input in TERMINATING:
        raise DoneException()

def worked_on(thing, t):
    work_things[thing] += t

def not_worked_on(thing, t):
    not_work_things[thing] += t

thing_im_not_working_on = 'starting'

try:
    while True:
        start_not_work = time.time()
        user_input = raw_input('>>> not working [hit enter to start] ')
        stop_not_work = time.time()
        elapsed = stop_not_work - start_not_work

        not_worked_on(thing_im_not_working_on, elapsed)

        total_not_work_time += elapsed

        check_terminating(user_input)

        print_stats()

        thing_im_working_on = user_input

        start_work = time.time()
        user_input = raw_input('<<< working [hit enter to stop] ')
        stop_work = time.time()
        elapsed = stop_work - start_work

        worked_on(thing_im_working_on, elapsed)

        total_work_time += elapsed

        check_terminating(user_input)

        print_stats()

        thing_im_not_working_on = user_input
except DoneException:
    pass

print
print '*' * 50
print '*' * 50
print '*' * 50
print
print 'Final'
print
for work_thing in work_things:
    print '[work]     %10s > %s' % (work_thing, datetime.timedelta(seconds=work_things[work_thing]))
print
for not_work_thing in not_work_things:
    print '[not work] %10s < %s' % (not_work_thing, datetime.timedelta(seconds=not_work_things[not_work_thing]))
print

print_stats()

