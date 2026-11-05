from common import *
# 1 grid deformation
F=np.array([[0,0],[0,2],[1.2,2],[1.2,1.65],[0.4,1.65],[0.4,1.15],[1,1.15],[1,0.8],[0.4,0.8],[0.4,0]]).T
mats=[('旋转 30°',np.array([[np.cos(np.pi/6),-np.sin(np.pi/6)],[np.sin(np.pi/6),np.cos(np.pi/6)]])),
      ('剪切',np.array([[1,0.8],[0,1]])),('伸缩 diag(1.6, 0.6)',np.diag([1.6,0.6])),
      ('关于直线 y=x 反射',np.array([[0,1],[1,0]])),('投影到 x 轴（秩 1）',np.array([[1,0],[0,0]])),('一般矩阵 [[1,1],[−0.5,1]]',np.array([[1,1],[-0.5,1]]))]
fig,axs=plt.subplots(2,3,figsize=(13.5,8.6))
for ax,(name,A) in zip(axs.ravel(),mats):
    plane(ax,3)
    for k in range(-3,4):
        for line in ([[k,k],[-3,3]],[[-3,3],[k,k]]):
            P=np.array(line); ax.plot(P[0],P[1],color='#eceff4',lw=0.8,zorder=0)
            Q=A@P; ax.plot(Q[0],Q[1],color='#b9cdee',lw=0.9,zorder=1)
    ax.fill(F[0],F[1],color='#cccccc',alpha=0.6,zorder=2); G=A@F; ax.fill(G[0],G[1],color=C[1],alpha=0.75,zorder=3)
    vec(ax,A[:,0],c=C[0],lw=2.2); vec(ax,A[:,1],c=C[2],lw=2.2)
    ax.set_title(f'{name}\ndet = {np.linalg.det(A):.2f}',fontsize=11)
fig.suptitle('矩阵就是线性映射：灰色“F”经映射变为橙色，蓝/绿箭头是 e₁、e₂ 的像，也就是矩阵的两列',fontsize=12)
save(fig,'ch2-linear-maps.png')

# 2 kernel and image (rank 2 map R3->R3)
A=np.array([[1,0,1],[0,1,1],[1,1,2]],float)
fig=plt.figure(figsize=(12.5,5.2))
ax=fig.add_subplot(1,2,1,projection='3d')
k=np.array([1,1,-1])/np.sqrt(3); t=np.linspace(-1.8,1.8,2)
ax.plot(k[0]*t,k[1]*t,k[2]*t,color='#c0392b',lw=3); ax.text(*(k*1.9),'N(T)',color='#c0392b',fontsize=12)
x0=np.array([0.8,-0.2,0.4]); 
for s in [-1.2,0,1.2]: ax.scatter(*(x0+s*k),color=C[1],s=25)
ax.plot(*np.array([x0-1.4*k,x0+1.4*k]).T,color=C[1],ls='--')
ax.text(*(x0+1.5*k),'x₀ + N(T)：都映到同一点',color=C[1],fontsize=9)
clean3(ax,1.8); ax.set_title('定义域 ℝ³：核是一条直线（dim = 1）'); ax.view_init(20,-50)
ax=fig.add_subplot(1,2,2,projection='3d')
g=np.linspace(-1.5,1.5,8); S,T=np.meshgrid(g,g); P=np.einsum('ij,jkl->ikl',A[:,:2],np.stack([S,T]))
ax.plot_surface(P[0],P[1],P[2],alpha=0.3,color=C[0]); ax.text(1.4,-1.6,1.8,'R(T)',color=C[0],fontsize=12)
y=A@x0; ax.scatter(*y,color=C[1],s=50); ax.text(*(y+0.15),'T(x₀)',color=C[1])

clean3(ax,2.2); ax.set_title('值域 ℝ³：像是一个平面（dim = 2）'); ax.view_init(30,25)
fig.suptitle('亏加秩定理：dim N(T) + dim R(T) = 1 + 2 = 3 = dim V（这里 A = [[1,0,1],[0,1,1],[1,1,2]]）',fontsize=12)
save(fig,'ch2-kernel-image.png')

# 3 eigenvectors & power method
A=np.array([[2,1],[1,3]],float); w,V=np.linalg.eigh(A)
fig,axs=plt.subplots(1,2,figsize=(12.5,5.4))
ax=axs[0]; plane(ax,4)
th=np.linspace(0,2*np.pi,25)[:-1]
for t in th:
    x=np.array([np.cos(t),np.sin(t)]); y=A@x
    ax.annotate('',xy=y,xytext=x,arrowprops=dict(arrowstyle='-|>',color='#c8d3e6',lw=0.9,mutation_scale=8))
c=np.linspace(0,2*np.pi,200); ax.plot(np.cos(c),np.sin(c),color='#999',lw=1)
E=A@np.stack([np.cos(c),np.sin(c)]); ax.plot(E[0],E[1],color=C[0],lw=1.6)
for i,col in [(0,C[2]),(1,C[1])]:
    v=V[:,i]; ax.plot(*zip(-4.5*v,4.5*v),color=col,lw=1,ls='--')
    vec(ax,v,c=col,lw=2.4); vec(ax,w[i]*v,c=col,lw=1.2,alpha=0.6)
    ax.text(*(w[i]*v+[0.1,0.1]),f'λ={w[i]:.2f}',color=col,fontsize=10)
ax.set_title('单位圆 → 椭圆：只有特征方向不转，只被拉伸 λ 倍')
ax=axs[1]; plane(ax,1.3)
x=np.array([1.0,-0.5]); x=x/np.linalg.norm(x); est=[]
for k in range(6):
    vec(ax,x,c=plt.cm.viridis(k/6),lw=1.8,label=f'x{k}',fs=9)
    y=A@x; est.append(x@y/(x@x)); x=y/np.linalg.norm(y)
v=V[:,1]; ax.plot(*zip(-1.4*v,1.4*v),color=C[1],ls='--',lw=1); ax.text(*(1.15*v),'主特征方向',color=C[1])
ax.text(-1.25,-1.25,'Rayleigh 商估计：'+', '.join(f'{e:.3f}' for e in est)+f'\n→ λ₁ = {w[1]:.4f}',fontsize=9)
ax.set_title('幂法：反复左乘 A 并归一化，方向收敛到主特征向量')
save(fig,'ch2-eigenvectors.png')

# 4 householder & givens
fig,axs=plt.subplots(1,2,figsize=(12,5.2))
ax=axs[0]; plane(ax,3)
x=np.array([1.5,2.0]); y=np.array([np.linalg.norm(x),0]); wv=(x-y)/np.linalg.norm(x-y)
m=np.array([-wv[1],wv[0]]); ax.plot(*zip(-3.5*m,3.5*m),color='#999',lw=1.5,ls='--'); ax.text(*(2.6*m+[0.1,0]),'镜面 w⊥',color='#777')
vec(ax,wv,c=C[3],label='w'); vec(ax,x,c=C[0],label='x'); vec(ax,y,c=C[1],label='Hx = ‖x‖e₁',off=(-0.6,-0.4))
ax.plot(*zip(x,y),':',color='#555')
ax.set_title('Householder：H = I − 2wwᴴ，把 x 镜像到坐标轴上')
ax.text(-2.9,-2.7,'H 是酉矩阵、Hermite、对合（H² = I）\n常用于一次性把一列化为 (*, 0, …, 0)',fontsize=9.5)
ax=axs[1]; plane(ax,3)
x=np.array([2.0,1.4]); r=np.linalg.norm(x); c_,s_=x/r
arc=np.linspace(0,np.arctan2(x[1],x[0]),40); ax.plot(0.9*np.cos(arc),0.9*np.sin(arc),color=C[2])
ax.text(1.0,0.3,'θ',color=C[2],fontsize=12)
vec(ax,x,c=C[0],label='x=(xᵢ, xⱼ)'); vec(ax,(r,0),c=C[1],label='Tx = (√(xᵢ²+xⱼ²), 0)',off=(-1.6,-0.45))
ax.set_title('Givens：在 (i, j) 坐标平面内旋转 −θ，消去一个分量')
ax.text(-2.9,-2.7,'c = xᵢ/r，s = xⱼ/r\n每次只改动两行，适合逐个消元',fontsize=9.5)
save(fig,'ch2-householder-givens.png')
