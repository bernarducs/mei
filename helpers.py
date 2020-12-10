import time


def print_timestamp(now=True):
    timestamp = time.localtime(time.time())
    if now:
        print_time = '{}/{}/{} {}:{}:{}'.format(timestamp.tm_mday, timestamp.tm_mon, timestamp.tm_year,
                                           timestamp.tm_hour, timestamp.tm_min, timestamp.tm_sec)
        return print_time
    print_time = '{:04d}{:02d}{:02d}'.format(timestamp.tm_year, timestamp.tm_mon, timestamp.tm_mday)
    return print_time


def retorna_ufs():
    with open('lista de uf.txt', 'r', encoding='latin-1') as f:
        file = f.readlines()
    ufs = [uf[:-1] for uf in file]
    return ufs
