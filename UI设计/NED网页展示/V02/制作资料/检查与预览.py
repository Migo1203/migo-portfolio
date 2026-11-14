from pathlib import Path
import json, threading, functools, shutil, tempfile, argparse, base64
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url='http://127.0.0.1:'+str(server.server_port)+'/index.html'
report={'日期':'2026-11-15','引擎':'Chromium / Playwright，桌面浏览器及触控模拟；未用实体手机','布局':[],'交互':{},'错误':[]}
def loaded(p):
    p.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
    p.evaluate("Promise.all([...document.images].filter(i=>i.id!=='viewer-image').map(i=>i.decode().catch(()=>{})))")
    p.evaluate("document.fonts.ready")
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context=browser.new_context(reduced_motion='reduce')
    page=context.new_page()
    page.on('pageerror',lambda e:report['错误'].append(str(e)))
    page.on('console',lambda m:report['错误'].append(m.text) if m.type=='error' else None)
    for width,height in [(1440,900),(2048,1180),(1024,768),(820,1180),(768,1024),(390,844),(320,720)]:
        for lang in ['zh','en']:
            page.set_viewport_size({'width':width,'height':height})
            page.goto(url+'?lang='+lang,wait_until='networkidle');loaded(page)
            metrics=page.evaluate("""()=>({
              viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth,
              broken:[...document.images].filter(i=>i.id!=='viewer-image'&&(!i.complete||!i.naturalWidth)).map(i=>i.alt),
              fonts:[document.fonts.check('16px "NED Latin"'),document.fonts.check('16px "NED Chinese"')],
              overflow:[...document.querySelectorAll('main h1,main h2,main h3,main p,main button,header a:not(.skip-link),header button')].filter(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return s.display!=='none'&&r.width&& (r.right>innerWidth+1||r.left< -1||e.scrollWidth>e.clientWidth+2)}).map(e=>e.textContent.slice(0,70)),
              hero:document.querySelector('.hero').getBoundingClientRect().height,
              selectedImages:[...document.querySelectorAll('main img')].map(i=>({source:decodeURI(new URL(i.currentSrc||i.src).pathname),naturalWidth:i.naturalWidth,shownWidth:Math.round(i.getBoundingClientRect().width)})),
              verticalSpill:[...document.querySelectorAll('main>section:not(.hero)')].filter(s=>s.querySelector('.wrap').getBoundingClientRect().bottom>s.getBoundingClientRect().bottom+1).map(s=>s.id),
              sections:[...document.querySelectorAll('main>section,footer')].map(e=>({id:e.id,height:Math.round(e.getBoundingClientRect().height),background:getComputedStyle(e).backgroundColor}))
            })""")
            report['布局'].append({'宽度':width,'语言':lang,**metrics})
    (ROOT/'检查记录.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    page.set_viewport_size({'width':1440,'height':900});page.goto(url,wait_until='networkidle');loaded(page)
    page.locator('[data-light-scene=night]').click();assert '夜间场景' in unquote(page.locator('#scene-image').get_attribute('src'))
    page.wait_for_function("document.querySelector('#scene-image').complete && decodeURI(document.querySelector('#scene-image').currentSrc).includes('夜间场景')")
    report['交互']['场景切换']=True
    for b in page.locator('.swatch').all():
        b.click();assert page.locator('#color-number').inner_text()==b.get_attribute('data-hex')
    report['交互']['五色用途切换']=True
    page.locator('#copy-color').click()
    page.wait_for_function("document.querySelector('#copy-status').textContent.length > 0")
    report['交互']['复制或可选文字回退']=True
    for i in range(8):
        link=page.locator('.gallery-link').nth(i);link.click()
        assert page.locator('#lightbox').evaluate('(d)=>d.open')
        assert page.locator('#viewer-count').inner_text()==str(i+1)+' / 8'
        page.keyboard.press('ArrowRight')
        assert page.locator('#viewer-count').inner_text()==str((i+1)%8+1)+' / 8'
        page.keyboard.press('Escape')
        assert link.evaluate('(e)=>e===document.activeElement')
    report['交互']['八张原图及前后切换Esc焦点返回']=True
    page.locator('.gallery-link').first.click()
    page.locator('#next').focus();page.keyboard.press('Tab')
    assert page.locator('#close-viewer').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Escape');report['交互']['对话框焦点约束']=True
    page.locator('#language').click();assert page.locator('html').get_attribute('lang')=='en'
    report['交互']['双语切换']=True
    # 静态正文与普通原图链接不依赖JS。
    nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
    n=nojs.new_page();n.goto(url);assert n.locator('#background').is_visible() and n.locator('.gallery-link').count()==8
    report['交互']['无JS静态阅读与原图链接']=True;nojs.close()
    # 孤立文件：复制HTML到临时空目录，测试无仓库依赖及动态寻址。
    with tempfile.TemporaryDirectory(prefix='ned-v02-') as temp:
        isolated=Path(temp)/'展示样稿.html';shutil.copyfile(ROOT/'展示样稿.html',isolated)
        offline=browser.new_context(reduced_motion='reduce',viewport={'width':390,'height':844})
        op=offline.new_page();errs=[];op.on('pageerror',lambda e:errs.append(str(e)))
        isolated_server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=temp))
        threading.Thread(target=isolated_server.serve_forever,daemon=True).start()
        report['本地文件协议']='曾实际尝试file://，环境浏览器策略返回ERR_BLOCKED_BY_ADMINISTRATOR；改用空目录HTTP验证便携性，不冒称双击已验证。'
        op.goto('http://127.0.0.1:'+str(isolated_server.server_port)+'/展示样稿.html',wait_until='networkidle');loaded(op)
        assert op.locator('img:not(#viewer-image)').evaluate_all('(es)=>es.every(i=>i.complete&&i.naturalWidth)')
        op.locator('[data-light-scene=night]').click();assert op.locator('#scene-image').get_attribute('src').startswith('data:')
        op.locator('.gallery-link').first.click();assert op.locator('#viewer-image').get_attribute('src').startswith('data:')
        op.keyboard.press('Escape');assert not errs,errs
        report['交互']['孤立HTML图片字体动效模块与切图']=True
        report['便携模块']=op.evaluate("({ready:document.documentElement.dataset.momentsReady,failed:document.querySelector('[data-moment]').dataset.momentFailed||null})")
        offline.close();isolated_server.shutdown()
    # 用户确认需要真实可操作样稿；截图为实际浏览器渲染，不是示意图。
    for width,height,name in [(1440,900,'桌面'),(390,844,'手机')]:
        page.set_viewport_size({'width':width,'height':height});page.goto(url,wait_until='networkidle');loaded(page)
        page.screenshot(path=str(ROOT/'预览图'/('完整页面_'+name+'.png')),full_page=True)
        page.screenshot(path=str(ROOT/'.impeccable/review'/('desktop.png' if width==1440 else 'mobile.png')))
        if width==1440:
            for id,label in [('background','项目背景'),('strategy','设计策略'),('palette','项目参考色')]:
                page.evaluate('window.scrollTo(0,0)')
                box=page.locator('#'+id).bounding_box()
                cdp=page.context.new_cdp_session(page)
                result=cdp.send('Page.captureScreenshot',{'format':'png','captureBeyondViewport':True,'fromSurface':True,'clip':{**box,'scale':1}})
                (ROOT/'预览图'/(label+'_桌面.png')).write_bytes(base64.b64decode(result['data']))
                cdp.detach()
    touch=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,reduced_motion='reduce')
    tp=touch.new_page();tp.goto(url,wait_until='networkidle');loaded(tp)
    tp.locator('[data-light-scene=night]').tap();assert tp.locator('[data-light-scene=night]').get_attribute('aria-pressed')=='true'
    tp.locator('.swatch').first.tap();assert tp.locator('#color-number').inner_text()=='#F4F1EB'
    tp.locator('.gallery-link').first.tap();assert tp.locator('#lightbox').evaluate('(d)=>d.open')
    tp.locator('#close-viewer').tap();report['交互']['模拟触控切场景色谱及原图']=True;touch.close()
    browser.close()
server.shutdown()
bad=[r for r in report['布局'] if r['scrollWidth']>r['viewport'] or r['broken'] or r['overflow'] or r['verticalSpill'] or not all(r['fonts'])]
report['布局通过']=not bad
(ROOT/'检查记录.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'布局数':len(report['布局']),'问题':bad,'错误':report['错误'],'交互':report['交互'],'便携模块':report['便携模块']},ensure_ascii=False))
assert not bad and not report['错误']
