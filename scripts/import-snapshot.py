import pathlib,re,json,shutil
from html.parser import HTMLParser
root=pathlib.Path.cwd(); assets=pathlib.Path(r'C:/Users/Moro/Downloads/The Sustainabilist_files')
s=pathlib.Path(r'C:/Users/Moro/Downloads/The Sustainabilist.html').read_text(encoding='utf-8')
for f in assets.iterdir():
 if f.is_file() and f.suffix.lower() in ['.css','.jpg','.jpeg','.png','.svg','.gif','.webp','.woff','.woff2','.ttf','.ico'] or f.name=='css':
  shutil.copy2(f,root/'static/assets'/f.name)
styles=[]
for tag in re.findall(r'<link\b[^>]*>',s):
 if 'stylesheet' in tag:
  m=re.search(r'href="([^"]+)"',tag)
  if m and 'The Sustainabilist_files/' in m[1] and '23b23' not in m[1]:
   url=m[1].replace('./The Sustainabilist_files/','/assets/')
   if url not in styles: styles.append(url)
b=re.search(r'<body[^>]*>(.*)</body>',s,re.S)[1]
b=re.sub(r'<script\b[^>]*>.*?</script>|<iframe\b[^>]*>.*?</iframe>|<link\b[^>]*>','',b,flags=re.S|re.I)
b=re.sub(r'\s+on\w+="[^"]*"','',b)
b=b.replace('./The Sustainabilist_files/','/assets/').replace('�s', '’s').replace(' � ', ' – ')
b=re.sub(r'<li style="position: absolute;[^"]*"[^>]*>\s*</li>','',b)
b=re.sub(r'(<li) style="position: absolute;[^"]*"',r'\1',b)
b=re.sub(r'(<ul class="grid[^"]*" id="grid") style="[^"]*"',r'\1',b)
b=re.sub(r'<form[^>]*id="gform_1".*?</form>','<p><a href="https://thesustainabilist.ae/contact-us/">Contact The Sustainabilist</a></p>',b,flags=re.S)
b=b.replace('name="phrase" placeholder=', 'name="s" placeholder=').replace('action="https://thesustainabilist.ae/#" autocomplete=', 'action="https://thesustainabilist.ae/" autocomplete=')
b=re.sub(r'<img(?![^>]*loading=)', '<img loading="lazy"',b)
b=b.replace('<img loading="lazy" src="/assets/logo.png"','<img src="/assets/logo.png"')
(root/'src/lib/homepage.json').write_text(json.dumps({'styles':styles,'body':b},ensure_ascii=False),encoding='utf-8')
print('Copied',len(list((root/'static/assets').iterdir())),'assets; article links',len(re.findall(r'\+ Read More',b)))
