"""从已维护的线框 HTML 生成 GitHub Pages 发布目录，不安装依赖。"""

import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import shutil
from urllib.parse import unquote, urlsplit


GALLERY_IMAGES = (
    "00_主图_近白底_V01.webp", "01_产品展示_V02.webp",
    "02_旋钮操作_V02.webp", "03_光色调节_V01.webp",
    "04_夜间无线续航_V02.webp", "05_尺寸材质_V02.webp",
    "06_户外使用_V02.webp", "07_多场景使用_V02.webp",
)

V03_ROOT = "UI设计/NED网页展示/V03"
V03_CASE_ART = ("brand-story", "aplus-composed", "banner")

V03_PREVIEW_FILES = (
    "UI设计/NED网页展示/V03/首屏A.html",
    "UI设计/NED网页展示/V03/首屏.css",
    *(f"{V03_ROOT}/{name}" for name in ("高级A+.css", "品牌故事.css", "成果与复盘.css", "图文切换.js")),
    "UI设计/NED网页展示/V03/assets/palette/sand-wall.webp",
    "UI设计/NED网页展示/V03/assets/palette/walnut-table.webp",
    "UI设计/NED网页展示/V03/assets/palette/charcoal-fabric.webp",
    "UI设计/NED网页展示/V03/assets/palette/terracotta-vase.webp",
    "UI设计/NED网页展示/V02/assets/字体/项目西文.woff",
    "UI设计/NED网页展示/V02/assets/字体/网页中文.woff",
    "UI设计/NED网页展示/V02/assets/图片/封面_原场景裁切.webp",
    "UI设计/NED网页展示/V02/assets/图片/策略_餐桌暮色.webp",
    "UI设计/NED网页展示/V02/assets/图片/夜间场景.webp",
    "UI设计/NED网页展示/V02/assets/图片/策略_产品透明抠图.webp",
    "UI设计/NED网页展示/V02/assets/图片/A加操作.webp",
    "UI设计/NED网页展示/V02/assets/图片/品牌生活.webp",
    "UI设计/NED网页展示/V02/assets/图片/材质特写.webp",
    *(f"UI设计/NED网页展示/V02/assets/响应式/400/{name}"
      for name in ("策略_餐桌暮色.webp", "夜间场景.webp", "A加操作.webp", "品牌生活.webp")),
    *(f"UI设计/NED网页展示/V02/assets/响应式/800/{name}"
      for name in ("夜间场景.webp", "A加操作.webp", "品牌生活.webp")),
    *(f"UI设计/NED网页展示/V02/assets/{folder}/{name}"
      for folder in ("图片", "缩略图", "响应式/缩略320") for name in GALLERY_IMAGES),
)


class PreviewDependencyCheck(HTMLParser):
    """检查 V03 的本地图片、响应式候选、样式和脚本是否纳入发布。"""

    def __init__(self, repo, document, files):
        super().__init__()
        self.repo = repo
        self.document = document
        self.files = set(files)
        self.missing = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        candidates = []
        if tag in {"img", "source", "script"} and attrs.get("src"):
            candidates.append(attrs["src"])
        if tag == "link" and attrs.get("rel") == "stylesheet" and attrs.get("href"):
            candidates.append(attrs["href"])
        if tag in {"img", "source"}:
            candidates.extend(item.split()[0] for item in (attrs.get("srcset") or "").split(",") if item.strip())
        for candidate in candidates:
            url = urlsplit(candidate)
            if url.scheme or url.netloc or not url.path:
                continue
            target = (self.document.parent / unquote(url.path)).resolve()
            if not target.is_relative_to(self.repo):
                raise ValueError(f"V03 资源需使用仓库内的相对路径：{candidate}")
            relative = target.relative_to(self.repo).as_posix()
            if relative not in self.files:
                self.missing.add(relative)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="独立的发布输出目录")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    source = repo / "线框/第三版/线框审阅.html"
    output = args.output.resolve()
    if output == repo or output in source.parents:
        parser.error("输出目录不能覆盖仓库根目录或线框源目录")
    html = source.read_text(encoding="utf-8")
    required = ('name="robots"', 'noindex,nofollow', 'id="wireframe"', 'window.wireframeState')
    if not all(marker in html for marker in required):
        raise ValueError("线框源文件缺少必要标记，请先核对原型与发布范围")
    v03 = repo / V03_ROOT / "首屏A.html"
    art = sorted(
        path.relative_to(repo).as_posix()
        for group in V03_CASE_ART
        for path in (repo / V03_ROOT / "assets" / group).glob("*.webp")
        if path.is_file()
    )
    preview_files = (*V03_PREVIEW_FILES, *art)
    dependencies = PreviewDependencyCheck(repo, v03, preview_files)
    dependencies.feed(v03.read_text(encoding="utf-8"))
    dependencies.close()
    if dependencies.missing:
        raise ValueError("V03 资源未纳入发布：\n" + "\n".join(sorted(dependencies.missing)))
    output.mkdir(parents=True, exist_ok=True)
    (output / "index.html").write_text(html, encoding="utf-8")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    for relative in preview_files:
        source_file = repo / relative
        if not source_file.is_file():
            raise FileNotFoundError(f"V03预览依赖缺失：{relative}")
        target_file = output / relative
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)
    manifest = {
        "scope": "网站线框与NED V03完整案例嵌入审阅，非正式作品集网站",
        "source": source.relative_to(repo).as_posix(),
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "files": ["index.html", ".nojekyll", *preview_files, "部署清单.json"],
    }
    (output / "部署清单.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"output": str(output), **manifest}, ensure_ascii=False))


if __name__ == "__main__":
    main()
