import random, statistics as st, json
from collections import Counter
from sim2 import play_level, LEVELS
rnd=random.Random(11)
# ---- 离线：绿档（仅保底规则）单关消耗分布
N=40000
DIST={}
for n in (3,4,5,6):
    c=Counter(play_level(n,0,rnd)[1] for _ in range(N)); DIST[n]={k:v/N for k,v in sorted(c.items())}
E_G={n:sum(k*p for k,p in d.items()) for n,d in DIST.items()}
MAX_G={3:5,4:7,5:12,6:18}   # 精确穷举结果
def surv(n,cost): return sum(p for k,p in DIST[n].items() if k>=cost)
def w1_of(n,cost):
    q=surv(n,cost)
    return 1.0 if q<=.10 else .6 if q<=.25 else .2 if q<=.50 else 0.0
def w2_of(bad): return [0,.3,.7,1.0][min(bad,3)]
def w3_of(pot, rest):
    if not rest: return 0.0
    E=sum(E_G[n] for n in rest); M=sum(MAX_G[n] for n in rest)
    if pot>=M: return 0.0
    r=(pot-E)/(M-E)
    return 1.0 if r<0 else .7 if r<.5 else .4
def level_of(W): return 'red' if W>=.7 else 'orange' if W>=.5 else 'yellow' if W>=.3 else 'green'
PM={'green':0,'yellow':.3,'orange':.6,'red':.9}
# 失败概率表（绿档、理性随机玩家）：P(剩余关卡总消耗 > 药水)
def conv(a,b):
    o={}
    for x,p in a.items():
        for y,q in b.items(): o[x+y]=o.get(x+y,0)+p*q
    return o
def pfail(i,pot):
    d={0:1.0}
    for n in LEVELS[i:]: d=conv(d,DIST[n])
    return sum(p for k,p in d.items() if k>pot)

def run(S0, dda=True, honest=False):
    pot=S0; w1h=[]; bad=0; mode='green'; modes=[]; spent=0
    for i,n in enumerate(LEVELS):
        modes.append(mode)
        t,c,mk,failed=play_level(n, PM[mode] if dda else 0, rnd, potions=pot, honest=honest)
        pot-=c; spent+=c
        if failed: return dict(fail=True,level=i+1,spent=spent,modes=modes)
        w=w1_of(n,c); w1h.insert(0,w)
        W1=.5*w1h[0]+.3*(w1h[1] if len(w1h)>1 else 0)+.2*(w1h[2] if len(w1h)>2 else 0)
        bad = bad+1 if w>=.6 else (0 if w==0 else bad)
        W2=w2_of(bad); W3=w3_of(pot, LEVELS[i+1:])
        W=.35*W1+.25*W2+.40*W3
        mode=level_of(W)
    return dict(fail=False,spent=spent,left=pot,modes=modes)

if __name__=='__main__':
    print('E_G',{k:round(v,2) for k,v in E_G.items()},'sumE',round(sum(E_G[n] for n in LEVELS),2))
    print('DIST',json.dumps({n:{k:round(p,3) for k,p in d.items()} for n,d in DIST.items()}))
    M=20000
    for S0 in (45,48,50,52,55,58,61):
        row=[]
        for lab,kw in [('honest',dict(dda=False,honest=True)),('rule',dict(dda=False)),('dda',dict(dda=True))]:
            rs=[run(S0,**kw) for _ in range(M)]
            fr=sum(r['fail'] for r in rs)/M
            sp=st.mean(r['spent'] for r in rs if not r['fail']) if fr<1 else 0
            iv=sum(any(m!='green' for m in r['modes']) for r in rs)/M
            row.append(f"{lab}: fail {fr:.1%} spent {sp:.1f} interv {iv:.0%}")
        print(S0,' | '.join(row), '| pfail_table', f"{pfail(0,S0):.1%}")
    print('pfail table (level idx start, potions):')
    for i in range(6):
        print(i+1,[ (p, round(pfail(i,p),3)) for p in range(sum(n for n in LEVELS[i:]), sum(MAX_G[n] for n in LEVELS[i:])+1, 3)])
