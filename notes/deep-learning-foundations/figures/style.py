import matplotlib, logging
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
try: font_manager.fontManager.addfont('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
except OSError: pass  # 需要可用的中文字体，例如文泉驿正黑
plt.rcParams.update({
 'font.family':['WenQuanYi Zen Hei','DejaVu Sans'],'axes.unicode_minus':False,'font.size':11,
 'axes.spines.top':False,'axes.spines.right':False,'axes.titlesize':12,'axes.titleweight':'bold',
 'figure.dpi':100,'savefig.dpi':160,'savefig.bbox':'tight','axes.grid':True,'grid.alpha':0.25,
 'legend.frameon':False,'mathtext.fontset':'custom','mathtext.rm':'DejaVu Sans','mathtext.it':'DejaVu Sans:italic','mathtext.bf':'DejaVu Sans:bold','mathtext.sf':'DejaVu Sans','mathtext.fallback':'stixsans',
})
C=['#2f6fde','#e8743b','#19a979','#c94c7c','#8a5cd1','#7f7f7f','#d4a017']
import os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../../images/courses/deep-learning-foundations/')
def save(fig,name):
    fig.savefig(OUT+name, facecolor='white'); plt.close(fig); print('saved',name)
from matplotlib.ticker import FuncFormatter
import math
def logfmt(ax):
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_: '$10^{%d}$'%round(math.log10(v)) if v>0 else ''))
_orig_save=save
def save(fig,name):
    for ax in fig.axes:
        if ax.get_yscale()=='log': logfmt(ax)
    _orig_save(fig,name)
