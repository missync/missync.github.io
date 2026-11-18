from common import *
# 1 subspaces
fig=plt.figure(figsize=(14,4.6))
ax=fig.add_subplot(1,3,1); plane(ax)
t=np.linspace(-3,3,2)
ax.plot(t,0.5*t,color=C[0],lw=2.5,label='W = {(x, x/2)}：过原点')
ax.plot(t,0.5*t+1,color=C[1],lw=2.5,ls='--',label='L = {(x, x/2+1)}：不过原点')
vec(ax,(1,1.5),c=C[1],label='u',off=(0.1,-0.25)); vec(ax,(-2,0),c=C[1],label='v',off=(-0.3,0.15))
vec(ax,(-1,1.5),c='#c0392b',label='u+v ∉ L',off=(-1.3,0.2))
ax.plot([1,-1],[1.5,1.5],':',color='#999'); ax.plot([-2,-1],[0,1.5],':',color='#999')
ax.legend(fontsize=9,loc='lower right'); ax.set_title('子空间必须过原点并对运算封闭')
ax=fig.add_subplot(1,3,2,projection='3d')
g=np.linspace(-1.6,1.6,10); X,Y=np.meshgrid(g,g)
ax.plot_surface(X,Y,0*X,alpha=0.25,color=C[0]); ax.plot_surface(X,0*X+0.0+Y*0,  Y*0+X*0+Y, alpha=0) 
Xb,Zb=np.meshgrid(g,g); ax.plot_surface(Xb,0.6*Zb,Zb,alpha=0.25,color=C[2])
ax.plot([-1.6,1.6],[0,0],[0,0],color='#c0392b',lw=3)
ax.text(1.7,0,0.1,'W₁∩W₂',color='#c0392b',fontsize=11); ax.text(-1.6,-1.6,0.1,'W₁',color=C[0],fontsize=12); ax.text(-1.6,1,1.6,'W₂',color=C[2],fontsize=12)
clean3(ax,1.7); ax.view_init(22,-58); ax.set_title('两个平面：交为直线，和为整个 ℝ³')
ax=fig.add_subplot(1,3,3); plane(ax)
ax.plot(t,0*t,color=C[0],lw=2.5); ax.plot(0*t,t,color=C[2],lw=2.5)
ax.text(2.2,0.15,'W₁',color=C[0],fontsize=12); ax.text(0.15,2.5,'W₂',color=C[2],fontsize=12)
vec(ax,(1.8,0),c=C[0],label='u',off=(0,-0.35)); vec(ax,(0,1.5),c=C[2],label='v',off=(-0.35,0))
vec(ax,(1.8,1.5),c='#c0392b',label='u+v',off=(0.05,0.1))
ax.text(-2.9,-2.7,'u+v 不在 W₁∪W₂ 中：并集一般不是子空间\n和空间 W₁+W₂ = 整个平面',fontsize=9.5,bbox=dict(fc='white',ec='none'),zorder=6)
ax.set_title('并 ≠ 和：W₁+W₂ 才是最小子空间')
save(fig,'ch1-subspaces.png')

# 2 basis & coordinates
fig,axs=plt.subplots(1,2,figsize=(11.5,5))
x=np.array([2.2,1.6]); e=[np.array([1,0]),np.array([0,1])]; b=[np.array([1,0.25]),np.array([0.5,1])]
B=np.column_stack(b); c=np.linalg.solve(B,x)
for ax,basis,name,coord in [(axs[0],e,'标准基 e₁, e₂',x),(axs[1],b,'新基 x₁, x₂',c)]:
    plane(ax,3.2)
    M=np.column_stack(basis)
    for k in range(-4,5):
        p=np.array([M@[k,s] for s in (-4,4)]); ax.plot(p[:,0],p[:,1],color='#dde4f0',lw=0.9,zorder=0)
        p=np.array([M@[s,k] for s in (-4,4)]); ax.plot(p[:,0],p[:,1],color='#dde4f0',lw=0.9,zorder=0)
    vec(ax,basis[0],c=C[2],label=name.split('，')[0][-5:-3] if False else None); vec(ax,basis[1],c=C[2])
    ax.text(*(basis[0]+[0.05,-0.35]),'第1个基向量',color=C[2],fontsize=9); ax.text(*(basis[1]+[-1.1,0.1]),'第2个基向量',color=C[2],fontsize=9)
    p1=coord[0]*basis[0]; ax.plot(*zip((0,0),p1),color=C[1],lw=1.2,ls='--'); ax.plot(*zip(p1,x),color=C[1],lw=1.2,ls='--')
    vec(ax,x,c=C[0],label='x',lw=2.6)
    ax.set_title(f'{name}下：坐标 = ({coord[0]:.2f}, {coord[1]:.2f})')
fig.suptitle('同一个向量 x，换一组基，坐标随之改变；坐标变换由过渡矩阵完成',fontsize=12)
save(fig,'ch1-basis-coordinates.png')

# 3 inner products
fig,axs=plt.subplots(1,3,figsize=(14,4.6))
th=np.linspace(0,2*np.pi,400); U=np.stack([np.cos(th),np.sin(th)])
for ax,G,title in [(axs[0],np.eye(2),'G = I：标准内积'),(axs[1],np.diag([2,0.5]),'G = diag(2, 0.5)'),(axs[2],np.array([[1,0.6],[0.6,1]]),'G = [[1, 0.6], [0.6, 1]]')]:
    plane(ax,2)
    w,V=np.linalg.eigh(G); pts=V@np.diag(1/np.sqrt(w))@U
    ax.fill(pts[0],pts[1],color=C[0],alpha=0.12); ax.plot(pts[0],pts[1],color=C[0],lw=2)
    x=np.array([1,0]); 
    y=np.array([-G[0,1],G[0,0]]); y=y/np.sqrt(y@G@y)  # G-orthogonal to x
    x=x/np.sqrt(x@G@x)
    vec(ax,x,c=C[1],label='x'); vec(ax,y,c=C[3],label='y')
    ax.set_title(title); ax.text(-1.9,-1.85,'(x,y) = yᴴGx = 0：在此内积下 x ⊥ y\n蓝色曲线：长度为 1 的向量',fontsize=9)
fig.suptitle('同一个线性空间可以定义不同的内积：“单位圆”变成椭圆，“垂直”的含义也随之改变',fontsize=12)
save(fig,'ch1-inner-products.png')

# 4 projection & Gram-Schmidt
fig=plt.figure(figsize=(12.5,5))
ax=fig.add_subplot(1,2,1); plane(ax,3)
y=np.array([2.6,0.9]); x=np.array([1.2,2.2]); p=(x@y)/(y@y)*y
ax.plot(*zip(-0.4*y,1.1*y),color='#ccc',lw=1); vec(ax,y,c=C[2],label='y',off=(0.05,-0.3)); vec(ax,x,c=C[0],label='x')
vec(ax,p,c=C[1],label='投影 p',off=(-0.2,-0.45)); ax.plot(*zip(p,x),'--',color=C[3],lw=1.8); ax.text(*( (p+x)/2+[0.1,0]),'x − p ⊥ y',color=C[3],fontsize=10)
d=(x-p)/np.linalg.norm(x-p)*0.18; u=y/np.linalg.norm(y)*0.18
ax.plot([p[0]-u[0],p[0]-u[0]+d[0],p[0]+d[0]],[p[1]-u[1],p[1]-u[1]+d[1],p[1]+d[1]],color='#555',lw=1)
ax.text(-2.9,-2.7,'|(x,y)| / ‖y‖ = ‖p‖ ≤ ‖x‖\n⇔ Cauchy–Schwarz：|(x,y)| ≤ ‖x‖·‖y‖',fontsize=10)
ax.set_title('投影与 Cauchy–Schwarz 不等式')
ax=fig.add_subplot(1,2,2,projection='3d')
x1=np.array([1.5,0.3,0.2]); x2=np.array([0.9,1.4,0.3]); x3=np.array([0.4,0.5,1.5])
y1=x1; y2=x2-(x2@y1)/(y1@y1)*y1; y3=x3-(x3@y1)/(y1@y1)*y1-(x3@y2)/(y2@y2)*y2
for v,c,l in [(x1,'#9db9ef','x₁'),(x2,'#9db9ef','x₂'),(x3,'#9db9ef','x₃')]: arrow3(ax,v,c=c,lw=1.4,label=l)
for v,c,l in [(y1,C[0],'y₁'),(y2,C[1],'y₂'),(y3,C[3],'y₃')]: arrow3(ax,v,c=c,lw=2.4,label=l)
ax.plot(*zip(x2,x2-y2),':',color=C[1]); ax.plot(*zip(x3,x3-y3),':',color=C[3])
clean3(ax,1.6); ax.view_init(20,-60); ax.set_title('Gram–Schmidt：每一步减去在已有方向上的投影')
save(fig,'ch1-projection-gram-schmidt.png')

# 5 direct sum
fig,axs=plt.subplots(1,2,figsize=(11.5,5))
for ax,(d1,d2,title) in zip(axs,[((1,0.2),(0.6,1),'直和 V = W₁ ⊕ W₂：沿 W₂ 方向投影到 W₁'),((1,0.35),(-0.35,1),'正交直和 V = W ⊕ W⊥：正交投影')]):
    plane(ax,3); d1=np.array(d1)/np.linalg.norm(d1); d2=np.array(d2)/np.linalg.norm(d2)
    for d,c,l in [(d1,C[0],'W₁' if '⊥' not in title else 'W'),(d2,C[2],'W₂' if '⊥' not in title else 'W⊥')]:
        ax.plot(*zip(-3.5*d,3.5*d),color=c,lw=2,alpha=0.7); ax.text(*(2.7*d+[0.1,0.1]),l,color=c,fontsize=12)
    x=np.array([2.3,1.5]) if '⊥' not in title else np.array([1.0,2.2]); a,b=np.linalg.solve(np.column_stack([d1,d2]),x)
    vec(ax,a*d1,c=C[0],label='x₁',off=(0.05,-0.35)); vec(ax,b*d2,c=C[2],label='x₂',off=(-0.45,0.05)); vec(ax,x,c=C[1],label='x = x₁ + x₂',lw=2.6)
    ax.plot(*zip(a*d1,x),'--',color='#999'); ax.plot(*zip(b*d2,x),'--',color='#999')
    ax.set_title(title,fontsize=11)
axs[0].text(-2.9,-2.8,'W₁∩W₂ = {0} ⇒ 分解唯一\ndim W₁ + dim W₂ = dim V',fontsize=9.5)
axs[1].text(-2.9,-2.8,'x₁ 是 W 中离 x 最近的点\n‖x‖² = ‖x₁‖² + ‖x₂‖²',fontsize=9.5)
save(fig,'ch1-direct-sum.png')

# 6 fourier
fig,axs=plt.subplots(1,2,figsize=(12.5,4.2),gridspec_kw={'width_ratios':[1.6,1]})
t=np.linspace(-np.pi,np.pi,1000); sq=np.sign(np.sin(t))
ax=axs[0]; ax.plot(t,sq,color='#999',lw=1.5,label='方波 f(t)'); ax.grid(True)
for N,c in [(1,C[0]),(3,C[2]),(7,C[1]),(25,C[3])]:
    s=sum(4/(np.pi*k)*np.sin(k*t) for k in range(1,N+1,2)); ax.plot(t,s,color=c,lw=1.6,label=f'前 {N} 阶')
ax.legend(fontsize=9,ncol=5,loc='upper center',bbox_to_anchor=(0.5,1.17)); ax.set_xlabel('t')
ax=axs[1]; k=np.arange(1,16); coef=np.where(k%2==1,4/(np.pi*k),0)*np.sqrt(np.pi)
ax.bar(k,coef,color=C[0]); ax.set_xticks(range(1,16,2)); ax.set_xlabel('基函数 sin(kt)/√π 的序号 k'); ax.set_title('坐标 = 内积 (f, εₖ)'); ax.grid(True,axis='y')
fig.suptitle('函数也是向量：{1/√2π, cos kt/√π, sin kt/√π} 是标准正交基，傅里叶系数就是坐标',fontsize=12,y=1.06)
save(fig,'ch1-fourier-basis.png')
