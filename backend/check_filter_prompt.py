"""Çalışan sunucuya karşı yapay zeka filtresini elle denemek için betik.

Kullanım: sunucu çalışırken proje kökünden `python backend/check_filter_prompt.py`
"""
import json
import urllib.request

BASE = 'http://127.0.0.1:8000'

SAMPLE_PROMPTS = [
    'Haftasonu dağlık bir araziye keşife çıkıcam, ona göre uygun bir kiralık araç lazım.',
    'Ailemle su kenarına piknik yapmaya gidicem, bize uygun bir araç lazım.',
]


def main():
    for prompt in SAMPLE_PROMPTS:
        req = urllib.request.Request(
            f'{BASE}/filter/prompt',
            data=json.dumps({'prompt': prompt}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as r:
            result = json.load(r)
            print('PROMPT:', prompt)
            print('FILTER:', result['parsed_filter'])
            print('MATCHED COUNT:', len(result['matched_cars']))
            print('FIRST:', result['matched_cars'][0] if result['matched_cars'] else None)
            print('---')


if __name__ == '__main__':
    main()
