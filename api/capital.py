import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CapitalId:
    def get_dp_id(self, dp_id):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': 'null',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Origin': 'https://meroshare.cdsc.com.np',
            'Pragma': 'no-cache',
            'Referer': 'https://meroshare.cdsc.com.np/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        session = requests.Session()
        retry = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        session.verify = False  # Insecure: disable SSL verification

        try:
            response = session.get('https://webbackend.cdsc.com.np/api/meroShare/capital/', headers=headers, timeout=10)
            response.raise_for_status()
            dp_id = str(dp_id)
            for item in response.json():
                if item['code'] == dp_id:
                    return item['id']
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        
        return 0