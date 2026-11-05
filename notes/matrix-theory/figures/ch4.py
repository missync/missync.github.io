from common import *
th=np.linspace(0,2*np.pi,800)
# 1 unit balls
fig,axs=plt.subplots(1,2,figsize=(12,5.2))
ax=axs[0]; plane(ax,1.6,ticks=True)
for p,c in [(1,C[0]),(1.5,C[4]),(2,C[2]),(4,C[3]),(np.inf,C[1])]:
    x=np.cos(th); y=np.sin(th)
    nrm=(np.abs(x)**p+np.abs(y)**p)**(1/p) if p!=np.inf else np.maximum(abs(x),abs(y))
    ax.plot(x/nrm,y/nrm,color=c,lw=2,label=f'p = {p if p!=np.inf else "∞"}')
ax.legend(fontsize=9,loc='upper right'); ax.set_title('ℓp 范数的单位球 {x : ‖x‖ₚ = 1}')
ax.text(-1.55,-1.5,'p 越大，单位球越“方”；p<1 时不再是凸集，不满足三角不等式',fontsize=9)
ax=axs[1]; plane(ax,1.6,ticks=True)
A=np.array([[2,0.8],[0.8,1]]); w,V=np.linalg.eigh(A); pts=V@np.diag(1/np.sqrt(w))@np.stack([np.cos(th),np.sin(th)])
ax.plot(np.cos(th),np.sin(th),color='#aaa',lw=1.5,ls='--',label='‖x‖₂ = 1')
ax.fill(pts[0],pts[1],color=C[0],alpha=0.15); ax.plot(pts[0],pts[1],color=C[0],lw=2,label='‖x‖_A = √(xᴴAx) = 1')
ax.legend(fontsize=9,loc='upper right'); ax.set_title('加权范数：正定 A 把单位圆压成椭圆')
save(fig,'ch4-unit-balls.png')

# 2 operator norms
A=np.array([[2,-1],[1,1.5]])
fig,axs=plt.subplots(1,3,figsize=(14.5,4.9))
U,S,Vt=np.linalg.svd(A)
for ax,(name,pts,nrm,val) in zip(axs,[
    ('2-范数（谱范数）',np.stack([np.cos(th),np.sin(th)]),lambda Y:np.sqrt((Y**2).sum(0)),S[0]),
    ('1-范数（列和范数）',np.array([[1,0,-1,0,1],[0,1,0,-1,0]],float),lambda Y:np.abs(Y).sum(0),np.abs(A).sum(0).max()),
    ('∞-范数（行和范数）',np.array([[1,1,-1,-1,1],[1,-1,-1,1,1]],float),lambda Y:np.abs(Y).max(0),np.abs(A).sum(1).max())]):
    plane(ax,3.4,ticks=True)
    ax.fill(pts[0],pts[1],color='#ccc',alpha=0.5,label='单位球')
    Y=A@pts; ax.fill(Y[0],Y[1],color=C[0],alpha=0.18); ax.plot(Y[0],Y[1],color=C[0],lw=2,label='A·单位球')
    # norm ball of radius val
    if '2' in name: B=val*np.stack([np.cos(th),np.sin(th)])
    elif '1-' in name: B=val*np.array([[1,0,-1,0,1],[0,1,0,-1,0]])
    else: B=val*np.array([[1,1,-1,-1,1],[1,-1,-1,1,1]])
    ax.plot(B[0],B[1],'--',color=C[1],lw=1.6,label=f'半径 {val:.3g} 的球')
    ax.legend(fontsize=8.5,loc='lower right'); ax.set_title(f'{name}：‖A‖ = {val:.3g}',fontsize=11)
fig.suptitle('算子范数 ‖A‖ = max ‖Ax‖/‖x‖：单位球的像被包住所需的最小半径（A = [[2, −1], [1, 1.5]]）',fontsize=12)
save(fig,'ch4-operator-norms.png')

# 3 Rayleigh quotient
A=np.array([[3,1],[1,2]]); w,V=np.linalg.eigh(A)
fig,axs=plt.subplots(1,2,figsize=(12,4.6),gridspec_kw={'width_ratios':[1.4,1]})
t=np.linspace(0,np.pi,400); X=np.stack([np.cos(t),np.sin(t)]); R=np.einsum('in,ij,jn->n',X,A,X)
ax=axs[0]; ax.plot(np.degrees(t),R,color=C[0],lw=2.2); ax.grid(True)
for i,col in [(0,C[2]),(1,C[1])]:
    ang=np.degrees(np.arctan2(V[1,i],V[0,i]))%180; ax.axhline(w[i],ls='--',color=col); ax.plot(ang,w[i],'o',color=col,ms=8)
    ax.text(3,w[i]+0.05,f'λ{2-i} = {w[i]:.3f}，在特征向量方向（{ang:.1f}°）取到',color=col,fontsize=9.5)
ax.set_xlabel('单位向量 x = (cos θ, sin θ) 的角度 θ（度）'); ax.set_ylabel('R(x) = xᴴAx / xᴴx'); ax.set_title('Rayleigh 商在单位圆上的取值，A = [[3,1],[1,2]]')
ax=axs[1]; plane(ax,1.5)
pts=np.stack([np.cos(th),np.sin(th)])
ax.plot(pts[0],pts[1],color='#aaa'); Rv=np.einsum('in,ij,jn->n',pts,A,pts)
sc=ax.scatter(pts[0],pts[1],c=Rv,cmap='viridis',s=6); fig.colorbar(sc,ax=ax,fraction=0.045,label='R(x)')
for i,col in [(0,C[2]),(1,C[1])]: vec(ax,V[:,i],c=col,lw=2.2)
ax.set_title('最大/最小值出现在两个正交的特征方向')
save(fig,'ch4-rayleigh.png')

# 4 Gershgorin
A=np.array([[10,1,0.5,0.2],[0.5,4+1j,1,0.3],[0.4,0.8,-3,0.5],[0.1,0.3,0.5,-1j*1+ -0.5]],complex)
ev=np.linalg.eigvals(A)
fig,axs=plt.subplots(1,2,figsize=(13,4.9))
for ax,(M,title) in zip(axs,[(A,'行盖尔圆：圆心 aᵢᵢ，半径 = 该行非对角元模之和'),(A.T,'列盖尔圆（Aᵀ 的行圆）：同样包含全部特征值')]):
    for i in range(4):
        c=M[i,i]; r=np.abs(M[i]).sum()-abs(c)
        ax.add_patch(mp.Circle((c.real,c.imag),r,fc=C[i],alpha=0.18,ec=C[i],lw=1.5)); ax.plot(c.real,c.imag,'+',color=C[i],ms=10)
        ax.text(c.real,c.imag+r+0.25,f'G{i+1}',color=C[i],ha='center')
    ax.plot(ev.real,ev.imag,'k*',ms=11,label='特征值')
    ax.axhline(0,color='#ccc',lw=0.8); ax.axvline(0,color='#ccc',lw=0.8)
    ax.set_aspect('equal'); ax.set_xlim(-6,13); ax.set_ylim(-4,4.5); ax.set_xlabel('Re'); ax.set_ylabel('Im'); ax.legend(loc='upper right'); ax.set_title(title,fontsize=11)
fig.suptitle('盖尔圆盘定理：特征值都落在圆盘的并集里；孤立的圆盘里恰有一个特征值',fontsize=12)
save(fig,'ch4-gershgorin.png')

# 5 matrix powers & Neumann
fig,axs=plt.subplots(1,2,figsize=(12.5,4.5))
k=np.arange(0,61)
ax=axs[0]
cases=[('正规阵 diag(0.9, 0.5)，ρ=0.9',np.diag([0.9,0.5]),C[2]),('非正规 [[0.9, 3],[0, 0.8]]，ρ=0.9',np.array([[0.9,3],[0,0.8]]),C[1]),('ρ=1.05 发散',np.array([[1.05,0.3],[0,0.7]]),C[3])]
for name,M,c in cases:
    ax.semilogy(k,[np.linalg.norm(np.linalg.matrix_power(M,i),2) for i in k],color=c,lw=2,label=name)
ax.axhline(1,color='#999',ls=':'); ax.grid(True); ax.legend(fontsize=9); ax.set_xlabel('k'); ax.set_ylabel('‖Aᵏ‖₂'); ax.set_title('Aᵏ → 0 ⇔ ρ(A) < 1（与 ‖A‖ 是否小于 1 无关）')
ax=axs[1]; M=np.array([[0.3,0.5,0.2],[0.1,0.4,0.2],[0.2,0.1,0.3]]); inv=np.linalg.inv(np.eye(3)-M)
S=np.zeros((3,3)); P=np.eye(3); err=[]
for i in range(40): S=S+P; P=P@M; err.append(np.linalg.norm(S-inv,2))
ax.semilogy(range(40),err,'o-',color=C[0],ms=3); ax.grid(True)
rho=max(abs(np.linalg.eigvals(M))); ax.semilogy(range(40),err[0]*rho**np.arange(40),'--',color='#999',label=f'参考斜率 ρ(A)ᵏ，ρ={rho:.3f}')
ax.legend(); ax.set_xlabel('部分和项数 N'); ax.set_ylabel('‖Σ Aᵏ − (I−A)⁻¹‖₂'); ax.set_title('Neumann 级数 I + A + A² + … → (I − A)⁻¹')
save(fig,'ch4-powers-neumann.png')

# 6 matrix exponential
fig,axs=plt.subplots(1,3,figsize=(14,4.7))
cases=[('A = [[0, 1], [−1, 0]]：eᵗᴬ 是旋转',np.array([[0,1],[-1,0]])),('A = [[−0.3, 1], [−1, −0.3]]：衰减螺旋',np.array([[-0.3,1],[-1,-0.3]])),('A = J₂(−0.5)：Jordan 块，退化结点',np.array([[-0.5,1],[0,-0.5]]))]
from math import factorial
def expm(M,t):
    w,V=np.linalg.eig(M)
    if abs(w[0]-w[1])<1e-9:  # jordan 2x2
        lam=w[0].real; N=M-lam*np.eye(2); return np.exp(lam*t)*(np.eye(2)+t*N)
    return (V@np.diag(np.exp(w*t))@np.linalg.inv(V)).real
for ax,(title,M) in zip(axs,cases):
    plane(ax,2.2)
    X,Y=np.meshgrid(np.linspace(-2,2,15),np.linspace(-2,2,15)); D=np.einsum('ij,jkl->ikl',M,np.stack([X,Y]))
    ax.quiver(X,Y,D[0],D[1],color='#c9d3e3',angles='xy',width=0.004)
    for x0 in [np.array([1.8,0]),np.array([0,1.8]),np.array([-1.5,-1.2]),np.array([1.2,-1.6])]:
        T=np.linspace(0,12,400); P=np.array([expm(M,t)@x0 for t in T]); ax.plot(P[:,0],P[:,1],color=C[0],lw=1.6); ax.plot(*x0,'o',color=C[1],ms=5)
    ax.set_title(title,fontsize=10.5)
fig.suptitle('x′(t) = Ax(t) 的解 x(t) = eᵗᴬx(0)：矩阵指数把“变化率”积分成轨迹',fontsize=12)
save(fig,'ch4-matrix-exponential.png')
