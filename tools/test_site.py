import subprocess, time, os, sys
from selenium import webdriver
from selenium.webdriver.common.by import By

OUT = '/home/claude/lp/shots'
os.makedirs(OUT, exist_ok=True)
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'], cwd='/home/claude/lp/site', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
xvfb = subprocess.Popen(['Xvfb', ':99', '-screen', '0', '1400x1000x24'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
os.environ['DISPLAY'] = ':99'
time.sleep(2)
opts = webdriver.WebKitGTKOptions()
opts.binary_location = '/usr/bin/MiniBrowser' if os.path.exists('/usr/bin/MiniBrowser') else opts.binary_location
d = webdriver.WebKitGTK(options=opts)
report = []
def shot(name):
    d.save_screenshot(f'{OUT}/{name}.png')
def metrics(tag):
    m = d.execute_script("return [document.documentElement.scrollWidth, window.innerWidth, document.documentElement.scrollHeight, [...document.images].filter(i=>i.complete&&i.naturalWidth===0).length]")
    report.append(f'{tag}: scrollW={m[0]} innerW={m[1]} H={m[2]} brokenImgs={m[3]}')
try:
    for W, H, tag in [(390, 844, 'phone'), (1280, 900, 'desk')]:
        d.set_window_rect(0, 0, W, H)
        d.get('http://localhost:8765/index.html')
        time.sleep(3)
        metrics(tag + '-home')
        shot(f'{tag}_1_top')
        d.execute_script("document.getElementById('stays').scrollIntoView()"); time.sleep(1.2); shot(f'{tag}_2_stays')
        d.execute_script("window.scrollTo(0, document.getElementById('how').offsetTop-60)"); time.sleep(1); shot(f'{tag}_3_how')
        d.execute_script("document.getElementById('owners').scrollIntoView()"); time.sleep(1); shot(f'{tag}_4_owners')
        # filter tap
        d.execute_script("window.scrollTo(0,0)")
        d.find_element(By.CSS_SELECTOR, '#chips [data-f="villa"]').click(); time.sleep(.5)
        report.append(tag + ' villa filter count: ' + d.find_element(By.ID, 'count').text)
        d.find_element(By.CSS_SELECTOR, '#chips [data-f="all"]').click()
        # unit page
        d.get('http://localhost:8765/index.html#u-877272'); time.sleep(2.5)
        metrics(tag + '-unit')
        shot(f'{tag}_5_unit')
        d.execute_script("document.getElementById('r-in').value='2026-12-10';document.getElementById('r-out').value='2026-12-14'")
        d.find_element(By.ID, 'r-n').send_keys('Test Guest')
        d.execute_script("document.getElementById('req').requestSubmit()"); time.sleep(.8)
        out = d.find_element(By.ID, 'r-out').text
        report.append(tag + ' request out: ' + out.replace('\n', ' | ')[:200])
        d.execute_script("document.getElementById('req').scrollIntoView()"); time.sleep(.6); shot(f'{tag}_6_request')
        d.find_element(By.ID, 'back').click(); time.sleep(1.2)
        report.append(tag + ' after back hash=' + d.execute_script('return location.hash') + ' unitOpen=' + str(d.execute_script("return document.body.classList.contains('unit-open')")))
        shot(f'{tag}_7_back')
finally:
    d.quit(); srv.kill(); xvfb.kill()
print('\n'.join(report))
