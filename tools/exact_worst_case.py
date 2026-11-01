import itertools, sys
from functools import lru_cache
n=int(sys.argv[1])
P=list(itertools.permutations(range(n)))
sys.setrecursionlimit(100000)
# 对称性：答案集合在「列置换+颜色重命名」下等价，这里只做精确搜索 + 记忆化（以候选集为键）
@lru_cache(maxsize=None)
def worst(lockmask, C):
    free=[i for i in range(n) if not lockmask>>i&1]
    k=len(free)
    if k==0: return (0,0)
    bt=bc=0
    seen=set()
    for gi in C:
        g=P[gi]
        groups={}
        for xi in C:
            x=P[xi]
            key=0
            for i in free:
                if x[i]==g[i]: key|=1<<i
            groups.setdefault(key,[]).append(xi)
        keys=[kk for kk in groups if kk] or list(groups)
        for key in keys:
            # 新候选：与 g 在 key 位相同、在其余 free 位不同
            nc=frozenset(xi for xi in groups[key])  # groups[key] 恰为 match 集合==key 的候选
            t,c=worst(lockmask|key, nc)
            if t+1>bt: bt=t+1
            if c+k>bc: bc=c+k
    return (bt,bc)
print(n, worst(0, frozenset(range(len(P)))), worst.cache_info().currsize, flush=True)
