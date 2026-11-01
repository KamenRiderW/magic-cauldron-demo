import itertools, random, statistics as st
from collections import Counter
LEVELS=[3,4,4,5,5,6]
PERMS={n:list(itertools.permutations(range(n))) for n in (3,4,5,6)}

def play_level(n, p_match, rnd, potions=None, honest=False):
    free=list(range(n)); C=PERMS[n]
    secret=rnd.choice(C) if honest else None
    t=cost=0; marks=[]; first=True
    while free:
        k=len(free)
        if potions is not None and potions-cost<k: return t,cost,marks,True
        g=rnd.choice(C); t+=1; cost+=k
        groups={}
        for x in C:
            key=tuple(i for i in free if x[i]==g[i]); groups.setdefault(key,[]).append(x)
        if honest:
            key=tuple(i for i in free if secret[i]==g[i])
        else:
            keys=[kk for kk in groups if kk] or list(groups)      # 保底进展
            if rnd.random()<p_match:                               # 倾向匹配：标记最多
                cand=[kk for kk in keys if not (first and len(kk)==k)] or keys   # 首次尝试不直接全对
                best=max(len(kk) for kk in cand)
                pool=[x for kk in cand if len(kk)==best for x in groups[kk]]
            else:
                pool=[x for kk in keys for x in groups[kk]]         # 常规：在保底集合中均匀
            tgt=rnd.choice(pool); key=tuple(i for i in free if tgt[i]==g[i])
        C=groups[key]; free=[i for i in free if i not in key]; marks.append(len(key)); first=False
    return t,cost,marks,False

if __name__=='__main__':
    rnd=random.Random(7); N=30000
    for n in (3,4,5,6):
        for lab,p,h in [('honest',0,True),('green',0,False),('yellow',.3,False),('orange',.6,False),('red',.9,False)]:
            cs=[play_level(n,p,rnd,honest=h)[1] for _ in range(N)]
            ts=None
            c=Counter(cs)
            print(n,lab,'mean %.2f'%st.mean(cs),'max',max(cs),'dist',{k:round(v/N,3) for k,v in sorted(c.items())})
