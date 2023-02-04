import requests
import time
import yaml

class SMMS(object):
    def __init__(self):
        with open(r"config.yaml") as f:
            config = yaml.safe_load(f)
        self.headers = {'Authorization': config['smms']['token']}

    def isDiskFull(self):
        url = 'https://sm.ms/api/v2/profile'
        res = requests.post(url, headers=self.headers, timeout=5).json()
        if res["disk_usage_raw"] > 0.9 * res["disk_limit_raw"]:
            return True

    def upload(self, filepath):
        files = {'smfile': open(filepath, 'rb')}
        url = 'https://sm.ms/api/v2/upload'
        res = requests.post(url, files=files, headers=self.headers, timeout=5).json()
        # print(json.dumps(res, indent=4))
        return res['data']['url']

    def getHistory(self):
        url = 'https://sm.ms/api/v2/upload_history'
        res = requests.get(url, headers=self.headers, timeout=5).json()
        return res

    def deleteHistory(self):
        history = self.getHistory()
        lastTime = time.time()
        for item in history["data"]:
            if item["created_at"] < lastTime:
                url = 'https://sm.ms/api/v2/delete/{}'.format(item["hash"])
                res = requests.get(url, headers=self.headers, timeout=5).json()
        print("History deleted!")
