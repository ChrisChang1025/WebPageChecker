## Technical Details

**This tool is designed to measure the performance of frontend homepage loading. By using webdriver.geturl as a starting point, the tool calculates the time taken for the specified homepage components to become visible.**

**Key features include:**
* Multi-domain support: Monitor multiple websites simultaneously.
* Timeout handling: Returns -1 if loading time exceeds a specified threshold.
* Maintenance detection: Returns 0 if the website is under maintenance.
* Sequential processing: Avoids concurrent multi-threading to optimize resource usage.

**Each domain is tested individually for both PC and Mobile versions.**


## Guide line

>docker 環境變數
>* **RENDER_TIMEOUT_SECONDS** : 單次的timeout (s) `預設為30秒`
>* **REPEAT_INTERVAL_MINUTES** : 每次掃完所有Domain PC/Wap 的間隔(m) `預設為4分鐘`
>* **TEST_DOMAIN_LIST** : 用逗號分隔的域名列表 `預設為"aaa.com,bbb.com,ccc.com"`
>* **PROMETHEUS_CLIENT_PORT** : 普羅米修斯的Client Port `預設值為5000`


>docker 執行指令
>```bash
>docker build -t portal_res_prometheus . #build image
>docker run -it -p 5000:5000 --name test portal_res_prometheus  >#run container
>```


