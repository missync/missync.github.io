from style import *
import numpy as np
rng=np.random.default_rng(0)

# 1. activation statistics across layers for different inits
def run(act, std_fn, L=10, n=512, B=1000):
    x=rng.standard_normal((B,n)); stds=[]; hs=[]
    for l in range(L):
        W=rng.standard_normal((n,n))*std_fn(n)
        z=x@W; x=act(z); stds.append(x.std()); hs.append(x.ravel()[:20000])
    return stds,hs
tanh=np.tanh; relu=lambda z:np.maximum(z,0)
cfgs=[('tanh, σ=0.01（过小）',tanh,lambda n:0.01),
      ('tanh, σ=1（过大）',tanh,lambda n:1.0),
      ('tanh, Xavier',tanh,lambda n:np.sqrt(1/n)),
      ('ReLU, Xavier',relu,lambda n:np.sqrt(1/n)),
      ('ReLU, He',relu,lambda n:np.sqrt(2/n))]
res=[run(a,f) for _,a,f in cfgs]
fig=plt.figure(figsize=(12,6.2))
gs=fig.add_gridspec(2,4,height_ratios=[1,1],hspace=0.45,wspace=0.3)
ax=fig.add_subplot(gs[:,0:2])
for i,(name,_,_) in enumerate(cfgs):
    ax.plot(range(1,11),res[i][0],'o-',color=C[i],label=name,lw=2,ms=4)
ax.set_yscale('log'); ax.set_xlabel('层数'); ax.set_ylabel('激活值标准差（对数轴）')
ax.set_title('激活值的尺度随深度如何变化'); ax.legend(fontsize=9.5,loc='lower left')
picks=[0,1,2,4]; titles=['tanh + σ 过小：逐层坍缩到 0','tanh + σ 过大：挤到 ±1 饱和区','tanh + Xavier：分布稳定','ReLU + He：分布稳定']
for k,i in enumerate(picks):
    a=fig.add_subplot(gs[k//2,2+k%2])
    h=res[i][1]
    for l,col in [(0,'#9db9ef'),(4,'#4f86e8'),(9,'#173f8f')]:
        d=h[l]; 
        if i==4: d=d[d>0]
        a.hist(d,bins=60,histtype='step',color=col,lw=1.5,density=True,label=f'第{l+1}层')
    a.set_title(titles[k],fontsize=10); a.set_yticks([])
    if k==0: a.legend(fontsize=8)
fig.suptitle('同一个 10 层、每层 512 个单元的全连接网络，只改变初始化',y=0.99,fontsize=13)
save(fig,'init-activation-scale.png')

# 2. loss landscape with/without normalization
def gd(grad,p0,lr,steps):
    p=np.array(p0,float); tr=[p.copy()]
    for _ in range(steps): p=p-lr*grad(p); tr.append(p.copy())
    return np.array(tr)
fig,axs=plt.subplots(1,2,figsize=(11,4.6))
for ax,(a,b,title,lr) in zip(axs,[(1,25,'特征尺度差异大：等高线狭长',0.038),(1,1.3,'归一化后：等高线接近圆形',0.3)]):
    X,Y=np.meshgrid(np.linspace(-3,3,300),np.linspace(-3,3,300))
    Z=a*X**2+b*Y**2
    ax.contour(X,Y,Z,levels=np.geomspace(0.05,80,14),cmap='Blues_r',linewidths=1)
    tr=gd(lambda p:np.array([2*a*p[0],2*b*p[1]]),[-2.7,1.2],lr,25)
    ax.plot(tr[:,0],tr[:,1],'o-',color=C[1],ms=3.5,lw=1.4)
    ax.plot(0,0,'*',color='k',ms=12)
    ax.set_title(title); ax.set_xlabel('$w_1$'); ax.set_ylabel('$w_2$'); ax.set_aspect('equal'); ax.grid(False)
    ax.text(-2.9,-2.8,f'学习率 η={lr}，迭代 25 步',fontsize=9,color='#444')
fig.suptitle('输入各维尺度不同 → 损失面某些方向特别陡；归一化让梯度下降走得更直',fontsize=12)
save(fig,'normalization-landscape.png')

# 3. normalization family: grid N x C, each cell = HxW
import matplotlib.patches as mp
fig,axs=plt.subplots(1,4,figsize=(13,3.6))
N,Cc=6,8
groups={'Batch Norm':lambda n,c:c==2,'Layer Norm':lambda n,c:n==2,'Instance Norm':lambda n,c:(n==2 and c==2),'Group Norm':lambda n,c:(n==2 and 2<=c<=3)}
desc={'Batch Norm':'同一通道、跨整个 batch\n统计量形状 1×C×1×1','Layer Norm':'同一样本、跨全部通道\n统计量形状 N×1×1×1','Instance Norm':'同一样本、同一通道\n统计量形状 N×C×1×1','Group Norm':'同一样本、同一组通道\n统计量形状 N×G×1×1'}
for ax,(name,f) in zip(axs,groups.items()):
    for n in range(N):
        for c in range(Cc):
            ax.add_patch(mp.Rectangle((n,c),0.92,0.92,color=C[0] if f(n,c) else '#e6ecf5'))
    ax.set_xlim(-0.3,N+0.2); ax.set_ylim(-0.3,Cc+0.2); ax.set_aspect('equal'); ax.grid(False)
    ax.set_xticks([]); ax.set_yticks([]); 
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xlabel('样本 N →'); ax.set_ylabel('通道 C →')
    ax.set_title(name); ax.text(N/2,-1.6,desc[name],ha='center',va='top',fontsize=9.5)
fig.suptitle('每个小方块代表一张 H×W 特征图；蓝色方块共同计算一组均值和方差',fontsize=12,y=1.02)
save(fig,'normalization-family.png')

# 4. optimizer trajectories on ill-conditioned function
def f(p): x,y=p; return 0.1*x**2+2*y**2
def g(p): x,y=p; return np.array([0.2*x,4*y])
def opt(name,steps=60,lr=0.1):
    p=np.array([-4.5,1.6]); tr=[p.copy()]; m=np.zeros(2); v=np.zeros(2); G=np.zeros(2)
    for t in range(1,steps+1):
        gr=g(p)
        if name=='SGD': p=p-lr*gr*4.5
        elif name=='Momentum': m=0.8*m-lr*gr*0.9; p=p+m
        elif name=='Adagrad': G+=gr**2; p=p-0.9*gr/(np.sqrt(G)+1e-8)
        elif name=='RMSProp': v=0.9*v+0.1*gr**2; p=p-0.12*gr/(np.sqrt(v)+1e-8)
        elif name=='Adam':
            m=0.9*m+0.1*gr; v=0.999*v+0.001*gr**2
            mh=m/(1-0.9**t); vh=v/(1-0.999**t); p=p-0.15*mh/(np.sqrt(vh)+1e-8)
        tr.append(p.copy())
    return np.array(tr)
names=['SGD','Momentum','Adagrad','RMSProp','Adam']
fig,axs=plt.subplots(1,2,figsize=(12.5,4.6),gridspec_kw={'width_ratios':[1.6,1]})
X,Y=np.meshgrid(np.linspace(-5,1.5,300),np.linspace(-2.2,2.2,300))
ax=axs[0]; ax.contour(X,Y,0.1*X**2+2*Y**2,levels=np.geomspace(0.02,12,14),colors='#b9c6dc',linewidths=0.9)
trs={}
for i,nm in enumerate(names):
    tr=opt(nm); trs[nm]=tr; ax.plot(tr[:,0],tr[:,1],'.-',color=C[i],label=nm,lw=1.4,ms=4)
ax.plot(0,0,'*k',ms=12); ax.set_title('前 60 步的参数轨迹（x 方向平缓，y 方向陡峭）'); ax.legend(ncol=5,fontsize=9,loc='upper center',bbox_to_anchor=(0.5,-0.13)); ax.grid(False)
ax.set_xlabel('$\\theta_1$'); ax.set_ylabel('$\\theta_2$')
ax=axs[1]
for i,nm in enumerate(names):
    ax.semilogy([f(p)+1e-6 for p in trs[nm]],color=C[i],label=nm,lw=1.8)
ax.set_xlabel('迭代步数'); ax.set_ylabel('损失（对数轴）'); ax.set_title('损失下降曲线')
fig.suptitle('同一个病态二次函数 L = 0.1·θ₁² + 2·θ₂² 上的五种优化器',fontsize=12)
save(fig,'optimizer-trajectories.png')

# 5. LR schedules
T=100; t=np.arange(T+1); a0=0.1
step=a0*0.1**np.searchsorted([30,60,90],t,side='right')
cos=0.5*a0*(1+np.cos(np.pi*t/T)); lin=a0*(1-t/T); isq=a0/np.sqrt(np.maximum(t,1))
d=512; s=np.arange(1,40001); warm=4000; tr_lr=d**-0.5*np.minimum(s**-0.5,s*warm**-1.5)
fig,axs=plt.subplots(1,3,figsize=(13.5,3.8))
ax=axs[0]; ax.step(t,step,where='post',color=C[0],lw=2); ax.set_title('阶梯衰减 Step'); ax.set_xlabel('epoch'); ax.set_ylabel('学习率')
ax.text(31,0.06,'在 30/60/90 处\n各乘 0.1',fontsize=9)
ax=axs[1]; ax.plot(t,cos,color=C[1],lw=2,label='余弦 Cosine'); ax.plot(t,lin,color=C[2],lw=2,label='线性 Linear'); ax.plot(t[1:],isq[1:],color=C[3],lw=2,label='$\\alpha_0/\\sqrt{t}$')
ax.set_ylim(0,0.105); ax.set_title('连续衰减'); ax.set_xlabel('epoch'); ax.legend(fontsize=9)
ax=axs[2]; ax.plot(s,tr_lr,color=C[4],lw=2); ax.axvline(warm,ls='--',color='#999'); ax.text(warm*1.15,tr_lr.max()*0.95,'warmup_steps\n=4000',fontsize=9)
ax.set_title('Warmup + 衰减（原始 Transformer）'); ax.set_xlabel('step')
fig.suptitle('常见的学习率调度曲线',fontsize=12,y=1.02)
save(fig,'lr-schedules.png')
