from pathlib import Path
import json, base64, html, re, hashlib
from urllib.parse import quote
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
esc=lambda s:html.escape(s,quote=True)
def data(p):
    mime={'.woff':'font/woff','.webp':'image/webp','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml'}[p.suffix]
    return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
BASE='https://github.com/Migo1203/AIGC/blob/4929b4063e74fd11642b6ff83c32f9f1f31deba1/'
SRC='作品项目/NED_Eric_Lamp_氛围灯/'
source=lambda p:BASE+quote(SRC+p,safe='/')
page=(ROOT/'制作资料/页面模板.html').read_text()
sources={
 'APLUS':source('制作交付/作品集展示/成果展示/V04/02_高级A+/README.md'),
 'STORY':source('制作交付/作品集展示/成果展示/V04/03_品牌故事/README.md'),
 'BANNER':source('制作交付/作品集展示/成果展示/V04/04_Banner系统/README.md'),
 'BRIEF':source('项目规划/统一主视觉与设计方向-v0.2.md'),
 'ASSETS':source('制作交付/作品集展示/成果展示/V04/README.md')
}
for key,value in sources.items(): page=page.replace('{{SOURCE_'+key+'}}',value)
items=[
 ('00_主图_近白底_V01.webp','产品主图','Main image','先建立完整外观识别','Establish the product shape'),
 ('01_产品展示_V02.webp','产品展示','Product view','把产品放回生活空间','Place the product within a room'),
 ('02_旋钮操作_V02.webp','旋钮操作','Knob controls','近景解释具体动作','Explain the control action'),
 ('03_光色调节_V01.webp','光色调节','Light adjustment','把操作与光感联系起来','Connect the action with light'),
 ('04_夜间无线续航_V02.webp','夜间使用','Night-time use','呈现夜间的使用情境','Show a night-time setting'),
 ('05_尺寸材质_V02.webp','尺寸与材质','Scale and finish','回答尺度与表面的问题','Explain scale and surface'),
 ('06_户外使用_V02.webp','户外情境','Outdoor setting','保留环境与使用条件','Keep the setting understandable'),
 ('07_多场景使用_V02.webp','多场景使用','Different settings','同一产品延续不同空间','One product in different spaces'),
]
gallery=[]
for file,title,en,desc,desc_en in items:
    path='assets/图片/'+file
    thumb='assets/缩略图/'+file
    alt=title+'：NED Eric原商品图，完整构图与原英文保留。'
    gallery.append('<article class="gallery-item"><a class="gallery-link m-zoom" href="'+esc(path)+'" data-title="'+title+'" data-title-en="'+en+'" aria-label="放大查看'+title+'"><img src="'+esc(thumb)+'" alt="'+alt+'" width="640" height="640" loading="lazy" data-source="AIGC/NED/商品图/'+file+'" data-subject="'+title+'"></a><h3 data-en="'+en+'">'+title+'</h3><p data-en="'+desc_en+'">'+desc+'</p></article>')
page=page.replace('{{GALLERY}}','\n'.join(gallery))
colors=[
 ('bone','骨白','Bone','#F4F1EB','产品浅色与少量明亮区域，留住灯具的轻盈感。','Light product surfaces and a few bright areas keep the lamp visually light.'),
 ('sand','沙灰','Sand','#D8CABC','主要阅读底色，联系暖墙与织物，连接图片和网页。','The main reading ground connects warm walls, fabrics and the web page.'),
 ('walnut','深胡桃','Walnut','#5A463B','联系木质家具，承担背景介绍与色谱的深色阅读区域。','A connection to wooden furniture, used for deeper context and palette regions.'),
 ('charcoal','炭灰','Charcoal','#2F302E','支撑文字与夜间层次，形成稳定的视觉结构。','Reading text and darker night regions provide structure and contrast.'),
 ('terracotta','陶土','Terracotta','#9B6B56','作为局部暖色，与材质和光感呼应，不代表实测灯光颜色。','A local warm field relating to material and light, not a measured light color.')
]
swatches=[]
for cls,title,en,hexv,role,role_en in colors:
    rgb=' / '.join(str(int(hexv[i:i+2],16)) for i in (1,3,5))
    swatches.append('<button type="button" class="swatch '+cls+'" data-color="'+title+'" data-name-en="'+en+'" data-hex="'+hexv+'" data-role="'+esc(role)+'" data-role-en="'+esc(role_en)+'" aria-pressed="'+str(cls=='sand').lower()+'"><span class="swatch-name" data-en="'+en+'">'+title+'</span><span class="color-values"><b>'+hexv+'</b><span>RGB '+rgb+'</span></span></button>')
page=page.replace('{{SWATCHES}}','\n'.join(swatches))
for file in (ROOT/'assets/图片').glob('*.webp'):
    w,h=Image.open(file).size
    pattern=r'(<img\b[^>]*src="'+re.escape('assets/图片/'+file.name)+r'"[^>]*width=")\d+("[^>]*height=")\d+(")'
    page=re.sub(pattern,lambda m:m[1]+str(w)+m[2]+str(h)+m[3],page)
assert not re.search(r'\{\{[A-Z_]+\}\}',page)
# 源码入口真实选择较小资源；保留清晰原图作为放大入口。
responsive_map={}
gallery_sizes='(max-width:639px) calc((100vw - 60px)/2), (max-width:1023px) calc((100vw - 104px)/2), (max-width:1200px) calc((100vw - 168px)/4), (max-width:1440px) calc((100vw - 232px)/4), 302px'
def responsive_img(match):
    tag=match[0]
    sm=re.search(r'src="([^"]+)"',tag)
    if not sm or 'viewer-image' in tag:return tag
    path=sm[1];p=ROOT/path;name=p.name
    candidates=[]
    if path.startswith('assets/缩略图/'):
        candidates=[ROOT/'assets/响应式/缩略320'/name,p];sizes=gallery_sizes
    elif path.startswith('assets/图片/') and (ROOT/'assets/响应式/400'/name).exists():
        candidates=[ROOT/'assets/响应式/400'/name,ROOT/'assets/响应式/800'/name,p]
        sizes='(max-width:639px) calc(100vw - 48px), (max-width:1023px) calc(100vw - 80px), 50vw'
        if 'hero__bg' in tag:sizes='(max-width:639px) 600px, 100vw'
        elif name=='A加手机.webp':sizes='(max-width:639px) 300px, 27vw'
        elif name=='策略_餐桌暮色.webp':
            w,h=Image.open(p).size;ratio=w/h
            sizes='(max-width:639px) calc((100vw - 48px) * '+str(round(ratio/1.25,5))+'), (max-width:1023px) calc((100vw - 80px) * '+str(round(ratio/(16/9),5))+'), calc(56vw * '+str(round(ratio/1.5,5))+')'
        elif name in ['夜间场景.webp','Banner场景.webp']:
            w,h=Image.open(p).size;ratio=w/h
            mobile=str(round(ratio/1.5,5));other=str(round(ratio/1.9,5))
            sizes='(max-width:639px) calc((100vw - 48px) * '+mobile+'), (max-width:1023px) calc((100vw - 112px)/2 * '+other+'), (max-width:1200px) calc((100vw - 144px)/2 * '+other+'), (max-width:1440px) calc((100vw - 208px)/2 * '+other+'), calc(616px * '+other+')'
    if not candidates:return tag
    widths={}
    for c in candidates:widths[Image.open(c).size[0]]=str(c.relative_to(ROOT))
    srcset=', '.join(esc(v)+' '+str(w)+'w' for w,v in sorted(widths.items()))
    if name in ['策略_餐桌暮色.webp','夜间场景.webp']:
        w,h=Image.open(p).size;ratio=w/h
        scene_sizes='(max-width:639px) calc((100vw - 48px) * '+str(round(ratio/1.25,5))+'), (max-width:1023px) calc((100vw - 80px) * '+str(round(ratio/(16/9),5))+'), calc(56vw * '+str(round(ratio/1.5,5))+')'
        responsive_map[path]={'srcset':srcset,'sizes':scene_sizes}
    return tag[:-1]+' srcset="'+srcset+'" sizes="'+sizes+'">'
page=re.sub(r'<img\b[^>]*>',responsive_img,page)
page=page.replace('<script src="制作资料/页面交互.js"></script>','<script id="ned-responsive">window.NED_RESPONSIVE_MAP='+json.dumps(responsive_map,ensure_ascii=False)+';</script><script src="制作资料/页面交互.js"></script>')
(ROOT/'index.html').write_text(page)
image_files=list((ROOT/'assets/图片').glob('*.webp'))+list((ROOT/'assets/缩略图').glob('*.webp'))
image_map={str(p.relative_to(ROOT)):data(p) for p in image_files}
portable=re.sub(r'\s+(srcset|sizes)="[^"]*"','',page)
portable=re.sub(r'<script id="ned-responsive">[\s\S]*?</script>','',portable)
image_map={p:u for p,u in image_map.items() if p in portable or p in ['assets/图片/策略_餐桌暮色.webp','assets/图片/夜间场景.webp']}
for path,url in image_map.items():
    portable=portable.replace('src="'+path+'"','src="'+url+'"').replace('href="'+path+'"','href="'+url+'"').replace('content="'+path+'"','content="'+url+'"')
def style(m):
    p=ROOT/m[1]
    css=p.read_text()
    def replace_url(u):
        relative=u[1].strip('\'"')
        if relative.startswith(('data:','http:','https:','#')): return u[0]
        target=(p.parent/relative).resolve()
        return 'url("'+data(target)+'")' if target.is_file() else u[0]
    css=re.sub(r'url\(([^)]+)\)',replace_url,css)
    return '<style>\n'+css+'\n</style>'
portable=re.sub(r'<link rel="stylesheet" href="([^"]+)">',style,portable)
motion=(ROOT/'assets/motion/motion.js').read_text().replace('</script',r'<\/script')
lib=data(ROOT/'assets/moments/lib.js')
moment=data(ROOT/'assets/moments/picture-develops/moment.js')
moment_css=data(ROOT/'assets/moments/picture-develops/moment.css')
loader=(ROOT/'assets/moments/moments.js').read_text()
loader=loader.replace("import * as lib from './lib.js';","import * as lib from '"+lib+"';")
loader=loader.replace("const BASE = new URL('./', import.meta.url);","const BASE = new URL('https://ned-v02.invalid/assets/moments/');")
# 只重写资源寻址，不修改动效与判断逻辑；原模块原样保留。
tick=chr(96); interpolation=chr(36)+'{id}'
loader=loader.replace('css(new URL('+tick+interpolation+'/moment.css'+tick+', BASE).href)','css('+json.dumps({'picture-develops':moment_css})+'[id])')
loader=loader.replace('import(new URL('+tick+interpolation+'/moment.js'+tick+', BASE).href)','import('+json.dumps({'picture-develops':moment})+'[id])')
loader=loader.replace('</script',r'<\/script')
portable=portable.replace('<script type="module" src="assets/motion/motion.js"></script>','<script type="module">\n'+motion+'\n</script>')
portable=portable.replace('<script type="module" src="assets/moments/moments.js"></script>','<script type="module">\n'+loader+'\n</script>')
ui=(ROOT/'制作资料/页面交互.js').read_text()
scene_map={key:image_map[key] for key in ['assets/图片/策略_餐桌暮色.webp','assets/图片/夜间场景.webp']}
portable=portable.replace('<script src="制作资料/页面交互.js"></script>','<script>window.NED_ASSET_MAP='+json.dumps(scene_map,ensure_ascii=False)+';</script><script>\n'+ui+'\n</script>')
licenses={p.name:p.read_text() for p in [ROOT/'assets/taste-skill许可证.txt',*list((ROOT/'assets/字体').glob('*OFL.txt'))]}
portable=portable.replace('</body>','<script type="application/json" id="third-party-licenses">'+json.dumps(licenses,ensure_ascii=False).replace('</','<\\/')+'</script>\n</body>')
(ROOT/'展示样稿.html').write_text(portable)
(ROOT/'构建记录.json').write_text(json.dumps({'日期':'2026-11-15','源码入口':'index.html','便携入口':'展示样稿.html','便携字节数':len(portable.encode()),'内嵌图片数':len(image_map),'便携SHA256':hashlib.sha256(portable.encode()).hexdigest(),'模块打包':'官方CSS与motion模块原样内嵌；moments loader仅将资源地址重写为data URL，功能逻辑不改。源码入口加载原样模块。'},ensure_ascii=False,indent=2))
print('已生成源码入口与便携HTML；图片',len(image_map),'；便携字节',len(portable.encode()))
