from script.access_web import *
from concurrent.futures import ThreadPoolExecutor  # 線程池
from apscheduler.schedulers.blocking import BlockingScheduler
from prometheus_client import Gauge,start_http_server
import datetime


scheduler = BlockingScheduler()
timeout = os.getenv('RENDER_TIMEOUT_SECONDS', 30)
interval = os.getenv('REPEAT_INTERVAL_MINUTES', 1)
test_domain = os.getenv('TEST_DOMAIN_LIST', "aaa.com,bbb.com,ccc.com")
http_port = os.getenv('PROMETHEUS_CLIENT_PORT', 5000)

gauge = Gauge(  'Portal_response_time', 
                'calculate portal response & render time',
                ['Portal_URL']) # -1 = timeout  0 = during maintaince

def run():
    testlist= test_domain.split(',')
    gauge.clear()
    # print(f"{datetime.datetime.now().strftime('%m/%d %H:%M:%S')}開始測試")
    for url in testlist :
        res = askwebPC(url,timeout)        
        gauge.labels('PC :'+url).set(res)
    
    for url in testlist :
        res = askwebWAP(url,timeout)
        gauge.labels('WAP :'+url).set(res)

    # pool = ThreadPoolExecutor(max_workers=20)  # 可調整線程執行數量
    # task1 = [pool.submit(askwebPC, url, dic_PC,30) for url in urls]
    # task2 = [pool.submit(askwebWAP, url, dic_WAP,30) for url in urls]
    # pool.shutdown()
    # print(f"{datetime.datetime.now().strftime('%m/%d %H:%M:%S')}測試結束")

if __name__ == "__main__":
    start_http_server(http_port)
    scheduler.add_job(run,'cron',minute='*/'+str(interval))
    scheduler.start()  # 定時執行


    
