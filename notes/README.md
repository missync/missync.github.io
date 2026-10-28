# 课程笔记原稿

本目录保留新增课程笔记的 Markdown 原稿。网站页面位于 `courses/`，插图位于 `images/courses/`，目录结构与原有静态站点一致。

当前仓库保存的是 Hexo 生成后的站点，不包含 `_config.yml`、主题源文件或完整构建工程。若之后从本地 Hexo 工程重新生成站点，应先将这里的 Markdown 原稿加入该工程的 `source/_posts/`（也可以按原工程的课程页面组织方式放置），并将配图复制到 `source/images/courses/deep-learning-foundations/`，避免新页面在重新部署时被覆盖。

原稿中的 `permalink` 与现有页面地址一致，`math: true` 用于开启公式。内容中的 `course-math` 容器依赖页面样式；生成时请保持数学公式内容原样，并为该类设置横向滚动。课程目录、前后章导航和站内搜索也需与源工程保持同步。

- [第三章：神经网络与训练](deep-learning-foundations/neural-networks.md)
- [第四章：卷积神经网络](deep-learning-foundations/convolutional-neural-networks.md)
