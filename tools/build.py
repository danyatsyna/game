"""Builds index.html (single file, GitHub Pages ready) from src/index.src.html."""
import base64, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
s = (root / 'src/index.src.html').read_text(encoding='utf-8')
hero = 'data:image/webp;base64,' + base64.b64encode((root / 'src/hero.webp').read_bytes()).decode()
demo = (root / 'demo-data/demo-year.json').read_text(encoding='utf-8')
assert s.count("var HERO_SRC='__HERO__';") == 1 and s.count('__DEMOYEAR__') == 1
s = s.replace('__HERO__', hero).replace('__DEMOYEAR__', demo)
# standalone page: the artifact host adds this skeleton itself, GitHub Pages needs it explicitly
head = ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">'
        '<link rel="icon" type="image/png" href="favicon.png"><link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png?v=2"><link rel="manifest" href="manifest.webmanifest">'
        '<meta name="apple-mobile-web-app-title" content="DANIIL"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'
        '<style>:root{color-scheme:light}html:not(.on-hero) body{padding-top:env(safe-area-inset-top,0px)}'
        'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>')
(root / 'index.html').write_text(head + s.replace('<title>Билд Даниила</title>', '<title>DANIIL</title>', 1) + '</body></html>', encoding='utf-8')
print('built index.html', len(s) // 1024, 'KB')
