import sys
src,dst=sys.argv[1],sys.argv[2]
t=open(src).read(); open(dst,'w').write(t)
i=t.find('- dialog')
if i<0: print('NO DIALOG IN SNAPSHOT'); raise SystemExit
for l in t[i:].split('\n'):
    l2=l.strip()
    if not l2 or 'img' in l2 or 'svg' in l2 or l2.startswith('- /url') or (l2.startswith('- generic [ref') and l2.endswith(':')) or 'Deselect' in l2 or 'sources" [disabled]' in l2 or 'source" [disabled]' in l2: continue
    print(l2[:200])
