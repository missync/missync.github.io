---
title: 深度学习基础与应用（三）：神经网络与训练
date: 2026-10-28 12:00:00
updated: 2026-10-28 12:00:00
permalink: /courses/deep-learning-foundations/neural-networks/
categories:
  - 深度学习
tags:
  - 深度学习
math: true
description: 前向与反向传播、计算图、激活函数、泛化与正则化。
---

## 1. 从多层感知机到完整训练过程

上一章用隐藏层之间的非线性变换，把线性分类器扩展为 MLP。本章继续回答三个问题：**参数怎样得到梯度、激活函数怎样影响训练、训练误差低为什么还可能泛化差。**

以一个隐藏层的分类网络为例，沿用列向量记法：输入 x 为 D 维，隐藏层宽度为 H，类别数为 C。

<div class="course-math">
\[
z_1=W_1x+b_1,\quad h=\phi(z_1),\quad
s=W_2h+b_2,\quad p=\operatorname{softmax}(s),
\]
\[
W_1\in\mathbb R^{H\times D},\quad W_2\in\mathbb R^{C\times H},
\qquad \ell=-\log p_c.
\]
</div>

c 是正确类别索引，s 是类别分数，φ 是激活函数。整个数据集的训练目标还可以加上正则项。

| 环节 | 计算内容 | 得到什么 |
| --- | --- | --- |
| 前向传播 Forward | 输入依次经过各层，再计算损失 | 中间激活、输出与损失 |
| 反向传播 Backward | 从损失出发，按计算图逆序应用链式法则 | 损失对各参数的梯度 |
| 参数更新 | 优化器利用梯度更新权重和偏置 | 下一次迭代使用的参数 |

**反向传播负责求梯度，优化器负责更新参数。** 两者是训练中相连的不同环节。前向计算保存的中间结果，也会在反向求导时使用。

## 2. 计算图与链式法则

### 2.1 把复杂函数拆成局部运算

计算图把加法、乘法、矩阵乘法、激活函数等表示为节点。每个节点只需要知道自己的前向规则和局部导数，就可以组合成整个网络的求导过程。

若某节点输出 q=f(x)，上游已经传来损失对 q 的导数，则：

<div class="course-math">
\[
\frac{\partial L}{\partial x}
=\frac{\partial L}{\partial q}\frac{\partial q}{\partial x}.
\]
</div>

即**下传梯度 = 上游梯度 × 局部导数**。这里先用标量说明；向量、矩阵情况要按维度进行乘法，不能直接把所有梯度都当成标量相乘。

### 2.2 手算例子：f=(x+y)z

课件取 x=−2、y=5、z=−4。令 q=x+y，前向先算 q=3，再算 f=qz=−12。

反向从 ∂f/∂f=1 出发：

<div class="course-math">
\[
\frac{\partial f}{\partial q}=z=-4,\qquad
\frac{\partial f}{\partial z}=q=3,
\]
\[
\frac{\partial f}{\partial x}
=\frac{\partial f}{\partial q}\cdot1=-4,\qquad
\frac{\partial f}{\partial y}
=\frac{\partial f}{\partial q}\cdot1=-4.
\]
</div>

![加法和乘法节点的反向传播示例](/images/courses/deep-learning-foundations/backpropagation.png)
*课件第 67 页：绿色为前向数值，红色为反向梯度。反向传播计算的是输出变化对各输入的敏感程度。*

### 2.3 常见节点怎样传梯度

| 节点 | 局部求导规律 | 直观理解 |
| --- | --- | --- |
| 加法 q=x+y | 对两输入的局部导数都为 1 | 将上游梯度分别传给两条输入 |
| 乘法 q=xy | 对 x 的导数为 y，对 y 的导数为 x | 用另一输入的值缩放上游梯度 |
| 最大值 q=max(x,y) | 无并列最大值时，仅最大输入获得梯度 | 将梯度路由到被选中的输入 |
| 分支：同一变量用于多处 | 累加每条后续路径传回的梯度 | 一次使用产生一项贡献 |

**沿一条路径使用链式法则，来自多条路径的贡献相加。** 参数共享的卷积层、后面要学的残差连接，都遵循同一规则。最大值出现并列时，需要约定具体的次梯度或实现规则。

## 3. 向量化反向传播与形状检查

### 3.1 线性层的三个梯度

设 q=Wx+b，其中 x∈ℝᴰ、W∈ℝᴹˣᴰ、q 与 b 为 M 维，上游梯度记作 g=∇q L。

<div class="course-math">
\[
\nabla_W L=gx^{\mathsf T},\qquad
\nabla_x L=W^{\mathsf T}g,\qquad
\nabla_b L=g.
\]
</div>

| 梯度 | 计算形状 | 与谁一致 |
| --- | --- | --- |
| ∇W L | (M×1)(1×D)=M×D | 权重 W |
| ∇x L | (D×M)(M×1)=D×1 | 输入 x |
| ∇b L | M×1 | 偏置 b |

**对某个变量的梯度，形状应与该变量相同。** 这是检查转置、广播和维度错误的直接办法。批量计算时，偏置在各样本间共享，因此要累加各样本对偏置的梯度；若损失取批内平均，还要包含相应的平均系数。

### 3.2 课件例子：f(x,W)=‖Wx‖²

令 q=Wx，f=qᵀq，则 ∇q f=2q。代入线性层的规则：

<div class="course-math">
\[
\nabla_W f=2qx^{\mathsf T},\qquad
\nabla_x f=2W^{\mathsf T}q.
\]
</div>

课件中 W=[[0.1,0.5],[−0.3,0.8]]，x=[0.2,0.4]ᵀ，因此 q=[0.22,0.26]ᵀ，f=0.116。权重梯度为 [[0.088,0.176],[0.104,0.208]]，输入梯度为 [−0.112,0.636]ᵀ。

### 3.3 把两层分类网络串起来

对于第 1 节的单样本 Softmax 交叉熵，令 y 为 one-hot 标签，⊙ 为逐元素乘法，可以得到：

<div class="course-math">
\[
\delta_2=p-y,\qquad
\nabla_{W_2}\ell=\delta_2h^{\mathsf T},\qquad
\nabla_{b_2}\ell=\delta_2,
\]
\[
\delta_1=(W_2^{\mathsf T}\delta_2)\odot\phi'(z_1),\qquad
\nabla_{W_1}\ell=\delta_1x^{\mathsf T},\qquad
\nabla_{b_1}\ell=\delta_1.
\]
</div>

这是把线性层、激活函数与损失的局部规则组合起来的结果。若目标中还有正则项，参数梯度还要加上正则项的贡献。

## 4. 激活函数：表达能力与梯度传播

### 4.1 为什么隐藏层需要非线性

多层仿射变换可以合并为一层，只有在线性层之间加入非线性，才能获得更丰富的函数表示。激活函数还通过自己的导数影响梯度怎样传到前面的层。

![Sigmoid、tanh、ReLU、ELU、GELU 与 Swish 的曲线对照](/images/courses/deep-learning-foundations/activation-functions.png)
*课件第 100 页：比较函数曲线时，也要关注饱和区和负半轴的梯度。*

### 4.2 Sigmoid 与 tanh

<div class="course-math">
\[
\sigma(z)=\frac1{1+e^{-z}},\qquad
\sigma'(z)=\sigma(z)(1-\sigma(z)),
\]
\[
\tanh(z)=2\sigma(2z)-1,\qquad
\tanh'(z)=1-\tanh^2(z).
\]
</div>

Sigmoid 输出位于 (0,1)，适合表示二分类概率，但作为深层隐藏激活存在两个问题：输入绝对值很大时进入饱和区，导数接近 0；输出始终为正，不以零为中心。Sigmoid 的导数最大只有 1/4，多层链式相乘时可能使梯度进一步缩小。

tanh 输出位于 (−1,1)，函数以原点为中心，但大正值和大负值处仍会饱和。**“以零为中心”描述函数特性，不保证任意一批激活的均值恰好为 0。** 梯度是否消失还与权重、深度及整体结构有关。

### 4.3 ReLU、Leaky ReLU 与 PReLU

<div class="course-math">
\[
\operatorname{ReLU}(z)=\max(0,z),\qquad
\operatorname{LeakyReLU}(z)=\max(\alpha z,z),\quad 0<\alpha<1.
\]
</div>

ReLU 在正半轴的导数为 1，计算简单，是传统 CNN 中常见的隐藏激活。负半轴导数为 0；如果一个神经元对训练样本长期都输出 0，它的输入侧参数可能持续收不到梯度，称为 **Dying ReLU**。单个样本出现负输入，并不意味着该神经元永久死亡。

Leaky ReLU 在负半轴保留小斜率；PReLU 进一步把这个斜率设为可学习参数。ReLU 在 0 点不可导，实际实现通常采用约定的次梯度。

### 4.4 ELU、GELU 与 SiLU

<div class="course-math">
\[
\operatorname{ELU}(z)=
\begin{cases}z,&z>0,\\\alpha(e^z-1),&z\le0,\end{cases}
\quad \alpha>0,
\]
\[
\operatorname{GELU}(z)=z\Phi(z),\qquad
\operatorname{SiLU}(z)=z\sigma(z).
\]
</div>

Φ 是标准正态分布的累积分布函数。GELU 常用的 tanh 近似为：

<div class="course-math">
\[
\operatorname{GELU}(z)\approx
\frac z2\left[1+\tanh\!\left(\sqrt{\frac2\pi}(z+0.044715z^3)\right)\right].
\]
</div>

| 函数 | 核心特点 | 需要注意 |
| --- | --- | --- |
| ELU | 正半轴线性，负半轴平滑趋向 −α | 负值不等于所有输入分布下都严格零均值；负向饱和时梯度也会小 |
| GELU | 用 Φ(z) 对输入做平滑加权 | 比 ReLU 复杂，常使用近似实现 |
| SiLU / Swish（β=1） | 用 Sigmoid 平滑门控，保留部分负输出 | 不等同于只输出正数的 ReLU |

课件还介绍了 **SwiGLU**：一条线性分支经过 SiLU，再与另一条线性分支逐元素相乘。

<div class="course-math">
\[
\operatorname{SwiGLU}(x)
=\operatorname{SiLU}(xW+b)\odot(xV+c).
\]
</div>

这里按行向量记法写，与前面的列向量记法仅是矩阵放置约定不同。**SwiGLU 是包含双分支投影的门控结构，SiLU 是其中使用的激活函数。**

## 5. 泛化、欠拟合与过拟合

### 5.1 我们关心的是新数据上的误差

训练损失用于指导参数学习，泛化误差衡量模型在未见样本上的表现。模型既要学到规律，也要避免把训练集里的噪声与偶然关系当作规律。

| 状态 | 常见表现 | 排查与改进方向 |
| --- | --- | --- |
| 欠拟合 | 训练和验证误差都较高 | 检查优化是否充分，再考虑增加容量或改进表示 |
| 过拟合 | 训练误差低，验证误差明显更高 | 增加数据、正则化、数据增强、早停 |
| 拟合较合适 | 训练误差较低，验证表现也较好 | 用独立测试集评价最终泛化 |

**训练误差高不一定只因为模型太小，也可能是学习率或优化过程出了问题。** 诊断时应结合训练曲线和验证曲线。

### 5.2 Bias 与 Variance 分别看什么

偏差 Bias 衡量模型平均预测与真实规律的系统性差异；方差 Variance 衡量更换训练集后，预测结果的波动程度。这里的偏差不同于线性层中的偏置参数 b。

为明确课件中的关系，在平方误差回归下，设 y=f(x)+ε，噪声条件均值为 0、方差为 σ²，D 表示随机训练集，则固定 x 处有：

<div class="course-math">
\[
\mathbb E_{D,\varepsilon}\!\left[(\hat f_D(x)-y)^2\right]
=\underbrace{\left(\mathbb E_D[\hat f_D(x)]-f(x)\right)^2}_{\text{Bias}^2}
+\underbrace{\mathbb E_D\!\left[(\hat f_D(x)-\mathbb E_D\hat f_D(x))^2\right]}_{\text{Variance}}
+\sigma^2.
\]
</div>

最后一项是该假设下的不可约噪声误差。模型太简单往往偏差高；过度追随训练样本的复杂模型往往方差高。课件中的经典曲线用于建立直觉，**不能把所有深度网络的测试误差都预设为严格的 U 形曲线**。

## 6. 正则化与避免过拟合

### 6.1 把数据损失与参数约束合在一起

<div class="course-math">
\[
L(W)=\frac1N\sum_{i=1}^{N}\ell_i(W)+\lambda R(W).
\]
</div>

数据损失要求模型解释训练数据，正则项对参数施加偏好，λ 控制两者的相对强度。以下统一采用 L2 项含 1/2 的约定；如果省去 1/2，相应梯度会多一个 2。

| 方法 | 正则项 R(W) | 倾向 |
| --- | --- | --- |
| L1 | 各权重绝对值之和 | 倾向产生稀疏权重，0 点用次梯度处理 |
| L2 | 权重平方和的 1/2 | 惩罚大权重，使权重整体收缩 |

课件给出两个权重向量 [1,0,0,0] 与 [0.25,0.25,0.25,0.25]，它们与输入 [1,1,1,1] 的点积都为 1，但权重平方和分别是 1 和 1/4，L2 更偏好后者。这说明正则项会在相同数据拟合结果之间继续施加偏好。

### 6.2 L2 为什么对应权重衰减

采用普通 SGD、L2 正则项 λ‖W‖²/2 时，更新式为：

<div class="course-math">
\[
W_{t+1}
=W_t-\eta\left(\nabla_W L_{\mathrm{data}}+\lambda W_t\right)
=(1-\eta\lambda)W_t-\eta\nabla_W L_{\mathrm{data}}.
\]
</div>

除了沿数据梯度更新，原权重还乘上一个收缩系数，这就是这里的 Weight Decay。**这个等价关系基于普通 SGD 的更新式，不能不加区分地推广到所有优化器。** 正则化强度过大也会造成欠拟合。

### 6.3 Dropout：训练时随机屏蔽激活

课件用 p 表示丢弃概率。每次训练时为激活采样随机掩码，使网络减少对某个节点的过度依赖。它通常屏蔽激活，不是永久删除神经元或把参数清零。

![Dropout 前后网络连接的示意](/images/courses/deep-learning-foundations/dropout.png)
*课件第 149 页：每一步随机使用部分节点，常见于全连接层。*

采用常见的 inverted dropout，设保留概率 q=1−p：

<div class="course-math">
\[
m_j\sim\operatorname{Bernoulli}(q),\qquad
\tilde h_j=\frac{m_j}{q}h_j,\qquad
\mathbb E[\tilde h_j\mid h_j]=h_j.
\]
</div>

训练时对保留的激活除以 q，使期望保持不变；测试时关闭随机丢弃，直接使用完整激活，不再额外乘 q。**需要分清 p 是丢弃率还是保留率，以及缩放发生在训练还是测试阶段。**

### 6.4 Early Stopping 与数据增强

**早停**监控验证集指标：训练误差继续下降、验证误差却开始变差时，保留验证表现最好的检查点。可设置 patience 容忍短期波动，而不是根据测试集选择停止时间。

**数据增强**对训练样本做保持标签语义的变换，例如合理的裁剪、翻转和颜色变化，增加训练输入的多样性。变换必须与任务匹配：水平翻转通常适合普通物体识别，却未必适合区分左右方向的任务。增强不会凭空增加独立采集样本中的全部新信息。

## 7. 本章易混淆点

| 容易混淆的说法 | 应怎样理解 |
| --- | --- |
| Backward 就是更新参数 | 先反向计算梯度，再由优化器更新参数 |
| 反向传播只需一路相乘 | 路径上用链式法则，分支贡献要相加 |
| ReLU 遇到负数就永久死亡 | 单次零激活与对训练数据持续失活不同 |
| 函数以零为中心就意味着激活均值为 0 | 实际均值还取决于输入分布 |
| 训练准确率越高，模型就越好 | 还要看验证与独立测试表现 |
| Dropout 在测试时继续随机丢弃 | 常规推理应关闭随机丢弃，并保持缩放约定一致 |

---

*课程依据：于茜《lecture3_NN_20261015》，2026-10-15。反向传播数值、激活函数与正则化主题据课件整理；完整两层网络梯度、偏差—方差展开式与 Dropout 期望为帮助理解补充的推导。*

[课程目录](/courses/deep-learning-foundations/) · [上一章：图像分类](/courses/deep-learning-foundations/image-classification/) · [下一章：卷积神经网络](/courses/deep-learning-foundations/convolutional-neural-networks/)
