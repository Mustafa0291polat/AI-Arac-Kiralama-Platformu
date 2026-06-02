import urllib.request
import urllib.error

base = 'http://127.0.0.1:8000'

try:
    with urllib.request.urlopen(f'{base}/cars/') as response:
        print('OK', response.status)
        body = response.read().decode('utf-8')
        print(body[:200])
except urllib.error.HTTPError as e:
    print('HTTP', e.code)
    print(e.read().decode('utf-8'))
except Exception as e:
    print('ERROR', e)
