import datetime as dt, numpy as np, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

RED="#E31B23"; BLK="#111111"; GRY="#8a8a8a"; LG="#eeeeee"
D=dt.date
M=[(D(2012,7,11),1),(D(2013,7,9),10),(D(2014,1,9),20),(D(2014,3,15),25),
   (D(2016,12,8),50),(D(2018,12,8),75),(D(2019,8,25),100)]
MO=30.4375
def yr(d): return d.year+(d.timetuple().tm_yday-1)/365.25
def mon(a,b): return (b-a).days/MO

# ---- models
phases=[]
for (d0,s0),(d1,s1) in zip(M[:-1],M[1:]):
    m=mon(d0,d1); phases.append((d0,d1,s0,s1,m,(s1-s0)/m))
dbl=[("10M to 20M",M[1],M[2]),("25M to 50M",M[3],M[4]),("50M to 100M",M[4],M[6])]
dbl=[(n,mon(a[0],b[0])) for n,a,b in dbl]
# trend A: OLS on 25M,50M,75M
xs=np.array([(d-D(1970,1,1)).days for d,_ in M[3:6]],float); ys=np.array([s for _,s in M[3:6]],float)
sl,ic=np.polyfit(xs,ys,1)
dA=D(1970,1,1)+dt.timedelta(days=float((100-ic)/sl))
slA=sl*MO
# trend B: last 24 months (50->75)
slB=phases[4][5]; dB=M[5][0]+dt.timedelta(days=(100-75)/slB*MO)
act=M[6][0]
res=dict(slA=slA,dA=str(dA),mA=mon(act,dA),slB=slB,dB=str(dB),mB=mon(act,dB),
         last=phases[-1][5],phases=[(str(p[0]),str(p[1]),p[4],p[5]) for p in phases],dbl=dbl,
         r2=float(np.corrcoef(xs,ys)[0,1]**2))
json.dump(res,open("res.json","w"),indent=1,default=str)
print(json.dumps(res,indent=1,default=str))

plt.rcParams.update({"font.family":"DejaVu Sans","axes.spines.top":False,"axes.spines.right":False,"font.size":10})
# Fig1
fig,ax=plt.subplots(figsize=(7.2,3.8))
x=[yr(d) for d,_ in M]; y=[s for _,s in M]
ax.plot(x,y,color=BLK,lw=2.5,marker="o",ms=6,mfc=RED,mec=BLK)
for (d,s) in M: ax.annotate(f"{s}M",(yr(d),s),textcoords="offset points",xytext=(-6,7),ha="right",fontsize=9)
t=yr(D(2019,3,27)); ax.axvline(t,color=RED,ls="--",lw=1.3)
ax.text(t-0.08,6,"T-Series passes\nPewDiePie\n(Mar 27, 2019)",color=RED,ha="right",fontsize=8.5)
ax.plot(yr(D(2019,5,29)),100,marker="s",color=GRY,ms=7); ax.annotate("T-Series 100M\n(May 29, 2019)",(yr(D(2019,5,29)),100),xytext=(-70,-6),textcoords="offset points",fontsize=8,color=GRY,ha="right")
ax.set_ylabel("Subscribers (millions)"); ax.set_xlim(2012.2,2020); ax.set_ylim(0,110); ax.grid(axis="y",color=LG)
fig.tight_layout(); fig.savefig("figs/f1.png",dpi=200); plt.close()
# Fig2 velocity
fig,ax=plt.subplots(figsize=(7.2,3.4))
lab=[f"{a}M-{b}M" for a,b in [(p[2],p[3]) for p in phases]]
v=[p[5] for p in phases]
ax.bar(lab,v,color=[RED if i==len(v)-1 else BLK for i in range(len(v))])
for i,val in enumerate(v): ax.text(i,val+0.05,f"{val:.2f}",ha="center",fontsize=9)
ax.set_ylabel("Net subscribers gained per month (M)"); ax.set_ylim(0,3.5); ax.grid(axis="y",color=LG); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig("figs/f2.png",dpi=200); plt.close()
# Fig3 doubling
fig,ax=plt.subplots(figsize=(7.2,3.0))
ax.barh([d[0] for d in dbl][::-1],[d[1] for d in dbl][::-1],color=[BLK,BLK,RED][::-1][::-1] if False else [BLK,BLK,RED][::-1])
for i,d in enumerate(dbl[::-1]): ax.text(d[1]+0.4,i,f"{d[1]:.1f} months",va="center",fontsize=9)
ax.set_xlabel("Months to double subscriber base"); ax.set_xlim(0,42); ax.grid(axis="x",color=LG); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig("figs/f3.png",dpi=200); plt.close()
# Fig4 counterfactual
fig,ax=plt.subplots(figsize=(7.2,3.8))
ax.plot(x,y,color=BLK,lw=2.5,marker="o",ms=5,mfc=RED,mec=BLK,label="Actual milestones",zorder=3)
xa=np.linspace(yr(D(2014,3,15)),yr(dA),50); ax.plot(xa,np.interp(xa,[yr(D(2014,3,15)),yr(dA)],[25,100]),color=GRY,ls="--",label=f"Trend A: 25-75M OLS ({slA:.2f}M/mo)")
ax.plot([yr(M[5][0]),yr(dB)],[75,100],color=RED,ls=":",lw=2,label=f"Trend B: 2017-18 pace ({slB:.2f}M/mo)")
ax.axhline(100,color=LG,lw=1)
ax.annotate(f"Actual: Aug 2019",(yr(act),100),xytext=(-10,-3),textcoords="offset points",ha="right",fontsize=8.5)
ax.annotate(f"Trend B: {dB.strftime('%b %Y')}",(yr(dB),100),xytext=(-6,10),textcoords="offset points",ha="right",fontsize=8.5,color=RED)
ax.annotate(f"Trend A: {dA.strftime('%b %Y')}",(yr(dA),100),xytext=(4,10),textcoords="offset points",ha="left",fontsize=8.5,color=GRY)
ax.set_xlim(2013.8,2022.4); ax.set_ylim(0,115); ax.set_ylabel("Subscribers (millions)"); ax.legend(loc="lower right",fontsize=8,frameon=False); ax.grid(axis="y",color=LG)
fig.tight_layout(); fig.savefig("figs/f4.png",dpi=200); plt.close()
# Fig5 flywheel
fig,ax=plt.subplots(figsize=(7.2,4.6)); ax.set_xlim(-1.6,1.6); ax.set_ylim(-1.15,1.2); ax.axis("off")
nodes=["High-volume,\nconsistent uploads","Algorithmic reach\n& new viewers","Subscriber\nbase grows","Community identity\n('Bro Army')","Rallying events &\nrivalry (T-Series)"]
n=len(nodes); pts=[(1.05*np.sin(2*np.pi*i/n),0.85*np.cos(2*np.pi*i/n)) for i in range(n)]
for i,(p,t) in enumerate(zip(pts,nodes)):
    ax.add_patch(FancyBboxPatch((p[0]-0.42,p[1]-0.16),0.84,0.32,boxstyle="round,pad=0.02",fc=RED if i==4 else BLK,ec="none"))
    ax.text(p[0],p[1],t,color="white",ha="center",va="center",fontsize=8.6,fontweight="bold")
for i in range(n):
    a=pts[i]; b=pts[(i+1)%n]
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=16,color=GRY,lw=1.6,shrinkA=34,shrinkB=34,connectionstyle="arc3,rad=-0.15"))
ax.text(0,0,"Reinforcing\ngrowth loop",ha="center",va="center",fontsize=11,color=RED,fontweight="bold")
fig.tight_layout(); fig.savefig("figs/f5.png",dpi=200); plt.close()
# Fig6 timeline
ev=[(D(2010,4,29),"Channel\ncreated"),(D(2012,7,11),"1M"),(D(2013,7,9),"10M\n(first channel)"),(D(2016,12,8),"50M\n(first channel)"),
    (D(2018,12,8),"75M"),(D(2019,3,27),"T-Series\npasses him"),(D(2019,5,29),"T-Series\nhits 100M"),(D(2019,8,25),"100M\n(first individual)")]
fig,ax=plt.subplots(figsize=(7.2,2.9)); ax.set_ylim(-2.9,2.0); ax.set_xlim(2009.8,2020.4); ax.axis("off")
ax.plot([2010,2020],[0,0],color=BLK,lw=2)
off=[0.8,-0.8,0.8,-0.8,0.8,-0.8,1.4,-2.0]
for (d,t),o in zip(ev,off):
    c=RED if "T-Series" in t or "100M" in t else BLK
    ax.plot(yr(d),0,"o",color=c,ms=7); ax.plot([yr(d),yr(d)],[0,o*0.75],color=c,lw=1)
    ax.text(yr(d),o*0.8+(0.18 if o>0 else -0.18),t,ha="center",va="bottom" if o>0 else "top",fontsize=8,color=c)
for yy in (2010,2012,2014,2016,2018,2020): ax.text(yy,-0.12,str(yy),ha="center",va="top",fontsize=7,color=GRY)
fig.tight_layout(); fig.savefig("figs/f6.png",dpi=200); plt.close()
