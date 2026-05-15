# 自动控制原理 — 频域分析与校正

> 一个例子贯穿始终 · 一张页面囊括全章 · 三本经典对照参考

本项目以**直流电机转速控制**为贯穿例子，将《自动控制原理》第5章「线性系统的频域分析与校正」的全部知识点串联起来，包含完整的教学文档、25 张 Python 生成的图表、以及可交互的 Web 页面。

---

## 项目结构

```
.
├── README.md                                    # 本文件
├── 自动控制原理入门.html                         # 贯穿全书的交互式概览页（第1章-第9章）
├── 第5章_频域分析与校正.html                     # 第5章完整教学网页（含侧边导航、MathJax公式）
├── 第5章_线性系统的频域分析与校正.md              # 第5章 Markdown 源文件
├── generate_all_figures.py                      # 全部图表的 Python 生成脚本
├── figures/                                     # 25 张 PNG 图表（150 dpi）
│   ├── fig5_1_sine_response.png                 # 正弦响应
│   ├── fig5_2a~2e_nyquist_*.png                 # 典型环节 Nyquist 图
│   ├── fig5_3a~3h_bode_*.png                    # 典型环节 Bode 图
│   ├── fig5_4a~4b_nyquist_criterion*.png        # 奈奎斯特稳定判据
│   ├── fig5_5a~5b_stability_margins*.png        # 稳定裕度
│   ├── fig5_6_openloop_freq_regions.png         # 三频段分析
│   ├── fig5_7_closed_loop_response.png          # 闭环频率特性
│   ├── fig5_9_correction_before_after.png       # 校正前后对比
│   ├── fig5_9_lead_lag_comparison.png           # 超前vs滞后
│   ├── fig5_9_pid_frequency.png                 # PID 频域特性
│   ├── fig5_x_correction_design_flow.png         # 校正设计流程
│   └── fig5_x_nyquist_openloop_summary.png      # 开环Nyquist汇总
├── 书籍/
│   └── 自动控制原理--卢京潮 2009.pdf             # 参考教材（加密，仅本地）
└── memory/                                      # Claude Code 记忆文件
```

---

## 快速开始

### 在线浏览

直接打开 HTML 文件即可：

```bash
# 全书概览（推荐先看这个）
start 自动控制原理入门.html

# 第5章完整教学
start 第5章_频域分析与校正.html
```

### 本地生成图表

```bash
pip install matplotlib numpy scipy
python generate_all_figures.py
# 输出 → ./figures/
```

---

## 第5章内容覆盖

| 节 | 内容 | 状态 |
|----|------|------|
| 5.1 | 频率特性的基本概念 | ✅ |
| 5.2 | 幅相频率特性（Nyquist 图） | ✅ 含 6 种典型环节 |
| **5.3** | **对数频率特性（Bode 图）** ⭐ | ✅ 含渐近线法、反问题、最小相位 |
| 5.4 | 频域稳定判据 | ✅ Nyquist + 对数判据 |
| **5.5** | **稳定裕度** ⭐ | ✅ PM/GM 定义与计算 |
| 5.6 | 开环频域性能分析 | ✅ 三频段分析 |
| 5.7-5.8 | 闭环频率特性 | ✅ 特征量 + 时域关系 |
| **5.9** | **频域法串联校正** ⭐⭐⭐ | ✅ 超前/滞后/滞后-超前/PID |

---

## 参考书籍

本项目内容参考以下三本经典教材编写，力求在严谨性和通俗性之间取得平衡：

<table>
<tr>
  <td align="center" width="33%">
    <strong>📘 自动控制原理</strong><br>
    卢京潮 主编<br>
    <em>清华大学出版社，2009</em>
  </td>
  <td align="center" width="33%">
    <strong>📙 自动控制原理</strong><br>
    胡寿松 主编<br>
    <em>科学出版社，第7版，2019</em>
  </td>
  <td align="center" width="33%">
    <strong>📗 控制之美</strong><br>
    王广雄 主编<br>
    <em>清华大学出版社，2012</em>
  </td>
</tr>
<tr>
  <td valign="top">
    <strong>特色</strong>：西北工业大学国家级精品课程教材，理论体系完整，例题丰富，考研指定参考书之一。
  </td>
  <td valign="top">
    <strong>特色</strong>：国内最广泛使用的自控教材之一，内容系统全面，涵盖经典控制与现代控制，习题量大，适合系统学习与考研复习。
  </td>
  <td valign="top">
    <strong>特色</strong>：以"控制之美"为核心理念，注重物理直觉与数学严谨的统一，图文并茂，深入浅出，适合入门与深化理解。
  </td>
</tr>
</table>

> **声明**：本项目为个人学习笔记和教学辅助材料，内容参考上述教材整理编写。教材 PDF 文件仅用于个人学习，不包含在本仓库中。

---

## 技术栈

- **前端**：HTML5 + CSS3 + MathJax 3（LaTeX 公式渲染）
- **图表**：Python 3 + matplotlib + numpy + scipy
- **交互**：原生 JavaScript（侧边导航、滚动定位、返回顶部）

---

## License

MIT License — 仅供学习交流使用，欢迎 Star ⭐ 和 PR。

---

## 致谢

感谢卢京潮老师、胡寿松老师、王广雄老师的经典教材，为无数控制学子铺平了学习之路。

---

*Made with ❤️ by [TanGuilin520](https://github.com/TanGuilin520)*
