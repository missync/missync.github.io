from style import *
import numpy as np
import matplotlib.patches as mp
plt.rcParams['axes.grid']=False
def vec(ax,v,o=(0,0),c='#2f6fde',lw=2.2,label=None,fs=12,off=(0.05,0.05),ls='-',alpha=1,zorder=3):
    ax.annotate('',xy=(o[0]+v[0],o[1]+v[1]),xytext=o,arrowprops=dict(arrowstyle='-|>',color=c,lw=lw,ls=ls,mutation_scale=14,shrinkA=0,shrinkB=0,alpha=alpha),zorder=zorder)
    if label: ax.text(o[0]+v[0]+off[0],o[1]+v[1]+off[1],label,color=c,fontsize=fs,zorder=5)
def plane(ax,lim=3,ticks=False):
    ax.axhline(0,color='#bbb',lw=0.8,zorder=0); ax.axvline(0,color='#bbb',lw=0.8,zorder=0)
    ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim); ax.set_aspect('equal')
    if not ticks: ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
def arrow3(ax,v,o=(0,0,0),c='#2f6fde',lw=2,label=None):
    ax.quiver(*o,*v,color=c,lw=lw,arrow_length_ratio=0.12)
    if label: ax.text(o[0]+v[0]*1.08,o[1]+v[1]*1.08,o[2]+v[2]*1.08,label,color=c,fontsize=12)
def clean3(ax,lim=2):
    ax.set_xlim(-lim,lim);ax.set_ylim(-lim,lim);ax.set_zlim(-lim,lim)
    ax.set_xticklabels([]);ax.set_yticklabels([]);ax.set_zticklabels([])
    ax.set_box_aspect((1,1,1))
