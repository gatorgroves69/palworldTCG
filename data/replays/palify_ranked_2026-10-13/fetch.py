"""Public GET-only, serialized 3-second cache. No auth, redirects, retries or bypasses."""
import pathlib as P,json,urllib.request,urllib.error,time,hashlib,datetime as D,gzip
ROOT=P.Path(__file__).resolve().parent; CACHE=ROOT/'cache'; CACHE.mkdir(exist_ok=True)
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**k):return None
OPENER=urllib.request.build_opener(NoRedirect)
def now():return D.datetime.now(D.timezone.utc).isoformat()
def get(url):
    assert url.startswith('https://palify.org/')
    key=hashlib.sha256(url.encode()).hexdigest();meta=CACHE/(key+'.meta.json');body=CACHE/(key+'.body.gz')
    if meta.exists():
        m=json.loads(meta.read_text());assert m['url']==url
        if m['status']!=200:raise RuntimeError('Cached non-success: '+str(m['status'])+' '+url)
        return gzip.decompress(body.read_bytes())
    ledger=ROOT/'requests.jsonl';last=ROOT/'last-request.json'
    if (ROOT/'BLOCKED.json').exists():raise RuntimeError('Collection blocked; inspect BLOCKED.json')
    if last.exists():time.sleep(max(0,3-(time.time()-json.loads(last.read_text())['epoch'])))
    start=time.time();last.write_text(json.dumps(dict(epoch=start,url=url)))
    req=urllib.request.Request(url,headers={'User-Agent':'palworldTCG-public-replay-research/1.0 (read-only; cached; max300 games)','Accept':'application/json,text/html,text/plain,*/*'})
    try:
        with OPENER.open(req,timeout=40) as r:raw=r.read();status=r.status;headers=dict(r.headers)
    except urllib.error.HTTPError as e:raw=e.read();status=e.code;headers=dict(e.headers)
    m=dict(url=url,method='GET',captured_utc=now(),status=status,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),content_type=headers.get('Content-Type'),retry_after=headers.get('Retry-After'))
    body.write_bytes(gzip.compress(raw,mtime=0));meta.write_text(json.dumps(m,indent=2)+'\n')
    with ledger.open('a') as f:f.write(json.dumps(m)+'\n')
    if status in (401,403,429): (ROOT/'BLOCKED.json').write_text(json.dumps(m,indent=2)+'\n')
    if status!=200:raise RuntimeError(f'HTTP {status}: {url}')
    return raw
if __name__=='__main__':
    import sys
    data=get(sys.argv[1]);print(data.decode()[:int(sys.argv[2]) if len(sys.argv)>2 else 10000])
