import re, json, os, subprocess, html as H
IDS = ["1724834880042877272","1721078214730516096","1791968941526110648","1794882459377791266","1763780573260738710","1731349165770781852","1791971488151196028","1766726224539846454","1724882387343265096","1791974258145963584","1791982398535076239","1791987201540201923","1791989617297554967"]
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15'
base = os.path.expanduser('~/Projects/laporta-site')
os.makedirs(base + '/raw', exist_ok=True); os.makedirs(base + '/img', exist_ok=True)
out = []
for lid in IDS:
    p = f'{base}/raw/{lid}.html'
    if not os.path.exists(p) or os.path.getsize(p) < 100000:
        subprocess.run(['curl', '-sL', '-A', UA, '-H', 'Accept-Language: en-US', '-o', p, f'https://www.airbnb.com/rooms/{lid}'])
    h = open(p, encoding='utf-8', errors='ignore').read().replace('\\u002F', '/').replace('\\/', '/')
    t = re.search(r'<title>([^<]*)</title>', h)
    title = H.unescape(t.group(1).split(' - ')[0]) if t else ''
    og = re.search(r'property="og:title" content="([^"]*)"', h)
    ogt = H.unescape(og.group(1)) if og else ''
    g = re.search(r'(\d+) guests?', h)
    imgs = []
    for u in re.findall(r'https://a0\.muscache\.com/im/pictures/(?:hosting/)?Hosting-' + lid + r'/original/[0-9a-f-]+\.(?:jpe?g|png|webp)', h, re.I):
        if u not in imgs: imgs.append(u)
    if not imgs:
        for u in re.findall(r'https://a0\.muscache\.com/im/pictures/(?:miso/)?(?:hosting/)?[^"?\\ \']*?' + lid + r'[^"?\\ \']*?\.(?:jpe?g|png|webp)', h, re.I):
            if u not in imgs: imgs.append(u)
    files = []
    for i, u in enumerate(imgs[:6]):
        f = f'img/{lid[-6:]}_{i}.jpg'
        fp = f'{base}/{f}'
        if not os.path.exists(fp) or os.path.getsize(fp) < 5000:
            subprocess.run(['curl', '-sL', '-A', UA, '-o', fp, u + '?im_w=1200&im_format=jpeg'])
        if os.path.exists(fp) and os.path.getsize(fp) > 5000:
            files.append(f)
    out.append({'id': lid, 'title': title, 'og': ogt, 'guests': int(g.group(1)) if g else None, 'n_imgs': len(imgs), 'files': files})
    print(lid, '|', title, '|', ogt, '|', g.group(1) if g else None, '|', len(imgs), len(files), flush=True)
json.dump(out, open(f'{base}/units.json', 'w'), ensure_ascii=False, indent=1)
print('DONE')
