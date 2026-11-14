---
name: "NED Eric Lamp · V02 局部候选"
description: "从空间氛围到购买信息：NED 电商视觉案例页的当前代码规则"
colors:
  case-bone: "#F4F1EB"
  case-sand: "#D8CABC"
  case-walnut: "#5A463B"
  case-charcoal: "#2F302E"
  case-terra: "#9B6B56"
  on-terra: "#fff"
typography:
  display:
    fontFamily: "'NED Latin','NED Chinese',sans-serif"
    fontSize: "calc(1 * clamp(44px, 3.429vw + 30.63px, 80px))"
    fontWeight: 400
    lineHeight: 1.02
    letterSpacing: "-.04em"
  headline:
    fontFamily: "'NED Latin','NED Chinese',sans-serif"
    fontSize: "clamp(32px,3.5vw,48px)"
    fontWeight: 400
    lineHeight: 1.38
    letterSpacing: "-.03em"
  title:
    fontFamily: "'NED Latin','NED Chinese',sans-serif"
    fontSize: "24px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "-.015em"
  lead:
    fontFamily: "'NED Latin','NED Chinese',sans-serif"
    fontSize: "20px"
    fontWeight: 400
    lineHeight: 1.9
  body:
    fontFamily: "'NED Latin','NED Chinese',sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.8
  label:
    fontFamily: "'NED Latin','NED Chinese',sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.8
rounded:
  image: "0px"
  control: "2px"
spacing:
  s-1: "4px"
  s-2: "8px"
  s-3: "12px"
  s-4: "16px"
  s-5: "24px"
  s-6: "32px"
  s-7: "48px"
  s-8: "64px"
  s-9: "96px"
  gut: "80px"
  padt: "112px"
  padb: "96px"
components:
  button-primary:
    backgroundColor: "{colors.case-walnut}"
    textColor: "{colors.case-bone}"
    rounded: "{rounded.control}"
    padding: "12px 24px"
  button-primary-hover:
    backgroundColor: "color-mix(in oklab, var(--action) 84%, var(--bg))"
  button-language:
    backgroundColor: "transparent"
    textColor: "{colors.case-charcoal}"
    rounded: "{rounded.control}"
    padding: "6px 12px"
  button-language-hover:
    backgroundColor: "{colors.case-bone}"
  button-scene:
    backgroundColor: "transparent"
    textColor: "{colors.case-charcoal}"
    rounded: "{rounded.control}"
    padding: "8px 16px"
  button-scene-selected:
    backgroundColor: "{colors.case-walnut}"
    textColor: "{colors.case-bone}"
    rounded: "{rounded.control}"
    padding: "8px 16px"
  button-copy:
    backgroundColor: "transparent"
    textColor: "{colors.case-bone}"
    rounded: "{rounded.control}"
    padding: "6px 16px"
  button-copy-hover:
    backgroundColor: "{colors.case-charcoal}"
  navigation:
    backgroundColor: "{colors.case-sand}"
    textColor: "{colors.case-charcoal}"
  palette-swatch-sand:
    backgroundColor: "{colors.case-sand}"
    textColor: "{colors.case-charcoal}"
    rounded: "{rounded.image}"
    padding: "24px"
  content-row:
    textColor: "{colors.case-charcoal}"
    padding: "32px 0"
  viewer-control:
    backgroundColor: "transparent"
    textColor: "{colors.case-bone}"
    padding: "8px 16px"
---

# Design System: NED Eric Lamp · V02 局部候选

## Overview

**Creative North Star: "从空间氛围到购买信息"**

“从空间氛围到购买信息”沿用本候选设计规划的方向摘要：暖墙、木纹、织物和局部灯光既构成作品氛围，也为网页阅读提供连续的色域。沙灰承接主要文字，深胡桃与炭灰建立深色章节，陶土承担局部暖色；骨白用于成果区域、浅色文字和有限的明亮表面。

这份文档是对 NED V02 当前 HTML／CSS／JavaScript 的扫描记录，只约束本目录内的候选案例页。它不是 NED 官方规范、实物校色结果或 Migo 全站 VI；Migo 是设计师主体，Beedog 是 Migo 的品牌角色。本次直接从已有作品与代码深化，不新增方向种子，也不把独立审阅者在局部契约范围内的 ship 结论记为用户批准。

**Key Characteristics:**

- 以通栏色域和开放式排版衔接图像与文字。
- 直角图片、轻微圆角控件，默认无卡片浮起阴影。
- 中文为主，原项目西文字体延续到网页；英文仍为审阅草稿。
- 正文自然增高，场景可取景，完整成果可查看原构图。

扫描依据为本目录的 [PRODUCT.md](PRODUCT.md)、[方向约定](.impeccable/surfaces/NED案例页.md)、[设计规划](设计规划.md)、[index.html](index.html)、[页面样式](制作资料/页面样式.css)、[页面交互](制作资料/页面交互.js)，并核对 HTML 实际加载的 system、layout、motion 与 picture-develops 文件及已有桌面／手机审阅截图。以最终样式级联为准；未启动浏览器进行新的 computed-style 采样。本文件只记录视觉规则，不代替执行记录、官方门禁结果或用户验收。

## Colors

五个原项目参考色形成暖中性的连续阅读环境，纯白仅作为陶土色域上的实际文字与焦点补充；色值以 frontmatter 为准。

### Primary

- **深胡桃（case-walnut）**：主要操作、背景介绍与 A+ 深色区域，也连接照片中的木质家具。

### Secondary

- **陶土（case-terra）**：产品识别章节与色谱中的局部暖色，回应材质；不描述实测灯光参数。

### Neutral

- **沙灰（case-sand）**：页面与导航的主要阅读底，联系暖墙与织物。
- **骨白（case-bone）**：商品图成果区域、深色域文字与少量明亮表面；不等同于禁止作品原图中的浅底。
- **炭灰（case-charcoal）**：浅色域正文、参考色章节和页脚深色底、图片查看器。
- **陶土上纯白（on-terra）**：陶土色域正文与焦点；不是第六个项目参考色。

**The Local Scope Rule.** 项目色通过 --case-* 管理，网站字体与文字入口通过 --site-* 管理；这里只记录 NED V02 已实现的局部候选，不把它升格为全站品牌规则。

**The Ground Pairing Rule.** 沙灰／骨白底使用炭灰正文，深胡桃／炭灰底使用骨白正文，陶土底使用纯白正文；修改底色时同时复核文字与焦点颜色。

当前五色没有定义连续色阶；sidecar 不合成 tonalRamp。细分隔线保留实际带透明度的深胡桃或沙灰，属于边界处理，不另设品牌色。纯色对比计算中，炭灰／沙灰为（8.27:1）、骨白／深胡桃为（7.85:1）、纯白／陶土为（4.53:1）；最后一组余量有限，更换字体、透明度或底色后须重新核查。这些是固定纯色对比值，不是整页无障碍认证。

## Typography

**Display Font:** 本地别名 `NED Latin` 对应原项目 DM Sans，后接 `NED Chinese` 与 sans-serif。

**Body Font:** 同一字体栈；`NED Chinese` 对应本地 Noto Sans SC 中文子集，是当前网页候选。

**Character:** 西文以常规字重和紧凑标题字距连接原成果，中文以较宽松的正文行高承载背景与策略。不新增第三套装饰字体；数值使用 tabular-nums，页面没有独立等宽字体角色。

### Hierarchy

- **Display**：对应开篇英文产品名，常规字重；桌面字号取已加载 layout 文件的 `--ly-h1-xl`，不是被更具体选择器覆盖的全局 h1 候选值。中屏（≤1023px）改用（clamp(48px,7vw,70px)）；手机（≤639px）改用（clamp(44px,12vw,68px)），行高（1.08）。
- **Headline**：对应章节标题；手机改为（30px）、行高（1.45）、字距（-.02em）。
- **Title**：对应正文内小标题；手机默认（22px）。商品图标题单独采用桌面（18px）／手机（16px），不能把它提升为章节标题。
- **Lead**：对应章节导语；手机为（18px）、行高（1.9）。开篇导语另用桌面行高（1.7）、手机（18px）。
- **Body**：常规正文默认最大行长（62ch）；手机改为（16px）与行高（1.85），局部继承规则以组件为准。A+ 正文容许（65ch）。加粗内容使用（500）。
- **Label**：对应边界说明、版本与状态文字。导航另用桌面（15px）／手机（13px），色谱数值说明为（13px），不用缩小正文来制造更多留白。

**The Live Text Rule.** 背景说明、策略、参考色名、HEX、RGB 和用途保持网页文字；原作品内的文字属于成果内容，不能用缩小长图替代网页正文。

字体采用 `font-display:swap`；两个本地文件都是 WOFF 变量字体子集，不是 WOFF2。DM Sans 声明字重范围（100–1000），Noto Sans SC 声明范围（100–900）；页面主要使用（400／500）。保留 [DM Sans OFL](assets/字体/DM_Sans_OFL.txt) 与 [Noto Sans SC OFL](assets/字体/Noto_Sans_SC_OFL.txt)，均为 SIL Open Font License 1.1。输出来源与校验值见 [字体记录](字体记录.json)。新增文案须补足子集字形；本文件不把候选字体升级为 Migo 品牌确认。

## Layout

所有章节共用居中容器：宽度取视口减两侧 gutter 与（1280px）中的较小值。桌面常用两栏开放排版；章节标题／导语为（1fr 1fr），策略为（1fr 1.4fr），背景为（1.05fr 1fr）。色域铺满视口，内部内容仍与导航对齐。正文采用自然高度，覆盖 kit 的整屏章节演示规则；不以 1H／2H 裁字。

间距主要沿现有（4／8）节奏组织；frontmatter 列出实际复用步长和桌面章节上下留白。较大的（96px）用于栏目分隔，小的（8／12／16px）用于状态控件和图注。实际还存在按版面职责设置的（40／80／112px），不推导新的等比尺度。

| 视口条件 | 两侧 gutter／导航高度 | 当前版面行为 |
| --- | --- | --- |
| ≥1600px | 96px／72px | 容器仍封顶1280px，开篇文字面宽500px |
| 1201–1599px | 80px／72px | 开篇文字面宽470px，照片在标题实色面旁保持主面积 |
| 1024–1200px | 48px／72px | 开篇文字面宽420px，部分列距缩小 |
| 640–1023px | 40px／64px | 开篇先文字再照片，章节标题与导语堆叠；上下留白96px／80px |
| ≤639px | 24px／64px | 主要内容单栏，上下留白64px／64px；首屏主操作随按钮行拉伸 |

商品图网格桌面为（4列），≤1023px 为（2列），手机仍保留两列以浏览整组；间距从（32px 24px）改为手机（24px 12px）。A+、故事与背景栏目在手机堆叠；角色分隔线从左边改到顶部。

色谱画布桌面列比（1.3fr 1fr .75fr），五色色域行比（.9fr 1.35fr 1.1fr 1fr 1fr）；≤1200px 微调列比，≤1023px 将材质／用途放至下一行，手机按场景、五色色域、材质与用途顺序堆叠。色块是选择控件，不是五颗装饰色点。

场景图与原成果采用不同图像规则：开篇与场景证据可 `cover` 取景，商品图、透明产品及 A+ 手机图使用 `contain` 保留识别。开篇桌面焦点位置为（62% center），中屏（70% center），手机（72% center）；手机图片高度为（34svh），限制在（220–320px）。场景证据比例桌面（1.5）、中屏（16/9）、手机（1.25）。不要把这些局部取景参数推广到所有成果。

成果图保留尺寸与说明；首屏图优先加载，其余图延迟加载。网页源通过实际 `srcset`／`sizes` 按屏幕选择资源：场景与照片使用长边（400／800px）变体及清晰原版本，商品网格预览使用宽度（320／640px）缩略图；放大链接与查看器仍指向完整成果。所有宽度描述符按 Pillow 读取的真实宽度生成，不把变体目录中的长边数值当作竖图宽度。`sizes` 根据开篇、策略、A+ 手机图与商品网格的显示区域分别设置，具体候选与表达式由[生成样稿脚本](制作资料/生成样稿.py)维护。`cover` 场景按裁切后的有效像素需求选图，不能只按容器宽度估计：手机开篇的 `sizes` 设为（600px）以补偿裁切；策略图按原图宽高比与当前画框宽高比的比值计算有效宽度，画框采用手机（1.25）、中屏（16/9）、桌面（1.5）。暮色与夜间各按自己的原图比例生成映射，切换时一并更新 `srcset` 和 `sizes`。材质特写区域采用胡桃底、grid 居中，图像以（176×176px）、`max-width:100%` 与 `object-fit:contain` 显示，保留源图尺寸而不放大。现有素材是 AI 辅助视觉与合成成果，不称实景摄影；保留各图来源属性与原图入口，本文不生成新图像。

## Elevation & Depth

当前页面以色域与真实成果图像建立深度，没有被使用的卡片阴影。开篇沙灰文字面显式设为无阴影；细线只区分导航、角色职责、内容行与页脚。图片查看器通过原生 dialog 的顶层与炭灰半透明遮罩区分前后关系，遮罩值为（#2F302EEB），不是投影系统。

**The Flat Surface Rule.** 深度由色域、照片和细分隔线建立；当前候选没有被使用的卡片阴影，不从已加载的 kit 中搬入未使用的浮起卡片。

开篇使用已加载的官方一次入场，标题单次动画（700ms），配套内容淡入（520ms），安全回显标记（700ms）；策略主图采用 film 方式一次显影（1600ms），缓动（cubic-bezier(.3,.2,.3,1)）。原图链接悬停轻微放大（1.03）；这些动作不创建循环背景或滚动劫持。减少动态效果时禁用位移／缩放并将本页过渡与动画压到（.01ms），显影图恢复静态；无脚本时已有图片与文字照常存在。sidecar 只提取本页实际使用的动作，未使用的 kit 循环、菜单、输入框阴影不在词汇表中。

## Shapes

图片、色域、场景边框与开放内容行采用直角；语言、主操作、场景与复制控件使用轻微圆角（2px）。边界以（1px）细线为主，原图查看器无额外装饰边框。色块的选中态是内缩（8px）的（1px）currentColor 轮廓，键盘焦点另用（3px）outline。

这里的 image／control 是对已实现形状的记录。kit 虽加载 sharp 半径变量，页面中的图片与这些控件以各自明确规则为准；未使用的 kit 卡片、面板和药丸形状不代表本候选规则。

## Components

### Buttons

主操作使用深胡桃底与骨白文字，内边距由 frontmatter 定义，最小高度（48px）、字号（16px），箭头为内联 SVG。hover 使用现有 color-mix，并在精细指针上上移（1px）；按下下移（1px）与缩放（.985），减少动态效果时保留色彩反馈。其他操作按职责保留透明底描边，不增加页面未实现的“次级 CTA”体系。

语言按钮使用沙灰环境、深胡桃透明描边，最小点击区域（48×44px），手机最小宽度（44px）；hover 转骨白底。场景按钮的选中态以 `aria-pressed` 配合深胡桃底／骨白文字，未选中透明底；当前无独立 hover 改色，不补造。场景键使用 `data-light-scene`，不复用 kit 的 `data-scene` 三维场景钩子。源入口切换场景时由 `window.NED_RESPONSIVE_MAP` 同步更新 `srcset` 与 `sizes`；无响应式映射时清除旧候选，避免仍显示上一个场景。复制按钮在深色域内使用沙灰描边、骨白文字，hover 转炭灰底；复制失败时选择可读的 HEX 并给出状态反馈。

全局 `:focus-visible` 为（3px）实线，偏移（5px），立即显示且不作过渡；浅色域用炭灰，深色域用骨白，陶土域用纯白。色块焦点改为向内偏移（-5px）并使用 currentColor。可见焦点不得只靠 hover 表达。

### Navigation

固定沙灰导航，Migo 为文字入口，项目内锚点以细下划线响应 hover／focus。桌面保留“作品案例”语境与三个章节入口；≤1023px 隐藏语境标签，手机隐藏最后一个成果锚点但保留首屏主操作。当前没有汉堡菜单、吸顶切换或滚动位置高亮。跳到正文链接在键盘聚焦时显示。

### Cards / Containers

当前没有重复卡片库。背景以两栏文字和角色分隔线组织，内容职责以开放列表行及下边线组织，商品图是无外壳的图像／标题／图注组合。不要把已加载但未使用的 cards.css 示例算作已实现组件。

### Palette Board

五个色域按钮同时展示色名、HEX 与 RGB；选中仅增加轮廓，不覆盖文字。右侧用途为 live region，复制反馈为 status。骨白和沙灰色块用炭灰文字，深胡桃和炭灰色块用骨白，陶土用纯白。照片色彩不要求逐像素匹配 HEX，也不附未经 ICC 转换的 CMYK。

### Image Viewer

八张原商品图均以完整构图进入原生 dialog；网格缩略图不替代放大原图。查看器关闭时也保留真实主图的初始 src 与说明，并采用延迟加载，不使用空图像地址。桌面宽度为（min(1040px,calc(100% - 48px))），手机留边（12px），图像使用 contain。查看器支持关闭、上一张／下一张、方向键、原生 Esc、Tab 边界处理、焦点返回与加载错误反馈。不支持 dialog 时原图链接仍可直接打开；不把静态 sidecar 预览描述成带这些脚本行为的运行实例。

便携 HTML 内嵌清晰单版本图像、样式、字体与交互；打包时移除 `srcset`／`sizes` 与响应式映射，避免把所有变体重复内嵌，并保留动态场景所需的资源寻址。随文件保留 taste-skill 许可证及字体 OFL。构建体积与静态资源数量见[构建记录](构建记录.json)，素材来源与导出参数见[素材来源](素材来源.json)；这些构建事实不作为视觉 token 或用户验收结果。

页面没有表单输入、筛选标签、工具提示或通用状态徽标；sidecar 不合成不存在的部件。

## Do's and Don'ts

### Do:

- Do 延续五个已有参考色的实际分工，并保留“非 NED 官方规范／非 Migo 最终 VI”的范围说明。
- Do 使用自然高度的正文与当前响应式堆叠，保留中英文内容和完整成果入口。
- Do 让场景取景保护 Eric 的灯罩、旋钮、灯杆和底座；商品图与透明产品图使用 contain 保留识别。材质特写按源图尺寸居中显示。
- Do 保持可见键盘焦点、aria-pressed、复制反馈、对话框关闭与焦点返回，以及减少动态效果和无 JavaScript 的阅读路径。
- Do 随字体子集保留 OFL 文件；新增文字或改字体后复查字形覆盖、换行和页面高度。

### Don't:

- Don't 把参考色或当前候选字体写成 NED 官方 VI、实物色号或 Migo 已定稿品牌规范。
- Don't 用重复白色圆角卡片替代本候选的通栏色域和开放排版；原成果里的浅色背景仍属于作品。
- Don't 把所有照片统一染成橙黄色，或为装饰裁掉完整商品图和产品轮廓。
- Don't 为机械整屏高度隐藏正文、删减策略或遮挡成果；不加入循环背景和滚动劫持。
- Don't 虚构色阶、表单、图像、设计种子或商业效果，也不把代码记录与检查结果写成用户终审。
