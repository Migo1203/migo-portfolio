"""仅交付格式转换与字体子集；不修改AIGC源文件。"""
from pathlib import Path
import json, shutil, hashlib, subprocess, sys
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
SRC = Path('/workspace/AIGC/作品项目/NED_Eric_Lamp_氛围灯')
TOOL = Path('/workspace/design-resources/素材与工具/工具/交付与检索脚本/图片交付.py')
OLD = REPO / '素材/NED/网页展示_V01'
OUT = ROOT / 'assets/图片'
ADDED = {
 '材质特写.webp': SRC/'制作交付/作品集展示/V04/可编辑源稿/策略_灯罩细节.png',
 '夜间原图.webp': SRC/'制作交付/作品集展示/V04/可编辑源稿/策略_夜间暖光.png',
 '品牌生活.webp': SRC/'制作交付/作品集展示/成果展示/V04/03_品牌故事/03_原始素材/B02_审美与造型.jpg',
 '夜间场景.webp': SRC/'制作交付/作品集展示/成果展示/V04/02_高级A+/03_原始素材/P04B_PC.jpg',
 'A加操作.webp': SRC/'制作交付/作品集展示/成果展示/V04/02_高级A+/03_原始素材/P03C_PC.jpg',
 'A加手机.webp': SRC/'制作交付/作品集展示/成果展示/V04/02_高级A+/03_原始素材/P03C_Mobile.jpg',
 'Banner场景.webp': SRC/'制作交付/作品集展示/成果展示/V04/04_Banner系统/03_原始素材/排版底图/BN02_电脑无字_源SVG提取.png',
}
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
if not OUT.exists():
    tmp = ROOT/'assets/本轮转换'
    subprocess.run([sys.executable,str(TOOL),*[str(v) for v in ADDED.values()], '--输出',str(tmp),'--格式','webp','--长边','1600','--质量','90'],check=True,stdout=subprocess.DEVNULL)
    OUT.mkdir()
    manifest=json.loads((tmp/'交付清单.json').read_text())
    items=[]
    for p in OLD.glob('*.webp'):
        shutil.copy2(p,OUT/p.name)
        items.append({'名称':p.name,'来源':str(p.relative_to(REPO)),'SHA256':digest(p),'处理':'沿用V01的sRGB WebP派生文件；原始来源见V01交付清单'})
    for name,src in ADDED.items():
        converted=tmp/(src.stem+'.webp')
        shutil.copy2(converted,OUT/name)
        items.append({'名称':name,'来源':str(src.relative_to(SRC)),'源SHA256':digest(src),'SHA256':digest(OUT/name),'转换记录':next(i for i in manifest['文件'] if i['输入文件']==str(src))})
    (ROOT/'素材来源.json').write_text(json.dumps({'日期':'2026-11-15','源仓库提交':'4929b4063e74fd11642b6ff83c32f9f1f31deba1','说明':'已有AI辅助图像与合成成果；不称实景摄影。仅格式与尺寸转换，不新增生成图片。','文件':items},ensure_ascii=False,indent=2))
    shutil.rmtree(tmp)  # 删除本脚本创建的临时交付目录，已有源文件不动。

THUMBS=ROOT/'assets/缩略图'
if not THUMBS.exists():
    original=json.loads((OLD/'交付清单.json').read_text())
    inputs=[f['输入文件'] for f in original['文件'] if Path(f['输出文件']).name[:2] in ['00','01','02','03','04','05','06','07']]
    assert len(inputs)==8
    subprocess.run([sys.executable,str(TOOL),*inputs,'--输出',str(THUMBS),'--格式','webp','--长边','640','--质量','85'],check=True,stdout=subprocess.DEVNULL)

# 源码入口的响应式派生资源；便携HTML保留单一清晰版本，避免把所有变体塞进去。
responsive_names=['封面_原场景裁切.webp','策略_餐桌暮色.webp','品牌生活.webp','策略_产品透明抠图.webp','A加操作.webp','A加手机.webp','夜间场景.webp','Banner场景.webp']
for edge in [400,800]:
    dest=ROOT/'assets/响应式'/str(edge)
    if not dest.exists():
        subprocess.run([sys.executable,str(TOOL),*[str(OUT/name) for name in responsive_names],'--输出',str(dest),'--格式','webp','--长边',str(edge),'--质量','85'],check=True,stdout=subprocess.DEVNULL)
dest=ROOT/'assets/响应式/缩略320'
if not dest.exists():
    subprocess.run([sys.executable,str(TOOL),*[str(p) for p in THUMBS.glob('*.webp')],'--输出',str(dest),'--格式','webp','--长边','320','--质量','85'],check=True,stdout=subprocess.DEVNULL)
if '--仅响应式' in sys.argv:
    print('响应式图片已准备；没有改字体或页面入口。')
    sys.exit(0)

FONTS=ROOT/'assets/字体'
FONTS.mkdir(exist_ok=True)
dm=SRC/'制作交付/作品集展示/成果展示/V04/02_高级A+/02_可编辑SVG/DMSans-VF.ttf'
cn=Path('/workspace/design-resources/素材与工具/字体/Noto_Sans_SC/简体无衬线可变.ttf')
# 包括中英文正文、控件、来源说明及动态状态；生成网页后重跑可增补字形。
text=''.join(p.read_text() for p in (ROOT/'制作资料').glob('*') if p.suffix in ['.html','.css','.js'])
if (ROOT/'index.html').exists(): text+=(ROOT/'index.html').read_text()
text+=''.join(chr(i) for i in range(32,127))+'你好我是暮色夜间已复制复制失败请手动选择颜色上一张下一张关闭完整成果错误无法加载请打开来源原图显示尚未加载'+'，。；：！？「」／×·—→'
records=[]
for name,src in [('项目西文',dm),('网页中文',cn)]:
    font=TTFont(src)
    cmap=font.getBestCmap()
    if name=='网页中文':
        missing=sorted({c for c in text if '\u4e00'<=c<='\u9fff' and ord(c) not in cmap})
        assert not missing,missing
    options=subset.Options();options.flavor='woff';options.layout_features=['*'];options.name_IDs=['*'];options.name_legacy=True;options.name_languages=['*'];options.notdef_glyph=True;options.recommended_glyphs=True
    sub=subset.Subsetter(options=options);sub.populate(text=text);sub.subset(font)
    font.flavor='woff';font.save(FONTS/(name+'.woff'))
    records.append({'名称':name+'.woff','来源':str(src),'源SHA256':digest(src),'输出SHA256':digest(FONTS/(name+'.woff')),'字节数':(FONTS/(name+'.woff')).stat().st_size,'格式':'WOFF，变量字体子集；不是WOFF2'})
shutil.copy2(dm.parent/'DM-Sans-OFL.txt',FONTS/'DM_Sans_OFL.txt')
shutil.copy2(OLD/'Noto_Sans_SC_OFL.txt',FONTS/'Noto_Sans_SC_OFL.txt')
(ROOT/'字体记录.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print(json.dumps({'图片':len(list(OUT.glob('*.webp'))),'字体':records},ensure_ascii=False))
