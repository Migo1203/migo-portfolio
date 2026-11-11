"""从已维护的线框 HTML 生成 GitHub Pages 发布目录，不安装依赖。"""

import argparse
import hashlib
import json
from pathlib import Path


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
    output.mkdir(parents=True, exist_ok=True)
    (output / "index.html").write_text(html, encoding="utf-8")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    manifest = {
        "scope": "低保真线框审阅，非正式作品集网站",
        "source": source.relative_to(repo).as_posix(),
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "files": ["index.html", ".nojekyll", "部署清单.json"],
    }
    (output / "部署清单.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"output": str(output), **manifest}, ensure_ascii=False))


if __name__ == "__main__":
    main()
