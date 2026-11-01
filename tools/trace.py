import itertools
NAMES='红黄蓝绿紫橙'
def check(ans, guesses):
    n=len(ans); locked=[None]*n; excl=set(); out=[]
    for g in guesses:
        assert all(locked[i] is None or g[i]==locked[i] for i in range(n)), 'must keep locked'
        assert all((i,g[i]) not in excl for i in range(n)), ('irrational',g)
        free=[i for i in range(n) if locked[i] is None]
        mk=[i for i in free if g[i]==ans[i]]
        for i in free:
            if i in mk: locked[i]=g[i]
            else: excl.add((i,g[i]))
        out.append((g,len(free),len(mk)))
    assert all(locked), 'not solved'
    return out
def find(n, first, want_marks):
    # 搜索：答案 + 后续理性猜测，使标记序列 == want_marks
    for ans in itertools.permutations(NAMES[:n]):
        ans=''.join(ans)
        def rec(locked, excl, gs, idx):
            free=[i for i in range(n) if locked[i] is None]
            if idx==len(want_marks): return gs if not free else None
            opts=[first] if idx==0 else [''.join(p) for p in itertools.permutations(NAMES[:n])]
            for g in opts:
                if any(locked[i] is not None and g[i]!=locked[i] for i in range(n)): continue
                if any((i,g[i]) in excl for i in range(n)): continue
                mk=[i for i in free if g[i]==ans[i]]
                if len(mk)!=want_marks[idx]: continue
                L=locked[:]; E=set(excl)
                for i in free:
                    if i in mk: L[i]=g[i]
                    else: E.add((i,g[i]))
                r=rec(L,E,gs+[g],idx+1)
                if r: return r
            return None
        r=rec([None]*n,set(),[],0)
        if r: return ans,r
for n,first,wm in [(3,'红黄蓝',[1,2]),(4,'红黄蓝绿',[1,3]),(4,'红黄蓝绿',[1,3]),(5,'红黄蓝绿紫',[1,1,3]),(5,'红黄蓝绿紫',[1,2,2]),(6,'红黄蓝绿紫橙',[4,2])]:
    ans,gs=find(n,first,wm)
    print(n,ans,[(g,k,m) for g,k,m in check(ans,gs)])
