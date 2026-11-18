# 矩阵理论与应用：笔记原稿

- [第一章：线性空间引论](linear-spaces.md)
- [第二章：线性映射与矩阵](linear-maps.md)
- [第三章：矩阵分解](matrix-decompositions.md)
- [第四章：矩阵分析](matrix-analysis.md)

网站页面位于 `courses/matrix-theory/`，插图位于 `images/courses/matrix-theory/`。插图由 `figures/` 中的脚本生成（`python3 figures/ch1.py` 等，需要 matplotlib 与中文字体），会直接输出到图片目录。

写法约定：正文中用 `<div class="note note-*" markdown="1">` 提示框区分内容类型——`note-info` 直观理解、`note-primary` 定义、`note-success` 定理、`note-warning` 例题、`note-danger` 易错点；独立公式放在 `course-math` 容器中。重新用 Hexo 生成站点时，需要支持 Markdown 内嵌 HTML 块中的 Markdown，并把原稿与图片放入源工程，避免页面被覆盖。
