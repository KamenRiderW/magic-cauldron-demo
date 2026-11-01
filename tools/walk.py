from run import *
from sim2 import play_level
pot=55; w1h=[]; bad=0
for i,(n,c) in enumerate(zip(LEVELS,[5,7,7,12,11,8])):
    pot-=c; q=surv(n,c); w=w1_of(n,c); w1h.insert(0,w)
    W1=.5*w1h[0]+.3*(w1h[1] if len(w1h)>1 else 0)+.2*(w1h[2] if len(w1h)>2 else 0)
    bad = bad+1 if w>=.6 else (0 if w==0 else bad)
    rest=LEVELS[i+1:]; E=sum(E_G[x] for x in rest); M=sum(MAX_G[x] for x in rest)
    W3=w3_of(pot,rest); W=.35*W1+.25*w2_of(bad)+.4*W3
    print(f"L{i+1} n={n} cost={c} q={q:.3f} w1={w} W1={W1:.2f} bad={bad} W2={w2_of(bad)} pot={pot} E={E:.2f} M={M} r={(pot-E)/(M-E) if M else 0:.3f} W3={W3} W={W:.3f} {level_of(W)} pfail_green={pfail(i+1,pot) if rest else 0:.3f}")
# 第6关 橙档 下失败概率
import random
rnd=random.Random(3)
N=40000
f=sum(play_level(6,.6,rnd,potions=13)[3] for _ in range(N))/N
g=sum(play_level(6,0,rnd,potions=13)[3] for _ in range(N))/N
print('L6 pot13 fail: green',g,'orange',f)
# 各档单关均值（用于表格）
for n in (4,5,6):
  for p in (.3,.6,.9):
    cs=[play_level(n,p,rnd)[1] for _ in range(20000)]
    print(n,p,round(sum(cs)/len(cs),2),max(cs))
