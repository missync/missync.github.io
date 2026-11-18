from common import *
def heat(ax,M,title,cmap='RdBu_r',vmax=None,fmt='{:.2g}',fs=9):
    vmax=vmax or np.abs(M).max()
    ax.imshow(M,cmap=cmap,vmin=-vmax,vmax=vmax)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v=M[i,j]; ax.text(j,i,'0' if abs(v)<1e-12 else fmt.format(v),ha='center',va='center',fontsize=fs,color='#bbb' if abs(v)<1e-12 else 'k')
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title(title,fontsize=11)
# 1 LU & full-rank
A=np.array([[2,1,1,0],[4,3,3,1],[8,7,9,5],[6,7,9,8]],float)
n=4; L=np.eye(n); U=A.copy()
for k in range(n-1):
    for i in range(k+1,n):
        L[i,k]=U[i,k]/U[k,k]; U[i]-=L[i,k]*U[k]
B=np.array([[1,2,1,3,4],[2,4,0,2,2],[3,6,1,5,6],[1,2,-1,-1,-2]],float)  # rank 2
F=B[:,[0,2]]; G=np.linalg.lstsq(F,B,rcond=None)[0]
fig,axs=plt.subplots(2,3,figsize=(12.5,7.4),gridspec_kw={'width_ratios':[1,1,1]})
heat(axs[0,0],A,'A（4×4）',fmt='{:.0f}'); heat(axs[0,1],L,'L：单位下三角（消元乘数）',fmt='{:.0f}'); heat(axs[0,2],U,'U：上三角（消元结果）',fmt='{:.0f}')
heat(axs[1,0],B,'B（4×5，秩 2）',fmt='{:.0f}'); heat(axs[1,1],F,'F：B 的第 1、3 列（4×2，列满秩）',fmt='{:.0f}'); heat(axs[1,2],G,'G：在 F 下的坐标（2×5，行满秩）',fmt='{:.0f}')
fig.text(0.355,0.73,'=',fontsize=24,ha='center'); fig.text(0.64,0.73,'×',fontsize=20,ha='center')
fig.text(0.355,0.29,'=',fontsize=24,ha='center'); fig.text(0.64,0.29,'×',fontsize=20,ha='center')
fig.suptitle('上：A = LU，L 记录 Gauss 消元的乘数；下：满秩分解 B = FG，F 取主元列，G 是各列在主元列下的坐标',fontsize=12)
save(fig,'ch3-lu-fullrank.png')

# 2 QR geometry
fig,axs=plt.subplots(1,2,figsize=(12,5))
ax=axs[0]; plane(ax,3.2)
a1=np.array([2.4,0.8]); a2=np.array([1.2,2.4])
q1=a1/np.linalg.norm(a1); r11=np.linalg.norm(a1); r12=q1@a2; u=a2-r12*q1; r22=np.linalg.norm(u); q2=u/r22
vec(ax,a1,c='#9db9ef',label='a₁',lw=2); vec(ax,a2,c='#9db9ef',label='a₂',lw=2)
vec(ax,q1,c=C[0],label='q₁',lw=2.6,off=(-0.1,0.15)); vec(ax,q2,c=C[1],label='q₂',lw=2.6,off=(-0.4,0))
ax.plot(*zip(r12*q1,a2),'--',color=C[1]); ax.plot(*zip((0,0),r12*q1),color=C[2],lw=4,alpha=0.5)
ax.text(*(r12*q1*0.5+[0.2,-0.75]),'r₁₂ = q₁ᴴa₂',color=C[2],fontsize=10); ax.text(*((r12*q1+a2)/2+[0.1,0]),'r₂₂ = ‖a₂ − r₁₂q₁‖',color=C[1],fontsize=10)
ax.text(-3,-2.9,f'R = [[{r11:.2f}, {r12:.2f}], [0, {r22:.2f}]]\nr₁₁ = ‖a₁‖；R 上三角，因为 a₁ 只用到 q₁',fontsize=10)
ax.set_title('QR = Gram–Schmidt 的矩阵形式：A = [a₁ a₂] = [q₁ q₂] R')
# 3 QR algorithm
M=np.array([[4,1,1],[1,3,1],[1,1,2]],float); Ak=M.copy(); sub=[];diag=[]
for k in range(25):
    Q,R=np.linalg.qr(Ak); Ak=R@Q; sub.append([abs(Ak[1,0]),abs(Ak[2,1])]); diag.append(np.diag(Ak).copy())
sub=np.array(sub); diag=np.array(diag); ev=np.sort(np.linalg.eigvalsh(M))[::-1]
ax=axs[1]; ax.semilogy(range(1,26),sub[:,0],'o-',color=C[0],ms=3,label='|a₂₁⁽ᵏ⁾|'); ax.semilogy(range(1,26),sub[:,1],'o-',color=C[1],ms=3,label='|a₃₂⁽ᵏ⁾|')
ax.grid(True); ax.set_xlabel('迭代次数 k'); ax.legend(loc='upper right')
ax.set_title('QR 迭代 Aₖ = QₖRₖ, Aₖ₊₁ = RₖQₖ：次对角元趋于 0')
ax.text(1,2e-8,'对角元 → 特征值\n'+', '.join(f'{d:.4f}' for d in diag[-1])+'\n精确值 '+', '.join(f'{e:.4f}' for e in ev),fontsize=9)
save(fig,'ch3-qr.png')

# 4 diagonalization dynamics
A=np.array([[0.9,0.2],[0.1,0.8]]); w,V=np.linalg.eig(A); w,V=w.real,V.real; idx=np.argsort(-w); w=w[idx]; V=V[:,idx]
fig,axs=plt.subplots(1,2,figsize=(12.5,5.2))
ax=axs[0]; plane(ax,3)
for i,col in [(0,C[1]),(1,C[2])]:
    v=V[:,i]/np.linalg.norm(V[:,i]); ax.plot(*zip(-3.5*v,3.5*v),'--',color=col,lw=1.2); ax.text(*(2.5*v*np.sign(v[0] or 1)+[0.1,0.1]),f'v{i+1}，λ{i+1}={w[i]:.1f}',color=col,fontsize=10)
rng=np.random.default_rng(2)
for x0 in [np.array([-2.5,2.5]),np.array([2.6,-1.2]),np.array([-1,-2.6]),np.array([2.4,2.2]),np.array([0.6,2.8])]:
    P=[x0]; 
    for k in range(25): P.append(A@P[-1])
    P=np.array(P); ax.plot(P[:,0],P[:,1],'.-',color=C[0],ms=4,lw=0.8)
ax.set_title('x_{k+1} = A x_k：λ₂ 分量逐步衰减，各点沿 v₂ 方向落到 v₁ 直线上')
ax.text(-2.9,-2.85,'A = [[0.9, 0.2], [0.1, 0.8]] = PΛP⁻¹\nAᵏx₀ = c₁·1ᵏ·v₁ + c₂(0.7)ᵏv₂ → c₁v₁',fontsize=9.5)
ax=axs[1]; plane(ax,3)
Ainv=np.linalg.inv(V)
for k in range(-3,4):
    for line in ([[k,k],[-3,3]],[[-3,3],[k,k]]):
        Pq=V@np.array(line); ax.plot(Pq[0],Pq[1],color='#e1e7f2',lw=0.9,zorder=0)
x0=np.array([-0.8,2.6]); c=Ainv@x0
for k,col in [(0,'#9db9ef'),(3,C[0]),(6,'#173f8f')]:
    xk=V@(w**k*c); vec(ax,xk,c=col,label=f'A^{k}x₀' if k else 'x₀',fs=10)
    p1=V[:,0]*w[0]**k*c[0]; ax.plot(*zip(p1,xk),':',color=col)
ax.set_title('在特征基坐标网格里看：每个坐标各自乘 λᵢ，互不干扰')
save(fig,'ch3-diagonalization.png')

# 5 spectral decomposition
A=np.array([[2,1],[0,0.5]]); w,V=np.linalg.eig(A); w,V=w.real,V.real; Vi=np.linalg.inv(V)
P1=np.outer(V[:,0],Vi[0]); P2=np.outer(V[:,1],Vi[1])
fig,ax=plt.subplots(figsize=(7,6)); plane(ax,3.4)
for i,col in [(0,C[0]),(1,C[2])]:
    v=V[:,i]/np.linalg.norm(V[:,i]); ax.plot(*zip(-4*v,4*v),color=col,lw=1.5,alpha=0.6); ax.text(*(2.9*v*np.sign(v[0]+v[1])+[0.05,0.15]),f'特征方向 λ={w[i]:g}',color=col)
x=np.array([0.6,1.6]); p1=P1@x; p2=P2@x
vec(ax,x,c='#555',label='x'); vec(ax,p1,c=C[0],label='P₁x',off=(0.05,-0.3)); vec(ax,p2,c=C[2],label='P₂x',off=(-0.6,0.05))
ax.plot(*zip(p1,x),':',color='#888'); ax.plot(*zip(p2,x),':',color='#888')
y=A@x; vec(ax,w[0]*p1,c=C[0],lw=1.2,alpha=0.6); vec(ax,w[1]*p2,c=C[2],lw=1.2,alpha=0.6); vec(ax,y,c=C[1],label='Ax = 2P₁x + 0.5P₂x',lw=2.6)
ax.plot(*zip(w[0]*p1,y),':',color=C[1]); ax.plot(*zip(w[1]*p2,y),':',color=C[1])
ax.set_title('谱分解 A = λ₁P₁ + λ₂P₂：先沿特征方向拆分，再各自伸缩')
ax.text(-3.3,-3.25,'P₁ + P₂ = I，PᵢPⱼ = 0（i≠j），Pᵢ² = Pᵢ\nA 不对称时 Pᵢ 是斜投影；Hermite 时为正交投影',fontsize=9.5)
save(fig,'ch3-spectral.png')

# 6 Jordan block
fig,axs=plt.subplots(1,3,figsize=(14,4.6))
for ax,(A,title) in zip(axs[:2],[(np.diag([1.4,1.4]),'1.4·I：每个方向都是特征方向'),(np.array([[1.4,0.7],[0,1.4]]),'Jordan 块 J₂(1.4)：只有 e₁ 方向不转')]):
    plane(ax,2.4); th=np.linspace(0,2*np.pi,16)[:-1]
    for t in th:
        x=np.array([np.cos(t),np.sin(t)]); y=A@x
        ax.annotate('',xy=y,xytext=x,arrowprops=dict(arrowstyle='-|>',color=C[0] if abs(x[0]*y[1]-x[1]*y[0])<1e-9 else '#9db9ef',lw=1.3,mutation_scale=9))
        ax.plot(*x,'o',color='#999',ms=3)
    if A[0,1]: ax.plot([-2.4,2.4],[0,0],color=C[1],lw=2.5,alpha=0.5); ax.text(-2.35,-0.35,'唯一特征方向 e₁',color=C[1])
    ax.set_title(title,fontsize=11)
ax=axs[2]; k=np.arange(1,41); lam=0.9
ax.semilogy(k,lam**k,color=C[2],lw=2,label='对角阵：λᵏ')
ax.semilogy(k,np.maximum(k*lam**(k-1),1e-6),color=C[1],lw=2,label='J₂(λ)ᵏ 右上角：kλᵏ⁻¹')
ax.semilogy(k[1:],(k*(k-1)/2*lam**(k-2))[1:],color=C[3],lw=2,label='J₃(λ)ᵏ 右上角：C(k,2)λᵏ⁻²')
ax.grid(True); ax.legend(fontsize=9); ax.set_xlabel('k'); ax.set_title('λ = 0.9：Jordan 块的幂先增大后衰减')
save(fig,'ch3-jordan.png')
