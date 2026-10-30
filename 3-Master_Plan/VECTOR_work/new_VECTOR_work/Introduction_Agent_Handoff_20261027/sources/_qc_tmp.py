import re, subprocess, sys, unicodedata

t = open('FOUNDY_Intro.bib', encoding='utf-8').read()
E = [e for e in re.split(r'\n(?=@)', t) if e.strip().startswith('@')]


def pdfs(key):
    for e in E:
        m = re.search(r'\n\s*title\s*=\s*\{(.*?)\},?\n', e, re.S)
        if m and key.lower() in re.sub(r'[{}]', '', m.group(1)).lower():
            f = re.search(r'\n\s*file\s*=\s*\{(.*?)\},?\n', e, re.S)
            if f:
                return re.findall(r'files/\d+/[^:;]*?\.pdf', f.group(1).replace('\\;', ';'))
    return []


def norm(s):
    s = unicodedata.normalize('NFKC', s).replace('ﬁ', 'fi').replace('ﬂ', 'fl')
    s = re.sub(r'[\u2018\u2019\u201c\u201d"\'`]', '', s)
    s = re.sub(r'-\s*\n\s*', '', s)
    s = re.sub(r'[\u2013\u2014\u2212-]', '-', s)
    return re.sub(r'\s+', ' ', s).lower()


for line in sys.stdin.read().strip().splitlines():
    key, q = line.split('|', 1)
    txt = ''.join(subprocess.run(['pdftotext', p, '-'], capture_output=True, text=True).stdout for p in pdfs(key))
    n, qq = norm(txt), norm(q)
    status = 'OK  ' if qq in n else ('PART' if qq[:40] in n else 'MISS')
    print(status, '|', key[:35], '|', q[:70])
