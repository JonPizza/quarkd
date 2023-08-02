from payloads.payloads import PAYLOADS

for p in PAYLOADS:
    print(f'{p["name"]} - {len(p["payloads"])} exploits loaded')