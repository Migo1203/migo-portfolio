(()=>{
 'use strict';
 const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
 let en=new URLSearchParams(location.search).get('lang')==='en';
 let scene='dusk',selected=$('.swatch[aria-pressed="true"]'),active=0,opener=null;
 const translated=$$('[data-en]');translated.forEach(e=>e.dataset.zh=e.innerHTML);
 const assets=window.NED_ASSET_MAP||{};const asset=p=>assets[p]||new URL(p,document.baseURI).href;
 const scenes={dusk:{src:'assets/图片/策略_餐桌暮色.webp',alt:'暮色中的Eric台灯置于餐桌，暖光照亮木纹和玻璃杯。',altEn:'Eric lamp at a dining table at dusk, lighting the wood and glass.',zh:'餐桌暮色：暖木与局部灯光形成生活氛围。',en:'Dining at dusk: warm wood and a local pool of light.'},night:{src:'assets/图片/夜间场景.webp',alt:'Eric台灯置于床头，暖光与蓝灰织物形成层次。',altEn:'Eric lamp by a bed, its warm light contrasting with cooler textiles.',zh:'床头夜间：保留蓝灰环境，突出局部暖光。',en:'Bedside at night: cooler surroundings keep the warm light distinct.'}};
 function renderColor(){$('#color-name').textContent=en?selected.dataset.nameEn:selected.dataset.color;$('#color-role').textContent=en?selected.dataset.roleEn:selected.dataset.role;$('#color-number').textContent=selected.dataset.hex;$('#copy-status').textContent='';}
 function renderScene(){const s=scenes[scene],img=$('#scene-image'),responsive=window.NED_RESPONSIVE_MAP?.[s.src];if(responsive){img.srcset=responsive.srcset;img.sizes=responsive.sizes;}else{img.removeAttribute('srcset');img.removeAttribute('sizes');}img.src=asset(s.src);img.alt=en?s.altEn:s.alt;$('#scene-note').textContent=en?s.en:s.zh;}
 function translate(){document.documentElement.lang=en?'en':'zh-CN';translated.forEach(e=>{if(en)e.textContent=e.dataset.en;else e.innerHTML=e.dataset.zh;});$('#language').textContent=en?'中文':'EN';$('#language').setAttribute('aria-label',en?'切换为中文':'Switch to English draft');$('.case-nav').setAttribute('aria-label',en?'Case navigation':'案例导航');renderColor();renderScene();if($('#lightbox').open)show(active);}
 $('#language').addEventListener('click',()=>{en=!en;translate();try{const u=new URL(location.href);u.searchParams.set('lang',en?'en':'zh');history.replaceState(null,'',u);}catch{}});
 $$('.scene-btn').forEach(b=>b.addEventListener('click',()=>{scene=b.dataset.lightScene;$$('.scene-btn').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));renderScene();}));
 $$('.swatch').forEach(b=>b.addEventListener('click',()=>{selected=b;$$('.swatch').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));renderColor();}));
 $('#copy-color').addEventListener('click',async()=>{try{if(!navigator.clipboard)throw new Error('clipboard unavailable');await navigator.clipboard.writeText(selected.dataset.hex);$('#copy-status').textContent=en?'HEX copied.':'已复制HEX。';}catch{const range=document.createRange();range.selectNodeContents($('#color-number'));const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);$('#copy-status').textContent=en?'Copy unavailable here. The HEX is selected; copy it manually.':'此环境不能自动复制，已选中色号，请手动复制。';}});
 const gallery=$$('.gallery-link'),dialog=$('#lightbox');
 function show(index){active=(index+gallery.length)%gallery.length;const a=gallery[active],img=a.querySelector('img');$('#viewer-image').src=a.href;$('#viewer-image').alt=img.alt;$('#lightbox-title').textContent=en?a.dataset.titleEn:a.dataset.title;$('#viewer-count').textContent=(active+1)+' / '+gallery.length;$('#image-error').textContent='';}
 gallery.forEach((a,i)=>a.addEventListener('click',e=>{if(typeof dialog.showModal!=='function')return;e.preventDefault();opener=a;show(i);dialog.showModal();document.body.classList.add('viewer-open');$('#close-viewer').focus();}));
 $('#close-viewer').addEventListener('click',()=>dialog.close());$('#previous').addEventListener('click',()=>show(active-1));$('#next').addEventListener('click',()=>show(active+1));
 dialog.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){e.preventDefault();show(active-1);}if(e.key==='ArrowRight'){e.preventDefault();show(active+1);}if(e.key==='Tab'){const buttons=[...dialog.querySelectorAll('button:not(:disabled)')],first=buttons[0],last=buttons[buttons.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}});
 dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
 dialog.addEventListener('close',()=>{document.body.classList.remove('viewer-open');opener?.focus();});
 $('#viewer-image').addEventListener('error',()=>{$('#image-error').textContent=en?'The image could not load. Close the viewer and use the original artwork source.':'图片未能加载。请关闭查看器，并从作品来源打开原稿。';});
 translate();
})();
