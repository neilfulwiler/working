
import time
import datetime

total_work_time = 0.
total_not_work_time = 0.

def print_stats():
    print 'working: %s (%.2f%%)' % (datetime.timedelta(seconds=total_work_time), 100. * total_work_time / (total_work_time + total_not_work_time) )
    print 'not working: %s (%.2f%%) ' % (datetime.timedelta(seconds=total_not_work_time), 100. * total_not_work_time / (total_work_time + total_not_work_time))

class DoneException(Exception):
    pass

def check_terminating(user_input):
    if user_input in ['q', 'quit', 'done', 'exit']:
        raise DoneException()

try:
    while True:
        start_not_work = time.time()
        user_input = raw_input('>>> not working [hit enter to start] ')
        stop_not_work = time.time()

        total_not_work_time += stop_not_work - start_not_work

        check_terminating(user_input)

        print_stats()

        start_work = time.time()
        user_input = raw_input('<<< working [hit enter to stop] ')
        stop_work = time.time()

        total_work_time += stop_work - start_work

        check_terminating(user_input)

        print_stats()
except DoneException:
    pass

print
print '*' * 50
print '*' * 50
print '*' * 50
print
print 'Final'
print
print_stats()

