#Replaces instead of removes duplicate rowsimport website.wsgi
import website.wsgi
from data.models import Treatment
from datetime import timedelta
import csv

def main():
    output = []
    for t in Treatment.objects.all():
        timers = t.user.worktimer_set.order_by('-timestamp')
        addlist = []
        if len(timers) > 1:
            for x in range(len(timers)-1):
                v = timers[x].value
                if timers[x].timestamp - timedelta(seconds=v) < timers[x+1].timestamp:
                    #Remove the current value and replace it with the difference
                    #between the current and the next timestamp in seconds
                    diff = timers[x].timestamp - timers[x+1].timestamp
                    info = {
                        'user': timers[x].user,
                        'user_id': timers[x].user_id,
                        'task_id': timers[x].task_id,
                        'timestamp': timers[x].timestamp,
                        'value': diff.seconds,
                        'page': timers[x].page,
                        'token': timers[x].token,
                        'id': timers[x].id,
                    }
                    output.append(info)
                else:
                    # add it to the list.
                    info = {
                        'user': timers[x].user,
                        'user_id': timers[x].user_id,
                        'task_id': timers[x].task_id,
                        'timestamp': timers[x].timestamp,
                        'value': int(timers[x].value),
                        'page': timers[x].page,
                        'token': timers[x].token,
                        'id': timers[x].id,
                    }
                    output.append(info)
        #Add the last value
        if len(timers) > 0:
            timer = timers.last()
            try:
                addValue = addlist.pop()
            except IndexError:
                addValue = 0
            info = {
                'user': timer.user,
                'user_id': timer.user_id,
                'task_id': timer.task_id,
                'timestamp': timer.timestamp,
                'value': int(timer.value) + addValue,
                'page': timer.page,
                'token': timer.token,
                'id': timer.id,
            }
            output.append(info)

    return output

def write_out(output):
    with open('worktimer_fix2.csv', 'w') as f:
        writer = csv.writer(f, csv.excel)
        headers = ['user', 'user_id', 'task_id', 'timestamp', 'value', 'page', 'token', 'id']
        writer.writerow(headers)
        for o in output:
            row = [o[h] for h in headers]
            writer.writerow(row)

if __name__=="__main__":
    write_out(main())
