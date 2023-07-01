from downloader import subscriptions, get_profile
import schedule
import time


def do_check():
    print("in")
    for url in subscriptions:
        test = get_profile(url)
        print(test)


schedule.every(1).minutes.do(do_check)

do_check()

while True:
    schedule.run_pending()
    time.sleep(1)
