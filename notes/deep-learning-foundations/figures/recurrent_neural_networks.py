from style import *
import numpy as np
import matplotlib.patches as mp
plt.rcParams['axes.grid']=False

def box(ax,x,y,w,h,fc,ec='none',text='',fs=11,tc='k',r=0.08):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle=f'round,pad=0,rounding_size={r}',fc=fc,ec=ec,lw=1.2))
    if text: ax.text(x,y,text,ha='center',va='center',fontsize=fs,color=tc)
def arr(ax,x1,y1,x2,y2,c='#555',lw=1.4,ls='-'):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',color=c,lw=lw,ls=ls,shrinkA=0,shrinkB=0,mutation_scale=11))
def clean(ax):
    ax.set_xticks([]);ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_aspect('equal')
XIN,HID,OUT='#cfe0fa','#cdebd6','#ead9f7'

# 1. sequence task patterns
fig,axs=plt.subplots(1,4,figsize=(14,3.9))
pats=[('一对多 one-to-many','图像描述：一张图 → 一句话',[1,0,0,0],[0,1,1,1]),
      ('多对一 many-to-one','情感分类：一句话 → 一个标签',[1,1,1,1],[0,0,0,1]),
      ('多对多（同步）','逐帧标注 / 字符级语言模型',[1,1,1,1],[1,1,1,1]),
      ('多对多（编码-解码）','机器翻译、视频描述',[1,1,1,0,0],[0,0,0,1,1])]
for ax,(t,sub,ins,outs) in zip(axs,pats):
    n=len(ins); off=(5-n)*0.55
    for i in range(n):
        x=i*1.1+off
        box(ax,x,1,0.8,0.6,HID)
        if ins[i]: box(ax,x,0,0.6,0.45,XIN,text='x'); arr(ax,x,0.23,x,0.7)
        if outs[i]: box(ax,x,2,0.6,0.45,OUT,text='y'); arr(ax,x,1.3,x,1.77)
        if i<n-1: arr(ax,x+0.4,1,x+0.7,1,c='#2b8a4b',lw=1.8)
    ax.set_xlim(-0.6,5*1.1-0.5); ax.set_ylim(-0.6,2.6); clean(ax)
    ax.set_title(t); ax.text(off+(n-1)*0.55,-0.55,sub,ha='center',va='top',fontsize=10,color='#444')
fig.suptitle('按输入、输出是否为序列划分的几类任务（绿色箭头 = 隐藏状态沿时间传递）',fontsize=12,y=1.03)
save(fig,'rnn-sequence-tasks.png')

# 2. unrolled RNN with char LM
fig,ax=plt.subplots(figsize=(12,5.2))
ins=['想','开','直','升']; tg=['开','直','升','机']
# folded
box(ax,0,1.5,1.0,0.7,HID,text='RNN',fs=12); box(ax,0,0,0.6,0.5,XIN,text='$x_t$'); box(ax,0,3,0.6,0.5,OUT,text='$\\hat y_t$')
arr(ax,0,0.25,0,1.15); arr(ax,0,1.85,0,2.75)
ax.add_patch(mp.FancyArrowPatch((0.5,1.65),(0.5,1.35),connectionstyle='arc3,rad=-2.2',arrowstyle='-|>',color='#2b8a4b',lw=1.8,mutation_scale=11))
ax.text(1.05,1.5,'$h_t$',fontsize=12,color='#2b8a4b',va='center')
ax.text(1.75,1.5,'=',fontsize=26,va='center',ha='center')
for i in range(4):
    x=3+i*2.3
    box(ax,x,1.5,1.2,0.7,HID,text=f'$h_{i}$')
    box(ax,x,0,0.6,0.5,XIN,text=ins[i],fs=13); arr(ax,x,0.25,x,1.15); ax.text(x+0.08,0.65,'$W_{xh}$',fontsize=9)
    box(ax,x,3,0.6,0.5,OUT,text=f'$\\hat y_{i}$'); arr(ax,x,1.85,x,2.75); ax.text(x+0.08,2.25,'$W_{hy}$',fontsize=9)
    box(ax,x,4.0,0.6,0.42,'#fde3d0',text=f'$L_{i}$'); arr(ax,x,3.25,x,3.79)
    ax.text(x,3.55,f'目标“{tg[i]}”',fontsize=8.5,ha='left',va='center',color='#a3460f',x=x+0.36) if False else ax.text(x+0.38,4.0,f'目标:{tg[i]}',fontsize=9,va='center',color='#a3460f')
    if i<3: arr(ax,x+0.6,1.5,x+1.7,1.5,c='#2b8a4b',lw=1.8); ax.text(x+1.15,1.62,'$W_{hh}$',fontsize=9,ha='center')
arr(ax,1.95,1.5,2.4,1.5,c='#2b8a4b',lw=1.8); ax.text(2.0,1.65,'$h_{-1}$',fontsize=9)
box(ax,6.45,5.1,2.4,0.55,'#f6b78f',text='总损失 $L=L_0+L_1+L_2+L_3$',fs=10.5)
for i in range(4): arr(ax,3+i*2.3,4.21,6.45+(i-1.5)*0.5,4.82,c='#e8743b',lw=1)
ax.annotate('',xy=(3,-0.75),xytext=(10.5,-0.75),arrowprops=dict(arrowstyle='-|>',color='#d62728',lw=2))
ax.text(6.75,-0.95,'反向传播沿时间逆序流动（BPTT），同一组 $W_{xh},W_{hh},W_{hy}$ 的梯度在各时间步累加',color='#d62728',ha='center',va='top',fontsize=10.5)
ax.set_xlim(-0.8,11.6); ax.set_ylim(-1.4,5.5); clean(ax)
ax.set_title('左：带环的紧凑画法；右：按时间展开的计算图（字符级语言模型“想开直升机”）',fontsize=12)
save(fig,'rnn-unrolled.png')

# 3. gradient flow simulation
rng=np.random.default_rng(1); n=64; T=60
def vanilla(rho):
    W=rng.standard_normal((n,n))/np.sqrt(n); W*=rho/np.max(np.abs(np.linalg.eigvals(W)))
    U=rng.standard_normal((n,n))/np.sqrt(n)*0.5
    h=np.zeros(n); J=np.eye(n); norms=[1]
    for t in range(T):
        h=np.tanh(W@h+U@rng.standard_normal(n)); D=np.diag(1-h**2)
        J=D@W@J; norms.append(np.linalg.norm(J,2))
    return norms
def lstm_path(lo,hi):
    f=rng.uniform(lo,hi,(T,n)); return [1]+list(np.cumprod(f.mean(1)))
fig,axs=plt.subplots(1,2,figsize=(12,4.2))
ax=axs[0]; k=np.arange(9)
for g,c,l in [(0.5,C[0],'每层 ×0.5'),(1.0,C[2],'每层 ×1.0'),(1.5,C[1],'每层 ×1.5')]:
    ax.plot(k,g**k,'o-',color=c,label=l,lw=2)
ax.set_title('玩具模型：同一因子反复相乘'); ax.set_xlabel('连乘次数'); ax.set_ylabel('梯度相对尺度'); ax.legend(); ax.grid(True)
ax.text(8,1.5**8,f'{1.5**8:.1f}',ha='right',va='bottom',color=C[1])
ax=axs[1]
for rho,c in [(0.9,C[0]),(1.5,C[3]),(3.0,C[1])]:
    ax.semilogy(vanilla(rho),color=c,lw=2,label=f'普通 RNN，$W_{{hh}}$ 谱半径 {rho}')
ax.semilogy(lstm_path(0.97,1.0),color=C[2],lw=2.5,ls='--',label='LSTM 细胞状态路径，$f_t\\in[0.97,1]$')
ax.set_xlabel('回传的时间步数 $T-t$'); ax.set_ylabel('$\\|\\partial h_T/\\partial h_t\\|$（对数轴）'); ax.grid(True)
ax.set_title('随机初始化的 64 维 RNN：雅可比连乘的范数'); ax.legend(fontsize=9)
save(fig,'rnn-gradient-flow.png')

# 4. word embedding analogy (illustrative)
fig,axs=plt.subplots(1,2,figsize=(11.5,4.3),gridspec_kw={'width_ratios':[1,1.2]})
ax=axs[0]; V=8; tokens=['apple','car','cat','dog']
M=np.zeros((4,V)); 
for i,j in enumerate([2,5,0,6]): M[i,j]=1
ax.imshow(M,cmap='Blues',vmin=0,vmax=1.3)
for i in range(4):
    for j in range(V): ax.text(j,i,int(M[i,j]),ha='center',va='center',fontsize=9,color='w' if M[i,j] else '#888')
ax.set_yticks(range(4)); ax.set_yticklabels(tokens); ax.set_xticks(range(V)); ax.set_xticklabels([f'{j}' for j in range(V)],fontsize=8)
ax.set_xlabel('词表位置（V 维）'); ax.set_title('One-hot：任意两个词的余弦相似度都是 0')
ax=axs[1]
P={'man':(1,1),'woman':(1.4,2.6),'king':(3.6,1.4),'queen':(4.0,3.0),'apple':(0.6,4.3),'pear':(1.2,4.6),'car':(4.6,0.2)}
for w,(x,y) in P.items(): ax.plot(x,y,'o',color=C[0] if w in('man','woman','king','queen') else '#999',ms=7); ax.text(x+0.1,y+0.12,w,fontsize=11)
for a,b,c in [('man','woman',C[3]),('king','queen',C[3]),('man','king',C[2]),('woman','queen',C[2])]:
    ax.annotate('',xy=P[b],xytext=P[a],arrowprops=dict(arrowstyle='-|>',color=c,lw=1.8,shrinkA=5,shrinkB=5))
ax.text(1.5,1.7,'性别方向',color=C[3],fontsize=9); ax.text(2.1,0.95,'“王室”方向',color=C[2],fontsize=9)
ax.set_xlim(0,5.3); ax.set_ylim(-0.2,5.1); ax.set_xticks([]); ax.set_yticks([]); ax.grid(True)
ax.set_title('稠密嵌入（示意）：king − man + woman ≈ queen')
save(fig,'word-embeddings.png')
