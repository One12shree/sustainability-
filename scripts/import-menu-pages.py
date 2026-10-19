from pathlib import Path
import re,json,urllib.request,hashlib,concurrent.futures,html
sources={p.stem:p.read_text(encoding='utf-8') for p in Path('scripts/references').glob('*.html')}
urls=set()
for s in sources.values():
 urls.update(html.unescape(u) for u in re.findall(r'<img[^>]*src=["\']([^"\']+)',s))
 for tag in re.findall(r'<link[^>]*>',s):
  if 'stylesheet' in tag:
   m=re.search(r'href=["\']([^"\']+)',tag)
   if m and 'thesustainabilist.ae' in m[1]:urls.add(html.unescape(m[1]))
targets=['ramadan','contribute','our-issues']
lookup={};errors=[]
def fetch(u):
 base=u.split('?')[0].split('/')[-1]
 if base in ['logo.png','ramadan-menu-1.svg','contribute.svg','issue.svg'] or base.endswith('.css') and Path('static/assets',base).exists():return u,'/assets/'+base
 name='page-'+hashlib.sha256(u.encode()).hexdigest()[:12]+'-'+base
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read();Path('static/assets',name).write_bytes(b);return u,'/assets/'+name
 except Exception as e:errors.append((u,str(e)));return u,u
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:lookup=dict(ex.map(fetch,urls))
for slug,s in sources.items():
 styles=[]
 for tag in re.findall(r'<link[^>]*>',s):
  if 'stylesheet' in tag:
   m=re.search(r'href=["\']([^"\']+)',tag)
   if m and html.unescape(m[1]) in lookup:
    u=lookup[html.unescape(m[1])]
    if u not in styles:styles.append(u)
 b=re.search(r'<body[^>]*>(.*)</body>',s,re.S)[1]
 b=re.sub(r'<script\b[^>]*>.*?</script>|<link\b[^>]*>','',b,flags=re.S|re.I)
 b=re.sub(r'\s+on\w+=(?:"[^"]*"|\'[^\']*\')','',b)
 for u,local in lookup.items(): b=b.replace(u,local).replace(html.escape(u,quote=False),local)
 # Preserve the issue reader visually, omit WordPress form/CAPTCHA frames.
 b=re.sub(r'<iframe\b[^>]*>.*?</iframe>',lambda m:m[0] if 'e.issuu.com' in m[0] else '',b,flags=re.S|re.I)
 b=re.sub(r'<textarea([^>]*)>.*?</textarea>',r'<textarea\1></textarea>',b,flags=re.S)
 b=re.sub(r'(<input\b[^>]*type=["\'])submit(["\'])',r'\1button\2',b,flags=re.I)
 b=re.sub(r'<input\b[^>]*type=["\']hidden["\'][^>]*>','',b,flags=re.I)
 for target in targets:
  b=re.sub(r'href=["\']https://thesustainabilist.ae/'+target+r'/?["\']', 'href="/'+target+'/"',b)
 b=b.replace('href="https://thesustainabilist.ae/"','href="/"')
 b=re.sub(r'<ul\b[^>]*id=["\']menu-header-menu["\'][^>]*>.*?</ul>',lambda m:re.sub(r'<a\b[^>]*>(.*?)</a>',r'<a>\1</a>',m[0],flags=re.S|re.I),b,flags=re.S|re.I)
 cut=b.find('<div class="page-wrap">')
 if cut>=0:b=re.sub(r'</a\s*>','</span>',re.sub(r'<a\b[^>]*>','<span class="menu-label">',b[:cut],flags=re.I),flags=re.I)+b[cut:]
 for asset,target in {'ramadan-menu-1.svg':'ramadan','contribute.svg':'contribute','issue.svg':'our-issues'}.items():
  pattern=r'<span class="menu-label">(<div class="tooltip">\s*<img[^>]*src="/assets/'+re.escape(asset)+r'".*?</div>)</span>'
  b=re.sub(pattern,lambda m:'<a href="/'+target+'/">'+m[1]+'</a>',b,flags=re.S)
 Path('src/lib/'+slug+'.json').write_text(json.dumps({'styles':styles,'body':b},ensure_ascii=False),encoding='utf-8')
print('Localized assets:',len(lookup),'failures:',errors)
