from style import *
import numpy as np
import matplotlib.patches as mp
plt.rcParams['axes.grid']=False
def box(ax,x,y,w,h,fc,ec='#333',text='',fs=10.5,lw=1.1,r=0.06):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle=f'round,pad=0,rounding_size={r}',fc=fc,ec=ec,lw=lw))
    if text: ax.text(x,y,text,ha='center',va='center',fontsize=fs)
def arr(ax,x1,y1,x2,y2,c='#333',lw=1.2,rad=0):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',color=c,lw=lw,shrinkA=0,shrinkB=0,mutation_scale=10,connectionstyle=f'arc3,rad={rad}'))
def clean(ax,eq=True):
    ax.set_xticks([]);ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    if eq: ax.set_aspect('equal')
toks=['我','是','北','航','的','学','生']

# 1. architecture
fig,ax=plt.subplots(figsize=(10,9.2))
ATT,FF,AN,EMB='#f4b6b0','#bcd6f2','#d6e3b5','#f2bcd6'
def addnorm_res(xc,y_from,y_to,side):
    xs=xc+side*1.25
    ax.plot([xc,xs,xs],[y_from,y_from,y_to],color='#333',lw=1.1); arr(ax,xs,y_to,xc+side*1.0,y_to)
# encoder
ex=0
ax.add_patch(mp.FancyBboxPatch((ex-1.45,1.75),2.9,4.55,boxstyle='round,pad=0,rounding_size=0.15',fc='#f6f6f6',ec='#999'))
box(ax,ex,0.4,2.0,0.5,EMB,text='输入嵌入'); ax.text(ex,-0.25,'源序列（例：我是北航的学生）',ha='center',fontsize=9.5)
ax.add_patch(mp.Circle((ex,1.15),0.14,fc='w',ec='#333')); ax.text(ex,1.15,'+',ha='center',va='center')
ax.text(ex-1.55,1.15,'位置编码 →',ha='right',va='center',fontsize=9.5); ax.plot([ex-1.5,ex-0.14],[1.15,1.15],color='#333',lw=1.1)
arr(ax,ex,0.65,ex,1.01); arr(ax,ex,1.29,ex,2.25)
box(ax,ex,2.6,2.0,0.7,ATT,text='多头自注意力'); box(ax,ex,3.55,2.0,0.42,AN,text='Add & Norm')
box(ax,ex,4.5,2.0,0.6,FF,text='前馈网络 FFN'); box(ax,ex,5.5,2.0,0.42,AN,text='Add & Norm')
arr(ax,ex,2.95,ex,3.34); arr(ax,ex,3.76,ex,4.2); arr(ax,ex,4.8,ex,5.29)
addnorm_res(ex,2.0,3.55,-1); addnorm_res(ex,4.0,5.5,-1)
ax.text(ex-1.75,4.0,'N×',fontsize=12,ha='right')
ax.text(ex,6.6,'编码器 Encoder',ha='center',fontsize=12,fontweight='bold')
# decoder
dx0=5
ax.add_patch(mp.FancyBboxPatch((dx0-1.45,1.75),2.9,6.15,boxstyle='round,pad=0,rounding_size=0.15',fc='#f6f6f6',ec='#999'))
box(ax,dx0,0.4,2.0,0.5,EMB,text='输出嵌入'); ax.text(dx0,-0.25,'目标序列右移一位（<START> I am ...）',ha='center',fontsize=9.5)
ax.add_patch(mp.Circle((dx0,1.15),0.14,fc='w',ec='#333')); ax.text(dx0,1.15,'+',ha='center',va='center')
ax.text(dx0+1.55,1.15,'← 位置编码',ha='left',va='center',fontsize=9.5); ax.plot([dx0+1.5,dx0+0.14],[1.15,1.15],color='#333',lw=1.1)
arr(ax,dx0,0.65,dx0,1.01); arr(ax,dx0,1.29,dx0,2.2)
box(ax,dx0,2.6,2.0,0.8,ATT,text='带掩码的\n多头自注意力'); box(ax,dx0,3.55,2.0,0.42,AN,text='Add & Norm')
box(ax,dx0,4.6,2.0,0.8,'#f0a49c',text='多头交叉注意力'); box(ax,dx0,5.55,2.0,0.42,AN,text='Add & Norm')
box(ax,dx0,6.5,2.0,0.6,FF,text='前馈网络 FFN'); box(ax,dx0,7.45,2.0,0.42,AN,text='Add & Norm')
arr(ax,dx0,3.0,dx0,3.34); arr(ax,dx0,3.76,dx0,4.2); arr(ax,dx0,5.0,dx0,5.34); arr(ax,dx0,5.76,dx0,6.2); arr(ax,dx0,6.8,dx0,7.24)
addnorm_res(dx0,1.95,3.55,1); addnorm_res(dx0,3.95,5.55,1); addnorm_res(dx0,5.95,7.45,1)
ax.text(dx0+1.75,4.8,'×N',fontsize=12)
box(ax,dx0,8.4,1.6,0.42,'#fbf3a6',text='Linear'); box(ax,dx0,9.05,1.6,0.42,'#d9cbb8',text='Softmax')
arr(ax,dx0,7.66,dx0,8.19); arr(ax,dx0,8.61,dx0,8.84); arr(ax,dx0,9.26,dx0,9.6); ax.text(dx0,9.68,'下一个词元的概率',ha='center',fontsize=10)
ax.text(dx0,8.0-0.0+2.1,'',fontsize=1)
ax.text(dx0-2.1,8.4,'解码器 Decoder',ha='center',fontsize=12,fontweight='bold')
# cross connection
ax.plot([ex,ex,2.7,2.7],[5.71,6.2,6.2,4.4],color='#c0392b',lw=1.6); arr(ax,2.7,4.4,dx0-1.0,4.4,c='#c0392b',lw=1.6)
ax.text(2.75,6.3,'编码器输出\n提供 K、V',fontsize=9.5,color='#c0392b',ha='center',va='bottom')
ax.text(dx0+0.3,4.05,'Q 来自解码器',fontsize=8,color='#555',ha='center') if False else None
ax.set_xlim(-2.6,8.2); ax.set_ylim(-0.6,10.0); clean(ax)
save(fig,'transformer-architecture.png')

# 2. attention step by step
d=4
rng=np.random.default_rng(3)
S=np.array([[6,1,1,1,0,1,1],[2,5,1,1,2,3,1],[1,1,6,6,0,2,1],[1,1,6,6,0,2,1],[1,0,3,3,4,3,3],[2,1,2,2,1,6,6],[2,1,2,2,1,6,6]],float)
S=S+rng.normal(0,0.6,S.shape); S=np.round(S*2,1)
def softmax(x): e=np.exp(x-x.max(1,keepdims=True)); return e/e.sum(1,keepdims=True)
A=softmax(S/np.sqrt(d))
M=np.triu(np.ones((7,7)),1)
Am=softmax(np.where(M>0,-np.inf,S/np.sqrt(d)))
fig,axs=plt.subplots(1,3,figsize=(15,5.0))
for ax,mat,title,cmap,fmt in [(axs[0],S,'① 相似度 $S=QK^{\\top}$',"Oranges",'{:.1f}'),(axs[1],A,'② 缩放 + 按行 softmax：$A=\\mathrm{softmax}(S/\\sqrt{d_k})$','Reds','{:.2f}'),(axs[2],Am,'③ 解码器：上三角置 $-\\infty$ 后再 softmax','Reds','{:.2f}')]:
    ax.imshow(mat if mat is S else mat,cmap=cmap,vmin=(S.min() if mat is S else 0),vmax=(S.max() if mat is S else 1))
    for i in range(7):
        for j in range(7):
            v=mat[i,j]; masked = (mat is Am and M[i,j]>0)
            ax.text(j,i,'−∞' if masked else fmt.format(v),ha='center',va='center',fontsize=9,color='#999' if masked else ('w' if (v>(0.55 if mat is not S else 9)) else 'k'))
    ax.set_xticks(range(7)); ax.set_yticks(range(7)); ax.set_xticklabels(toks); ax.set_yticklabels(toks)
    ax.set_xlabel('Key（被关注的词元）'); ax.set_ylabel('Query（当前词元）'); ax.set_title(title,fontsize=11)
    ax.tick_params(length=0)
fig.suptitle('“我是北航的学生”的注意力矩阵（数值为示意）：每一行是一个词元对全句的注意力分配，行和为 1',fontsize=12,y=1.0)
save(fig,'attention-map.png')

# 3. why scale by sqrt(dk)
rng=np.random.default_rng(0)
ds=[4,16,64,256,1024]; n=16; trials=400
mx_raw=[];mx_sc=[];std=[]
for dk in ds:
    q=rng.standard_normal((trials,1,dk)); k=rng.standard_normal((trials,n,dk))
    s=(q*k).sum(-1); std.append(s.std())
    mx_raw.append(softmax(s).max(1).mean()); mx_sc.append(softmax(s/np.sqrt(dk)).max(1).mean())
fig,axs=plt.subplots(1,2,figsize=(11.5,3.9))
ax=axs[0]; ax.plot(ds,std,'o-',color=C[1],lw=2,label='实测'); ax.plot(ds,np.sqrt(ds),'--',color='#555',label='$\\sqrt{d_k}$')
ax.set_xscale('log',base=2); ax.set_xlabel('$d_k$'); ax.set_title('点积 $q\\cdot k$ 的标准差随维度增长'); ax.legend(); ax.grid(True)
ax=axs[1]; ax.plot(ds,mx_raw,'o-',color=C[3],lw=2,label='不缩放：softmax$(QK^{\\top})$'); ax.plot(ds,mx_sc,'o-',color=C[0],lw=2,label='缩放：softmax$(QK^{\\top}/\\sqrt{d_k})$')
ax.axhline(1/n,ls=':',color='#999'); ax.text(4.2,1/n+0.02,'均匀分配 1/16',fontsize=9,color='#777')
ax.set_xscale('log',base=2); ax.set_ylim(0,1.05); ax.set_xlabel('$d_k$'); ax.set_ylabel('最大注意力权重（平均）'); ax.set_title('16 个 key 时，softmax 的“尖锐”程度'); ax.legend(fontsize=9); ax.grid(True)
fig.suptitle('q、k 各分量独立同分布 N(0,1)：不缩放时 softmax 几乎变成 one-hot，梯度很小',fontsize=12,y=1.03)
save(fig,'attention-scaling.png')

# 4. multi-head shapes
fig,ax=plt.subplots(figsize=(14,4.6))
def mat(x,y,r,c,col,label,cell=0.18,sub=''):
    for i in range(r):
        for j in range(c):
            ax.add_patch(mp.Rectangle((x+j*cell,y-(i+1)*cell),cell*0.92,cell*0.92,fc=col,ec='none'))
    ax.text(x+c*cell/2,y+0.12,label,ha='center',va='bottom',fontsize=10)
    ax.text(x+c*cell/2,y-r*cell-0.1,sub or f'{r}×{c}',ha='center',va='top',fontsize=9,color='#555')
    return x+c*cell
mat(0,1.9,7,5,'#d9a8e8','输入 X')
hc=['#f08a6b','#f6b8b0','#f2c78a']
for h in range(3):
    y=3.6-h*1.8
    arr(ax,1.05,1.25,1.6,y-0.45,c='#888')
    ax.text(1.65,y-0.3,f'头 {h+1}',fontsize=9.5,color='#444')
    x=mat(2.3,y,7,3,'#fbd38d','$Q_{%d}$'%(h+1),cell=0.13,sub=' ')
    x=mat(2.85,y,7,3,'#8fc5f4','$K_{%d}$'%(h+1),cell=0.13,sub='各 7×3')
    x=mat(3.4,y,7,3,'#a9dcb0','$V_{%d}$'%(h+1),cell=0.13,sub=' ')
    arr(ax,3.85,y-0.45,4.35,y-0.45,c='#888')
    mat(4.45,y,7,7,'#f3a29a','$A_{%d}$'%(h+1),cell=0.13,sub='7×7')
    arr(ax,5.42,y-0.45,5.9,y-0.45,c='#888')
    mat(6.0,y,7,3,hc[h],'$Z_{%d}=A_{%d}V_{%d}$'%(h+1,h+1,h+1),cell=0.13,sub='7×3')
    arr(ax,6.45,y-0.45,7.2,1.3,c='#888')
cx=7.3
for h in range(3): mat(cx+h*3*0.18,1.9,7,3,hc[h],'',sub=' ')
ax.text(cx+0.81,2.02,'拼接 Concat',ha='center',fontsize=10); ax.text(cx+0.81,0.55,'7×9',ha='center',va='top',fontsize=9,color='#555')
ax.text(9.1,1.25,'×',fontsize=18,ha='center',va='center')
mat(9.35,2.2,9,5,'#9fb8dd','$W^O$',sub='9×5')
ax.text(10.5,1.25,'=',fontsize=18,ha='center',va='center')
mat(10.75,1.9,7,5,'#e98d82','输出',sub='7×5（与输入同形）')
ax.set_xlim(-0.2,11.8); ax.set_ylim(-1.9,4.1); clean(ax)
ax.set_title('多头自注意力的形状变化：7 个词元，$d_{model}=5$，3 个头，每头 $d_k=d_v=3$',fontsize=12)
save(fig,'multihead-shapes.png')

# 5. positional encoding
def pe(L,dm):
    P=np.zeros((L,dm)); pos=np.arange(L)[:,None]; i=np.arange(0,dm,2)[None]
    P[:,0::2]=np.sin(pos/10000**(i/dm)); P[:,1::2]=np.cos(pos/10000**(i/dm)); return P
P=pe(64,128)
fig,axs=plt.subplots(1,2,figsize=(13,4.3),gridspec_kw={'width_ratios':[1.25,1]})
ax=axs[0]; im=ax.imshow(P,cmap='RdBu_r',aspect='auto',vmin=-1,vmax=1); fig.colorbar(im,ax=ax,fraction=0.04)
ax.set_xlabel('嵌入维度下标'); ax.set_ylabel('位置 pos'); ax.set_title('正弦位置编码矩阵（64 个位置 × 128 维）')
ax=axs[1]; x=np.linspace(0,20,400)
for k,(i,c) in enumerate([(0,C[0]),(4,C[2]),(12,C[3])]):
    ax.plot(x,np.sin(x/10000**(2*i/128))+k*2.4,color=c,lw=1.8)
    ax.plot(np.arange(21),np.sin(np.arange(21)/10000**(2*i/128))+k*2.4,'o',color=c,ms=3.5)
    ax.text(20.4,k*2.4,f'第 {2*i} 维',va='center',fontsize=9.5,color=c)
ax.set_yticks([]); ax.set_xlabel('位置 pos'); ax.set_xlim(0,23); ax.set_title('低维变化快、高维变化慢：像多根频率不同的“指针”')
save(fig,'positional-encoding.png')

# 6. masks
fig,axs=plt.subplots(1,3,figsize=(14.5,4.6),gridspec_kw={'wspace':0.45})
L=6; pad_src=[0,0,0,0,1,1]; pad_tgt=[0,0,0,0,0,1]
def show(ax,allowed,title,xl,yl,xt,yt):
    ax.imshow(allowed,cmap='Greens',vmin=-0.3,vmax=1.3)
    for i in range(allowed.shape[0]):
        for j in range(allowed.shape[1]):
            if not allowed[i,j]: ax.text(j,i,'×',ha='center',va='center',color='#c0392b',fontsize=12)
    ax.set_xticks(range(len(xt))); ax.set_xticklabels(xt,fontsize=9); ax.set_yticks(range(len(yt))); ax.set_yticklabels(yt,fontsize=9)
    ax.set_xlabel(xl); ax.set_ylabel(yl); ax.set_title(title,fontsize=11); ax.tick_params(length=0)
src=['我','是','学','生','PAD','PAD']; tgt=['<S>','I','am','a','student','PAD']
show(axs[0],np.array([[1-pad_src[j] for j in range(L)] for i in range(L)]),'编码器自注意力：只屏蔽 padding','Key（源序列）','Query（源序列）',src,src)
show(axs[1],np.array([[(j<=i)*(1-pad_tgt[j]) for j in range(L)] for i in range(L)]),'解码器自注意力：因果 + padding','Key（目标序列）','Query（目标序列）',tgt,tgt)
show(axs[2],np.array([[1-pad_src[j] for j in range(L)] for i in range(L)]),'交叉注意力：屏蔽源序列 padding','Key/Value（编码器输出）','Query（解码器）',src,tgt)
fig.suptitle('绿色 = 允许关注（M=0），× = 屏蔽（M=−∞）；A = softmax(QKᵀ/√dₖ + M)',fontsize=12,y=1.0)
save(fig,'attention-masks.png')
