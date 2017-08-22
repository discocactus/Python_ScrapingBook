import time


def slow_job(n):
    """
    引数で指定した秒数だけ時間のかかる処理を行う関数。
    time.sleep()を使って擬似的に時間がかかるようにしている。
    """

    print('Job {0} will take {0} seconds'.format(n))
    time.sleep(n)  # n秒待つ。
    print('Job {0} finished'.format(n))


slow_job(1)
slow_job(2)
slow_job(3)
