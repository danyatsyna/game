"""Builds index.html (single file, GitHub Pages ready) from src/index.src.html."""
import base64, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
s = (root / 'src/index.src.html').read_text(encoding='utf-8')
hero = 'data:image/webp;base64,' + base64.b64encode((root / 'src/hero.webp').read_bytes()).decode()
demo = (root / 'demo-data/demo-year.json').read_text(encoding='utf-8')
assert s.count("var HERO_SRC='__HERO__';") == 1 and s.count('__DEMOYEAR__') == 1
s = s.replace('__HERO__', hero).replace('__DEMOYEAR__', demo)
(root / 'index.html').write_text(s, encoding='utf-8')
print('built index.html', len(s) // 1024, 'KB')
