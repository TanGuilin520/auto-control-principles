#!/usr/bin/env python3
"""
《自动控制原理》第5章 频域分析与校正 — 全部图表生成脚本
保存路径: E:/长安面试/自动控制原理/figures/
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy import signal
import os

# ========== 全局配置 ==========
OUT_DIR = r"E:\长安面试\自动控制原理\figures"
os.makedirs(OUT_DIR, exist_ok=True)

rcParams['font.family'] = ['Microsoft YaHei', 'SimHei', 'sans-serif']
rcParams['axes.unicode_minus'] = False
rcParams['figure.dpi'] = 150
rcParams['savefig.dpi'] = 150
rcParams['savefig.bbox'] = 'tight'
rcParams['lines.linewidth'] = 1.5

COLORS = ['#1a56db', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4']

# ============================================================
# 5.1 频率特性基本概念
# ============================================================

def fig5_1_sine_response():
    """正弦输入及其稳态输出响应"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    t = np.linspace(0, 10, 1000)
    w = 2.0  # 频率
    u = np.sin(w * t)  # 输入
    # 模拟经过一阶惯性环节 G(s)=1/(s+1) 的稳态输出
    G_mag = 1 / np.sqrt(1 + w**2)
    G_phase = -np.arctan(w)
    y = G_mag * np.sin(w * t + G_phase)

    ax1.plot(t, u, color=COLORS[0], linewidth=2, label='输入 $r(t)=\\sin(\\omega t)$')
    ax1.set_ylabel('幅值', fontsize=12)
    ax1.set_title('正弦输入信号', fontsize=13, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-1.5, 1.5)

    ax2.plot(t, y, color=COLORS[1], linewidth=2, label=f'输出 $c(t)={G_mag:.2f}\\sin(\\omega t{G_phase:.2f})$')
    ax2.plot(t, u, color=COLORS[0], linewidth=1, alpha=0.4, linestyle='--', label='输入（对比）')
    ax2.set_xlabel('时间 $t$', fontsize=12)
    ax2.set_ylabel('幅值', fontsize=12)
    ax2.set_title('稳态输出响应（幅值衰减 + 相位滞后）', fontsize=13, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-1.5, 1.5)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_1_sine_response.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_1_sine_response.png')


# ============================================================
# 5.2 幅相频率特性（Nyquist图）— 典型环节
# ============================================================

def plot_nyquist_element(G_func, w_range, title, filename, xlim=None, ylim=None, annotations=None):
    """通用的Nyquist图绘制函数"""
    fig, ax = plt.subplots(figsize=(7, 7))

    w = np.logspace(w_range[0], w_range[1], 500)
    G = G_func(w)
    Re, Im = G.real, G.imag

    ax.plot(Re, Im, color=COLORS[0], linewidth=2)
    ax.scatter(Re[0], Im[0], color=COLORS[0], s=40, zorder=5, label=f'$\\omega \\to 0^+$')
    ax.scatter(Re[-1], Im[-1], color=COLORS[1], s=40, zorder=5, label=f'$\\omega \\to \\infty$')

    # 实轴、虚轴
    ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)

    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    ax.set_xlabel('实部 Re', fontsize=12)
    ax.set_ylabel('虚部 Im', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

    if annotations:
        for ann in annotations:
            ax.annotate(ann['text'], xy=ann['xy'], xytext=ann['xytext'],
                       arrowprops=dict(arrowstyle='->', color=COLORS[2]),
                       fontsize=10, color=COLORS[2])

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, filename), dpi=150)
    plt.close(fig)
    print(f'[OK] {filename}')


def fig5_2_nyquist_elements():
    """所有典型环节的Nyquist图汇总"""
    # ---- 比例环节 ----
    K = 2.0
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(K, 0, s=80, color=COLORS[0], zorder=5, edgecolors='white', linewidths=2)
    ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.set_xlim(-1, 3.5)
    ax.set_ylim(-2, 2)
    ax.set_xlabel('Re', fontsize=12)
    ax.set_ylabel('Im', fontsize=12)
    ax.set_title('比例环节 $G(s)=K$', fontsize=14, fontweight='bold')
    ax.annotate(f'$(K, 0)$ = ({K}, 0)', xy=(K, 0), xytext=(K+0.5, 0.8),
                arrowprops=dict(arrowstyle='->', color=COLORS[2]), fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_2a_nyquist_proportional.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_2a_nyquist_proportional.png')

    # ---- 积分环节 G(s)=1/s ----
    def G_int(w):
        s = 1j * w
        return 1 / s

    w = np.logspace(-2, 2, 500)
    G = G_int(w)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(G.real, G.imag, color=COLORS[0], linewidth=2)
    ax.scatter(G.real[0], G.imag[0], color=COLORS[0], s=40, zorder=5, label='$\\omega \\to 0^+$ (起点)')
    ax.scatter(G.real[-1], G.imag[-1], color=COLORS[1], s=40, zorder=5, label='$\\omega \\to \\infty$ (终点)')
    ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-5, 1)
    ax.set_xlabel('Re', fontsize=12)
    ax.set_ylabel('Im', fontsize=12)
    ax.set_title('积分环节 $G(s)=1/s$（负虚轴）', fontsize=14, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_2b_nyquist_integral.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_2b_nyquist_integral.png')

    # ---- 惯性环节 G(s)=1/(Ts+1), T=1 ----
    def G_inertia(w, T=1.0):
        s = 1j * w
        return 1 / (T * s + 1)

    w = np.logspace(-2, 2, 500)
    G = G_inertia(w)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(G.real, G.imag, color=COLORS[0], linewidth=2)
    ax.scatter(G.real[0], G.imag[0], color=COLORS[0], s=50, zorder=5, label='$\\omega = 0$ (起点: 1+j0)')
    ax.scatter(G.real[-1], G.imag[-1], color=COLORS[1], s=50, zorder=5, label='$\\omega \\to \\infty$ (终点: 原点)')

    # w=1 特殊点
    G1 = G_inertia(np.array([1.0]))
    ax.scatter(G1.real, G1.imag, color=COLORS[3], s=60, zorder=5, label='$\\omega = 1/T$ (半圆最低点)')

    ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-0.6, 0.2)
    ax.set_xlabel('Re', fontsize=12)
    ax.set_ylabel('Im', fontsize=12)
    ax.set_title('惯性环节 $G(s)=1/(Ts+1)$（半圆）', fontsize=14, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_2c_nyquist_inertia.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_2c_nyquist_inertia.png')

    # ---- 振荡环节 G(s)=1/(s^2+2ζs+1) 不同ζ对比 ----
    fig, ax = plt.subplots(figsize=(8, 8))
    zetas = [0.2, 0.4, 0.6, 0.8]
    for i, zeta in enumerate(zetas):
        def G_osc(w, z=zeta):
            s = 1j * w
            return 1 / (s**2 + 2*z*s + 1)
        w = np.logspace(-1.5, 2, 500)
        G = G_osc(w)
        ax.plot(G.real, G.imag, color=COLORS[i], linewidth=2, label=f'$\\zeta = {zeta}$')
        ax.scatter(G.real[0], G.imag[0], color=COLORS[i], s=30, zorder=5)

    ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.set_xlim(-0.6, 1.2)
    ax.set_ylim(-1.2, 0.3)
    ax.set_xlabel('Re', fontsize=12)
    ax.set_ylabel('Im', fontsize=12)
    ax.set_title('振荡环节 Nyquist 图（不同 $\\zeta$ 对比）', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_2d_nyquist_oscillation.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_2d_nyquist_oscillation.png')

    # ---- 时滞环节 G(s)=e^{-τs} ----
    def G_delay(w, tau=0.5):
        s = 1j * w
        return np.exp(-tau * s)

    w = np.linspace(0.01, 20, 500)
    G = G_delay(w)

    fig, ax = plt.subplots(figsize=(7, 7))
    # Draw unit circle for reference
    theta_c = np.linspace(0, 2*np.pi, 200)
    ax.plot(np.cos(theta_c), np.sin(theta_c), 'gray', linewidth=0.8, linestyle='--', alpha=0.5, label='单位圆')

    ax.plot(G.real, G.imag, color=COLORS[0], linewidth=2)
    ax.scatter(G.real[0], G.imag[0], color=COLORS[0], s=50, zorder=5, label='$\\omega = 0$')

    ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel('Re', fontsize=12)
    ax.set_ylabel('Im', fontsize=12)
    ax.set_title('时滞环节 $G(s)=e^{-\\tau s}$（单位圆上旋转）', fontsize=14, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_2e_nyquist_delay.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_2e_nyquist_delay.png')


# ============================================================
# 5.3 对数频率特性（Bode图）
# ============================================================

def bode_plot_element(w, mag_db, phase_deg, title, filename, mag_ylim=None,
                      annotations=None, extra_curves=None, legend_loc='best'):
    """通用Bode图绘制"""
    fig, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    ax_mag.semilogx(w, mag_db, color=COLORS[0], linewidth=2, label='幅频特性')
    ax_mag.set_ylabel('幅值 $L(\\omega)$ / dB', fontsize=12)
    ax_mag.set_title(title, fontsize=14, fontweight='bold')
    ax_mag.grid(True, alpha=0.3, which='both')
    if mag_ylim:
        ax_mag.set_ylim(mag_ylim)
    ax_mag.legend(loc=legend_loc, fontsize=9)

    ax_phase.semilogx(w, phase_deg, color=COLORS[1], linewidth=2, label='相频特性')
    ax_phase.set_xlabel('频率 $\\omega$ (rad/s)', fontsize=12)
    ax_phase.set_ylabel('相位 $\\varphi(\\omega)$ / °', fontsize=12)
    ax_phase.grid(True, alpha=0.3, which='both')
    ax_phase.legend(loc=legend_loc, fontsize=9)

    if annotations:
        for ann in annotations:
            if 'ax' in ann:
                target = ax_mag if ann['ax'] == 'mag' else ax_phase
            else:
                target = ax_mag
            target.annotate(ann['text'], xy=ann['xy'], xytext=ann.get('xytext', ann['xy']),
                          arrowprops=dict(arrowstyle='->', color='red', lw=1.2),
                          fontsize=ann.get('fontsize', 10), color='red')

    if extra_curves:
        for curve in extra_curves:
            target = ax_mag if curve.get('axes', 'mag') == 'mag' else ax_phase
            target.semilogx(w, curve['data'], color=curve.get('color', 'gray'),
                          linewidth=curve.get('linewidth', 1),
                          linestyle=curve.get('linestyle', '--'),
                          label=curve.get('label', ''))

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, filename), dpi=150)
    plt.close(fig)
    print(f'[OK] {filename}')


def fig5_3_bode_elements():
    """生成所有典型环节的Bode图"""
    w = np.logspace(-2, 3, 1000)

    # ---- 比例环节 K=10 ----
    K = 10
    mag_db = 20 * np.log10(K) * np.ones_like(w)
    phase_deg = np.zeros_like(w)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    ax1.semilogx(w, mag_db, color=COLORS[0], linewidth=2)
    ax1.set_ylabel('$L(\\omega)$ / dB', fontsize=12)
    ax1.set_title('比例环节 $G(s)=K$ ($K=10$, $20\\lg K = 20$ dB)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.set_ylim(10, 30)
    ax2.semilogx(w, phase_deg, color=COLORS[1], linewidth=2)
    ax2.set_xlabel('$\\omega$ (rad/s)', fontsize=12)
    ax2.set_ylabel('$\\varphi(\\omega)$ / °', fontsize=12)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.set_ylim(-10, 10)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_3a_bode_proportional.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_3a_bode_proportional.png')

    # ---- 积分环节 G(s)=1/s ----
    mag_db = 20 * np.log10(1 / w)
    phase_deg = -90 * np.ones_like(w)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    ax1.semilogx(w, mag_db, color=COLORS[0], linewidth=2, label='$-20$ dB/dec')
    ax1.axvline(x=1, color='red', linewidth=1, linestyle='--', alpha=0.5)
    ax1.annotate('$\\omega=1$, 0 dB', xy=(1, 0), xytext=(3, 10),
                arrowprops=dict(arrowstyle='->', color='red'), fontsize=10, color='red')
    ax1.set_ylabel('$L(\\omega)$ / dB', fontsize=12)
    ax1.set_title('积分环节 $G(s)=1/s$（斜率 $-20$ dB/dec）', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.legend(fontsize=10)
    ax2.semilogx(w, phase_deg, color=COLORS[1], linewidth=2)
    ax2.set_xlabel('$\\omega$ (rad/s)', fontsize=12)
    ax2.set_ylabel('$\\varphi(\\omega)$ / °', fontsize=12)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.set_ylim(-100, -80)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_3b_bode_integral.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_3b_bode_integral.png')

    # ---- 惯性环节 G(s)=1/(Ts+1) T=1 ----
    T = 1.0
    mag_db = 20 * np.log10(1 / np.sqrt(1 + (w*T)**2))
    phase_deg = np.degrees(-np.arctan(w*T))

    # 渐近线
    w_asy = np.logspace(-2, 3, 1000)
    mag_asy = np.where(w_asy <= 1/T, 0, -20 * np.log10(w_asy * T))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    ax1.semilogx(w, mag_db, color=COLORS[0], linewidth=2, label='实际曲线')
    ax1.semilogx(w_asy, mag_asy, color='gray', linewidth=1.2, linestyle='--', label='渐近线')
    ax1.axvline(x=1/T, color='red', linewidth=1, linestyle=':', alpha=0.6)
    ax1.annotate(f'转折频率 $\\omega_T=1/T$', xy=(1/T, -3), xytext=(3, 5),
                arrowprops=dict(arrowstyle='->', color='red'), fontsize=10, color='red')
    ax1.annotate('精确曲线在转折频率处\n低约 3 dB', xy=(1, -3), xytext=(0.15, -15),
                arrowprops=dict(arrowstyle='->', color=COLORS[3]), fontsize=9, color=COLORS[3])
    ax1.set_ylabel('$L(\\omega)$ / dB', fontsize=12)
    ax1.set_title('惯性环节 $G(s)=1/(Ts+1)$ ($T=1$)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.legend(fontsize=9)
    ax1.set_ylim(-40, 5)

    ax2.semilogx(w, phase_deg, color=COLORS[1], linewidth=2)
    ax2.axhline(y=-45, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax2.axvline(x=1/T, color='red', linewidth=1, linestyle=':', alpha=0.6)
    ax2.annotate(f'$\\omega=1/T$, $\\varphi=-45°$', xy=(1, -45), xytext=(3, -20),
                arrowprops=dict(arrowstyle='->', color='red'), fontsize=10, color='red')
    ax2.set_xlabel('$\\omega$ (rad/s)', fontsize=12)
    ax2.set_ylabel('$\\varphi(\\omega)$ / °', fontsize=12)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.set_ylim(-100, 5)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_3c_bode_inertia.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_3c_bode_inertia.png')

    # ---- 振荡环节 G(s)=1/(s^2+2ζs+1) 不同ζ ----
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    zetas = [0.1, 0.3, 0.5, 0.7, 1.0]
    for i, zeta in enumerate(zetas):
        mag_db = 20 * np.log10(1 / np.sqrt((1 - w**2)**2 + (2*zeta*w)**2))
        # Phase computation avoiding division by zero
        phase = np.where(w > 0, -np.arctan2(2*zeta*w, 1 - w**2), 0)
        phase_deg = np.degrees(phase)
        # Unwrap phase
        phase_deg = np.unwrap(np.radians(phase_deg))
        # Better: manual phase
        denom = 1 - w**2
        numer = 2 * zeta * w
        phase_rad = np.arctan2(numer, denom)
        # arctan2 gives [0, π] in upper and [-π, 0] in lower
        phase_deg = -np.degrees(np.arctan2(2*zeta*w, 1 - w**2))

        ax1.semilogx(w, mag_db, color=COLORS[i], linewidth=2, label=f'$\\zeta={zeta}$')
        ax2.semilogx(w, phase_deg, color=COLORS[i], linewidth=2, label=f'$\\zeta={zeta}$')

    ax1.set_ylabel('$L(\\omega)$ / dB', fontsize=12)
    ax1.set_title('振荡环节 $G(s)=1/(s^2+2\\zeta s+1)$（不同阻尼比）', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.legend(fontsize=9, ncol=3)
    ax1.set_ylim(-40, 20)

    ax2.set_xlabel('$\\omega$ (rad/s)', fontsize=12)
    ax2.set_ylabel('$\\varphi(\\omega)$ / °', fontsize=12)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.legend(fontsize=9, ncol=3)
    ax2.set_ylim(-200, 10)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_3d_bode_oscillation.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_3d_bode_oscillation.png')

    # ---- 时滞环节 G(s)=e^{-τs} τ=0.5 ----
    tau = 0.5
    mag_db = np.zeros_like(w)
    phase_deg = -np.degrees(w * tau)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    ax1.semilogx(w, mag_db, color=COLORS[0], linewidth=2)
    ax1.set_ylabel('$L(\\omega)$ / dB', fontsize=12)
    ax1.set_title(f'时滞环节 $G(s)=e^{{-\\tau s}}$ ($\\tau={tau}$)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.set_ylim(-5, 5)

    ax2.semilogx(w, phase_deg, color=COLORS[1], linewidth=2)
    ax2.annotate('相位随频率不断滞后\n最终趋向 $-\\infty$', xy=(5, -200), xytext=(15, -150),
                arrowprops=dict(arrowstyle='->', color='red'), fontsize=10, color='red')
    ax2.set_xlabel('$\\omega$ (rad/s)', fontsize=12)
    ax2.set_ylabel('$\\varphi(\\omega)$ / °', fontsize=12)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.set_ylim(-320, 20)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_3e_bode_delay.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_3e_bode_delay.png')

    # ---- 微分环节 G(s)=s ----
    mag_db = 20 * np.log10(w)
    phase_deg = 90 * np.ones_like(w)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    ax1.semilogx(w, mag_db, color=COLORS[0], linewidth=2, label='$+20$ dB/dec')
    ax1.axvline(x=1, color='red', linewidth=1, linestyle='--', alpha=0.5)
    ax1.annotate('$\\omega=1$, 0 dB', xy=(1, 0), xytext=(3, 10),
                arrowprops=dict(arrowstyle='->', color='red'), fontsize=10, color='red')
    ax1.set_ylabel('$L(\\omega)$ / dB', fontsize=12)
    ax1.set_title('微分环节 $G(s)=s$（斜率 $+20$ dB/dec）', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.legend(fontsize=10)
    ax2.semilogx(w, phase_deg, color=COLORS[1], linewidth=2)
    ax2.set_xlabel('$\\omega$ (rad/s)', fontsize=12)
    ax2.set_ylabel('$\\varphi(\\omega)$ / °', fontsize=12)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.set_ylim(80, 100)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_3f_bode_derivative.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_3f_bode_derivative.png')


def fig5_3_openloop_bode_construction():
    """开环系统Bode图绘制步骤（渐近线法）"""
    # 例子: G(s)H(s) = 10(s+1) / [s(s+10)]
    # 解析为: 10 * (1/10) * (s+1) / [s * (s/10+1)]
    #        = 1 * (s+1) / [s * (s/10+1)]
    # 各环节:
    #   K=1 → 0 dB
    #   积分 1/s → -20 dB/dec, 过0dB at ω=1
    #   一阶微分 (s+1) → +1 零点在 ω=1, 斜率+20 dB/dec
    #   惯性 1/(s/10+1) → 转折 ω=10, 斜率-20 dB/dec

    w = np.logspace(-1, 3, 2000)

    # Exact
    s = 1j * w
    G_exact = 10 * (s + 1) / (s * (s + 10))
    mag_exact = 20 * np.log10(np.abs(G_exact))
    phase_exact = np.degrees(np.angle(G_exact))

    # Asymptotes
    mag_asy = np.zeros_like(w)
    # Integrator: -20 dB/dec, =0 at ω=1
    # After ω=1: +20 dB/dec from zero
    # After ω=10: -20 dB/dec from pole (net 0)

    for i, wi in enumerate(w):
        if wi < 1:
            mag_asy[i] = 0 - 20 * np.log10(wi)  # only integrator
        elif wi < 10:
            mag_asy[i] = 0 - 20 * np.log10(wi) + 20 * np.log10(wi/1)  # integrator + zero
        else:
            mag_asy[i] = 0 - 20 * np.log10(wi) + 20 * np.log10(wi/1) - 20 * np.log10(wi/10)

    phase_asy = np.zeros_like(w)
    for i, wi in enumerate(w):
        p = -90  # integrator
        p += np.degrees(np.arctan(wi/1))  # zero at ω=1
        p -= np.degrees(np.arctan(wi/10))  # pole at ω=10
        phase_asy[i] = p

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

    ax1.semilogx(w, mag_exact, color=COLORS[0], linewidth=2, label='精确曲线')
    ax1.semilogx(w, mag_asy, color=COLORS[3], linewidth=1.5, linestyle='--', label='渐近线')
    ax1.axvline(x=1, color='red', linewidth=1, linestyle=':', alpha=0.6)
    ax1.axvline(x=10, color='red', linewidth=1, linestyle=':', alpha=0.6)
    ax1.annotate('$\\omega_1=1$ (零点)', xy=(1, -15), xytext=(0.3, -30),
                arrowprops=dict(arrowstyle='->', color='red'), fontsize=10, color='red')
    ax1.annotate('$\\omega_2=10$ (极点)', xy=(10, -15), xytext=(20, -30),
                arrowprops=dict(arrowstyle='->', color='red'), fontsize=10, color='red')
    ax1.set_ylabel('$L(\\omega)$ / dB', fontsize=12)
    ax1.set_title('开环Bode图绘制 — 渐近线法示例\n$G(s)H(s) = \\frac{10(s+1)}{s(s+10)}$',
                 fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.legend(fontsize=10)

    ax2.semilogx(w, phase_exact, color=COLORS[1], linewidth=2, label='精确曲线')
    ax2.semilogx(w, phase_asy, color=COLORS[3], linewidth=1.5, linestyle='--', label='渐近线')
    ax2.axhline(y=-90, color='gray', linewidth=0.8, linestyle=':', alpha=0.5)
    ax2.axhline(y=-180, color='gray', linewidth=0.8, linestyle=':', alpha=0.5)
    ax2.set_xlabel('$\\omega$ (rad/s)', fontsize=12)
    ax2.set_ylabel('$\\varphi(\\omega)$ / °', fontsize=12)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.legend(fontsize=10)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_3g_openloop_bode_construction.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_3g_openloop_bode_construction.png')


def fig5_3_minphase_comparison():
    """最小相位系统 vs 非最小相位系统"""
    w = np.logspace(-1, 2, 1000)

    # 最小相位: G1(s) = (s+1)/(s+2) → 零点在-1, 极点在-2
    s = 1j * w
    G1 = (s + 1) / (s + 2)
    mag1 = 20 * np.log10(np.abs(G1))
    phase1 = np.degrees(np.angle(G1))

    # 非最小相位: G2(s) = (-s+1)/(s+2) → 零点在+1 (右半平面)
    G2 = (-s + 1) / (s + 2)
    mag2 = 20 * np.log10(np.abs(G2))
    phase2 = np.degrees(np.angle(G2))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    ax1.semilogx(w, mag1, color=COLORS[0], linewidth=2, label='最小相位: $G(s)=\\dfrac{s+1}{s+2}$')
    ax1.semilogx(w, mag2, color=COLORS[1], linewidth=2, linestyle='--', label='非最小相位: $G(s)=\\dfrac{-s+1}{s+2}$')
    ax1.set_ylabel('$L(\\omega)$ / dB', fontsize=12)
    ax1.set_title('最小相位系统 vs 非最小相位系统（幅频相同，相频不同）', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.legend(fontsize=10)
    ax1.set_ylim(-25, 5)

    ax2.semilogx(w, phase1, color=COLORS[0], linewidth=2, label='最小相位: 相位滞后少')
    ax2.semilogx(w, phase2, color=COLORS[1], linewidth=2, linestyle='--', label='非最小相位: 相位滞后多')
    ax2.set_xlabel('$\\omega$ (rad/s)', fontsize=12)
    ax2.set_ylabel('$\\varphi(\\omega)$ / °', fontsize=12)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.legend(fontsize=10)
    ax2.set_ylim(-200, 50)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_3h_minphase_comparison.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_3h_minphase_comparison.png')


# ============================================================
# 5.4 频域稳定判据 — Nyquist
# ============================================================

def fig5_4_nyquist_criterion():
    """奈奎斯特稳定判据示意图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5))

    # --- 左图: s平面的Nyquist围线 ---
    # Draw the D-contour
    theta = np.linspace(-np.pi/2, np.pi/2, 200)
    R = 5  # Large radius
    x_semicircle = R * np.cos(theta)
    y_semicircle = R * np.sin(theta)

    # Small semicircle around origin (for integrator)
    r = 0.3
    theta_small = np.linspace(np.pi/2, -np.pi/2, 100)
    x_small = r * np.cos(theta_small)
    y_small = r * np.sin(theta_small)

    # Imaginary axis
    ax1.plot([0, 0], [-R, -r], 'b-', linewidth=2)  # negative imag
    ax1.plot([0, 0], [r, R], 'b-', linewidth=2)    # positive imag

    # Semicircles
    ax1.plot(x_semicircle, y_semicircle, 'b-', linewidth=2, label='Nyquist围线 $D$')
    ax1.plot(x_small, y_small, 'b-', linewidth=2)

    # Arrows
    ax1.annotate('', xy=(0, 3), xytext=(0, 1), arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax1.annotate('', xy=(-3, 0), xytext=(-5, 0), arrowprops=dict(arrowstyle='->', color='blue', lw=2))

    # Mark poles
    ax1.scatter([-1, -2], [0, 0], s=80, marker='x', color='red', linewidths=2, zorder=5)
    ax1.annotate('极点', xy=(-1, 0), xytext=(-1, 1.2), fontsize=10, color='red',
                ha='center', arrowprops=dict(arrowstyle='->', color='red'))

    ax1.set_xlim(-5.5, 1.5)
    ax1.set_ylim(-5.5, 5.5)
    ax1.set_xlabel('Re', fontsize=12)
    ax1.set_ylabel('Im', fontsize=12)
    ax1.set_title('$s$ 平面 — Nyquist围线', fontsize=14, fontweight='bold')
    ax1.axhline(y=0, color='gray', linewidth=0.5, alpha=0.3)
    ax1.axvline(x=0, color='gray', linewidth=0.5, alpha=0.3)
    ax1.grid(True, alpha=0.2)
    ax1.set_aspect('equal')
    ax1.legend(fontsize=9)

    # --- 右图: G(s)平面的Nyquist图 ---
    # Example: G(s) = 2/(s+1)(s+2), H(s)=1
    def G_nyq(w):
        s = 1j * w
        return 2 / ((s + 1) * (s + 2))

    w = np.logspace(-2, 3, 1000)
    G = G_nyq(w)

    ax2.plot(G.real, G.imag, 'b-', linewidth=2)
    ax2.scatter(G.real[0], G.imag[0], s=60, color=COLORS[0], zorder=5, label='$\\omega=0$')
    ax2.scatter(0, 0, s=60, color=COLORS[1], zorder=5, label='$\\omega\\to\\infty$')

    # (-1, j0) point
    ax2.scatter(-1, 0, s=100, marker='*', color='red', zorder=5, edgecolors='darkred', linewidths=1.5)
    ax2.annotate('$(-1, j0)$\n临界点', xy=(-1, 0), xytext=(-1.5, 0.8),
                fontsize=11, color='red', ha='center', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='red'))

    ax2.axhline(y=0, color='gray', linewidth=0.5, alpha=0.3)
    ax2.axvline(x=0, color='gray', linewidth=0.5, alpha=0.3)
    ax2.set_xlim(-0.2, 1.2)
    ax2.set_ylim(-0.7, 0.7)
    ax2.set_xlabel('Re', fontsize=12)
    ax2.set_ylabel('Im', fontsize=12)
    ax2.set_title('$GH$ 平面 — Nyquist曲线\n$G(s)=\\frac{2}{(s+1)(s+2)}$', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_4a_nyquist_criterion.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_4a_nyquist_criterion.png')


def fig5_4_nyquist_with_integrator():
    """含积分环节的Nyquist图处理"""
    # G(s) = K/[s(T1s+1)(T2s+1)]
    # Open-loop has a pole at origin → need to handle the "infinite semicircle"

    fig, ax = plt.subplots(figsize=(9, 8))

    K = 2
    T1, T2 = 1.0, 0.5

    # Positive ω part
    w_pos = np.logspace(-3, 3, 2000)
    s_pos = 1j * w_pos
    G_pos = K / (s_pos * (T1 * s_pos + 1) * (T2 * s_pos + 1))

    # Negative ω part (symmetric)
    w_neg = np.logspace(3, -3, 2000)
    s_neg = -1j * w_neg
    G_neg = K / (s_neg * (T1 * s_neg + 1) * (T2 * s_neg + 1))

    # Small semicircle: s = ε * e^{jθ}, θ from -π/2 to π/2
    eps = 1e-2
    theta_small = np.linspace(-np.pi/2, np.pi/2, 500)
    s_small = eps * np.exp(1j * theta_small)
    G_small = K / (s_small * (T1 * s_small + 1) * (T2 * s_small + 1))

    ax.plot(G_pos.real, G_pos.imag, color=COLORS[0], linewidth=2, label='$\\omega=0^+ \\to +\\infty$')
    ax.plot(G_neg.real, G_neg.imag, color=COLORS[1], linewidth=1.5, linestyle='--', label='$\\omega=-\\infty \\to 0^-$')
    ax.plot(G_small.real, G_small.imag, color=COLORS[3], linewidth=2.5, label='小半圆（绕过原点极点）')

    # (-1, j0)
    ax.scatter(-1, 0, s=120, marker='*', color='red', zorder=6, edgecolors='darkred', linewidths=2)
    ax.annotate('$(-1, j0)$', xy=(-1, 0), xytext=(-1.3, 0.5), fontsize=12, color='red', fontweight='bold')

    ax.axhline(y=0, color='gray', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='gray', linewidth=0.5, alpha=0.3)
    ax.set_xlabel('Re', fontsize=12)
    ax.set_ylabel('Im', fontsize=12)
    ax.set_title('含积分环节的 Nyquist 图\n$G(s)=\\frac{K}{s(T_1 s+1)(T_2 s+1)}$', fontsize=14, fontweight='bold')
    ax.legend(fontsize=9, loc='lower left')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.set_xlim(-3, 2)
    ax.set_ylim(-3, 1)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_4b_nyquist_with_integrator.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_4b_nyquist_with_integrator.png')


# ============================================================
# 5.5 稳定裕度
# ============================================================

def fig5_5_stability_margins():
    """稳定裕度在Bode图和Nyquist图上的标注"""
    w = np.logspace(-2, 1.5, 2000)

    # Example system: G(s) = 5/[s(s+1)(0.5s+1)]
    # ω_c ≈ 2 rad/s, PM ≈ 30°, ω_g ≈ 2.8 rad/s, GM ≈ 6 dB
    s = 1j * w
    G = 5 / (s * (s + 1) * (0.5 * s + 1))
    mag_db = 20 * np.log10(np.abs(G))
    phase_deg = np.degrees(np.angle(G))
    # Unwrap for proper visualization
    phase_deg = -180 - np.degrees(np.arctan2(w, 0) - np.arctan2(0, 1) + 0)  # won't work easily

    # Recalculate phase carefully
    phase_rad = np.angle(G)
    phase_deg = np.degrees(phase_rad)

    # Find crossover frequencies numerically
    # Gain crossover: |G| = 1 (0 dB)
    mag_abs = np.abs(G)
    idx_gc = np.argmin(np.abs(mag_abs - 1.0))
    w_gc = w[idx_gc]
    pm = 180 + phase_deg[idx_gc]

    # Phase crossover: phase = -180°
    # Find where phase crosses -180
    phase_wrapped = phase_deg.copy()
    idx_pc = np.argmin(np.abs(phase_wrapped + 180))
    w_pc = w[idx_pc]
    gm_db = -mag_db[idx_pc]

    # --- Bode plot with margins ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

    ax1.semilogx(w, mag_db, color=COLORS[0], linewidth=2)
    ax1.axvline(x=w_gc, color=COLORS[2], linewidth=1.2, linestyle='--')
    ax1.axvline(x=w_pc, color=COLORS[3], linewidth=1.2, linestyle='--')
    ax1.axhline(y=0, color='gray', linewidth=0.8, linestyle=':', alpha=0.5)

    # GM annotation
    ax1.annotate('', xy=(w_pc, 0), xytext=(w_pc, -mag_db[idx_pc]),
                arrowprops=dict(arrowstyle='<->', color=COLORS[3], lw=2))
    ax1.annotate(f'幅值裕度\n$K_g = {gm_db:.1f}$ dB', xy=(w_pc, -mag_db[idx_pc]/2),
                xytext=(w_pc*2, -mag_db[idx_pc]/2), fontsize=11, color=COLORS[3], fontweight='bold')
    ax1.annotate(f'$\\omega_c = {w_gc:.2f}$', xy=(w_gc, 0), xytext=(w_gc*0.7, -15),
                fontsize=10, color=COLORS[2])
    ax1.annotate(f'$\\omega_g = {w_pc:.2f}$', xy=(w_pc, 0), xytext=(w_pc*1.3, -25),
                fontsize=10, color=COLORS[3])

    ax1.set_ylabel('$L(\\omega)$ / dB', fontsize=12)
    ax1.set_title('稳定裕度 — Bode 图\n$G(s)=\\frac{5}{s(s+1)(0.5s+1)}$', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, which='both')

    # Phase
    ax2.semilogx(w, phase_deg, color=COLORS[1], linewidth=2)
    ax2.axhline(y=-180, color='gray', linewidth=0.8, linestyle=':', alpha=0.5)
    ax2.axvline(x=w_gc, color=COLORS[2], linewidth=1.2, linestyle='--')
    ax2.axvline(x=w_pc, color=COLORS[3], linewidth=1.2, linestyle='--')

    # PM annotation
    ax2.annotate('', xy=(w_gc, -180), xytext=(w_gc, phase_deg[idx_gc]),
                arrowprops=dict(arrowstyle='<->', color=COLORS[2], lw=2))
    ax2.annotate(f'相位裕度\n$\\gamma = {pm:.1f}°$', xy=(w_gc, (phase_deg[idx_gc] - 180)/2),
                xytext=(w_gc*0.3, (phase_deg[idx_gc] - 180)/2 + 15), fontsize=11, color=COLORS[2], fontweight='bold')

    ax2.set_xlabel('$\\omega$ (rad/s)', fontsize=12)
    ax2.set_ylabel('$\\varphi(\\omega)$ / °', fontsize=12)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.set_ylim(-280, 0)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_5a_stability_margins_bode.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_5a_stability_margins_bode.png')

    # --- Nyquist plot with margins ---
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.plot(G.real, G.imag, color=COLORS[0], linewidth=2)

    # Unit circle
    theta_uc = np.linspace(0, 2*np.pi, 300)
    ax.plot(np.cos(theta_uc), np.sin(theta_uc), 'gray', linewidth=0.8, linestyle='--', alpha=0.5, label='单位圆')

    # (-1, j0)
    ax.scatter(-1, 0, s=100, marker='*', color='red', zorder=5)
    ax.annotate('$(-1, j0)$', xy=(-1, 0), xytext=(-1.2, 0.2), fontsize=12, color='red', fontweight='bold')

    # Mark ω_gc (gain crossover) = intersection with unit circle
    ax.scatter(G[idx_gc].real, G[idx_gc].imag, s=70, color=COLORS[2], zorder=5)
    ax.annotate(f'$\\omega_c$, PM$={pm:.1f}°$', xy=(G[idx_gc].real, G[idx_gc].imag),
                xytext=(G[idx_gc].real+0.15, G[idx_gc].imag+0.15),
                fontsize=10, color=COLORS[2], fontweight='bold')

    # Mark ω_pc (phase crossover) = intersection with negative real axis
    ax.scatter(G[idx_pc].real, G[idx_pc].imag, s=70, color=COLORS[3], zorder=5)
    ax.annotate(f'$\\omega_g$, GM$={gm_db:.1f}$ dB', xy=(G[idx_pc].real, G[idx_pc].imag),
                xytext=(G[idx_pc].real-0.3, G[idx_pc].imag-0.3),
                fontsize=10, color=COLORS[3], fontweight='bold')

    ax.axhline(y=0, color='gray', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='gray', linewidth=0.5, alpha=0.3)
    ax.set_xlabel('Re', fontsize=12)
    ax.set_ylabel('Im', fontsize=12)
    ax.set_title('稳定裕度 — Nyquist 图', fontsize=14, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-1.8, 1.2)
    ax.set_ylim(-2.5, 0.5)
    ax.set_aspect('equal')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_5b_stability_margins_nyquist.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_5b_stability_margins_nyquist.png')


# ============================================================
# 5.6 开环频率特性分析系统性能
# ============================================================

def fig5_6_openloop_freq_regions():
    """开环对数幅频特性的三个频段"""
    w = np.logspace(-3, 4, 3000)

    # Example: Typical well-designed system
    # Low freq: -40 dB/dec (type 2) → high gain for accuracy
    # Mid freq: -20 dB/dec through crossover → good stability
    # High freq: -60 dB/dec → noise rejection

    # Construct piecewise:
    # ω < 1: -40 dB/dec, starting from 40dB at ω=0.01
    # 1 < ω < 3: -20 dB/dec (correction from zero)
    # ω > 3: -60 dB/dec (two poles)

    mag_db = np.zeros_like(w)
    for i, wi in enumerate(w):
        if wi < 1:
            mag_db[i] = 40 - 40 * np.log10(wi/0.01)  # -40 dB/dec from ω=0.01
        elif wi < 3:
            mag_db[i] = 40 - 40 * np.log10(1/0.01) - 20 * np.log10(wi/1)  # -20 dB/dec from ω=1
        else:
            mag_db[i] = 40 - 40 * np.log10(1/0.01) - 20 * np.log10(3/1) - 60 * np.log10(wi/3)

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.semilogx(w, mag_db, color=COLORS[0], linewidth=2.5)
    ax.axhline(y=0, color='red', linewidth=1, linestyle='--', alpha=0.6)

    # Crossover
    # Find crossover
    idx_cross = np.argmin(np.abs(mag_db))
    w_cross = w[idx_cross]
    ax.axvline(x=w_cross, color='red', linewidth=1, linestyle=':', alpha=0.5)
    ax.scatter(w_cross, 0, s=60, color='red', zorder=5)
    ax.annotate(f'穿越频率 $\\omega_c \\approx {w_cross:.1f}$', xy=(w_cross, 0),
                xytext=(w_cross*3, 10), fontsize=11, color='red', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='red'))

    # Region annotations
    # Low freq
    ax.axvspan(0.001, 0.8, alpha=0.1, color=COLORS[0])
    ax.annotate('低频段\n决定稳态精度\n斜率越陡、增益越高\n→ 误差越小',
                xy=(0.05, 30), fontsize=11, color=COLORS[0], fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#dbeafe', alpha=0.8))

    # Mid freq
    ax.axvspan(0.8, 8, alpha=0.1, color=COLORS[2])
    ax.annotate('中频段\n决定动态性能\n穿越频率 → 快速性\n相位裕度 → 超调量',
                xy=(1.8, -10), fontsize=11, color=COLORS[2], fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#d1fae5', alpha=0.8))

    # High freq
    ax.axvspan(8, 10000, alpha=0.1, color=COLORS[3])
    ax.annotate('高频段\n决定抗干扰能力\n衰减越快 → 噪声抑制越好',
                xy=(50, -30), fontsize=11, color=COLORS[3], fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#fef3c7', alpha=0.8))

    ax.set_xlabel('$\\omega$ (rad/s)', fontsize=13)
    ax.set_ylabel('$L(\\omega)$ / dB', fontsize=13)
    ax.set_title('开环对数幅频特性 — 三频段分析', fontsize=15, fontweight='bold')
    ax.grid(True, alpha=0.3, which='both')
    ax.set_ylim(-60, 50)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_6_openloop_freq_regions.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_6_openloop_freq_regions.png')


# ============================================================
# 5.7-5.8 闭环频率特性
# ============================================================

def fig5_7_closed_loop_response():
    """闭环频率特性特征量"""
    w = np.logspace(-2, 1.5, 2000)

    # Open loop: G(s) = ω_n^2/(s^2 + 2ζω_n s)  (unity feedback)
    # Closed loop: T(s) = G/(1+G) = ω_n^2/(s^2 + 2ζω_n s + ω_n^2)

    omega_n = 1.0
    zetas = [0.3, 0.5, 0.7]

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, zeta in enumerate(zetas):
        s = 1j * w
        T = omega_n**2 / (s**2 + 2*zeta*omega_n*s + omega_n**2)
        mag = np.abs(T)
        mag_db = 20 * np.log10(mag)

        # Find resonant peak
        if zeta < 1/np.sqrt(2):
            wr = omega_n * np.sqrt(1 - 2*zeta**2)
            Mr = 1 / (2*zeta * np.sqrt(1 - zeta**2))
        else:
            wr = 0
            Mr = 1

        ax.semilogx(w, mag_db, color=COLORS[i], linewidth=2, label=f'$\\zeta={zeta}$')

        if zeta < 1/np.sqrt(2):
            ax.axhline(y=20*np.log10(Mr), color=COLORS[i], linewidth=0.8, linestyle=':', alpha=0.5)
            ax.scatter(wr, 20*np.log10(Mr), color=COLORS[i], s=60, zorder=5)
            ax.annotate(f'$M_r={Mr:.2f}$\n$\\omega_r={wr:.2f}$',
                       xy=(wr, 20*np.log10(Mr)), xytext=(wr*2, 20*np.log10(Mr)+3),
                       fontsize=9, color=COLORS[i])

    # Bandwidth: M = 0.707 (-3 dB)
    ax.axhline(y=-3, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.annotate('$-3$ dB\n(带宽)', xy=(3, -3), fontsize=10, color='gray')

    # Zero frequency
    ax.axvline(x=w[0], color='gray', linewidth=0.5, linestyle=':', alpha=0.3)
    ax.annotate('$M(0)$\n零频值', xy=(0.02, 0), fontsize=10, color=COLORS[0])

    ax.set_xlabel('$\\omega$ (rad/s)', fontsize=12)
    ax.set_ylabel('$M(\\omega)$ / dB', fontsize=12)
    ax.set_title('闭环频率特性 — 谐振峰值 $M_r$ 与带宽 $\\omega_b$\n$T(s)=\\frac{\\omega_n^2}{s^2+2\\zeta\\omega_n s+\\omega_n^2}$',
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, which='both')
    ax.legend(fontsize=10)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_7_closed_loop_response.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_7_closed_loop_response.png')


# ============================================================
# 5.9 串联校正
# ============================================================

def fig5_9_lead_lag_comparison():
    """超前校正 vs 滞后校正 Bode图对比"""
    w = np.logspace(-2, 3, 2000)

    # Lead compensator: G_c(s) = (αTs+1)/(Ts+1), α>1
    # Parameters: α=10, T=0.1 → zero at 1, pole at 10
    T_lead = 0.1
    alpha = 10
    s = 1j * w
    G_lead = (alpha * T_lead * s + 1) / (T_lead * s + 1)
    mag_lead = 20 * np.log10(np.abs(G_lead))
    phase_lead = np.degrees(np.angle(G_lead))

    # Lag compensator: G_c(s) = (Ts+1)/(βTs+1), β>1
    T_lag = 1.0
    beta = 10
    G_lag = (T_lag * s + 1) / (beta * T_lag * s + 1)
    mag_lag = 20 * np.log10(np.abs(G_lag))
    phase_lag = np.degrees(np.angle(G_lag))

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    (ax1, ax2), (ax3, ax4) = axes

    # --- Lead - Magnitude ---
    ax1.semilogx(w, mag_lead, color=COLORS[0], linewidth=2)
    ax1.axhline(y=0, color='gray', linewidth=0.5, linestyle=':', alpha=0.5)
    ax1.axhline(y=20*np.log10(alpha), color='red', linewidth=0.8, linestyle='--', alpha=0.4)
    ax1.axvline(x=1/(alpha*T_lead), color='red', linewidth=0.8, linestyle=':', alpha=0.5)
    ax1.axvline(x=1/T_lead, color='red', linewidth=0.8, linestyle=':', alpha=0.5)
    ax1.annotate(f'$\\omega_1=1/(\\alpha T)$', xy=(1/(alpha*T_lead), 0),
                xytext=(0.05, -8), fontsize=8, color='red')
    ax1.annotate(f'$\\omega_2=1/T$', xy=(1/T_lead, 0),
                xytext=(15, -8), fontsize=8, color='red')
    ax1.set_ylabel('$L(\\omega)$ / dB', fontsize=11)
    ax1.set_title(f'超前校正 $G_c(s)=\\frac{{\\alpha Ts+1}}{{Ts+1}}$ ($\\alpha={alpha}$, $T={T_lead}$)\n最大相角 $\\phi_m = \\arcsin\\frac{{\\alpha-1}}{{\\alpha+1}} = {np.degrees(np.arcsin((alpha-1)/(alpha+1))):.1f}°$',
                 fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, which='both')

    # --- Lead - Phase ---
    ax2.semilogx(w, phase_lead, color=COLORS[0], linewidth=2)
    ax2.axhline(y=0, color='gray', linewidth=0.5, linestyle=':', alpha=0.5)
    # Max phase
    w_m = 1 / (T_lead * np.sqrt(alpha))
    phi_m = np.degrees(np.arcsin((alpha-1)/(alpha+1)))
    ax2.axvline(x=w_m, color='red', linewidth=0.8, linestyle=':', alpha=0.5)
    ax2.scatter(w_m, phi_m, s=60, color='red', zorder=5)
    ax2.annotate(f'$\\omega_m$\n$\\phi_m={phi_m:.1f}°$', xy=(w_m, phi_m),
                xytext=(w_m*4, phi_m-15), fontsize=9, color='red',
                arrowprops=dict(arrowstyle='->', color='red'))
    ax2.set_xlabel('$\\omega$ (rad/s)', fontsize=11)
    ax2.set_ylabel('$\\varphi(\\omega)$ / °', fontsize=11)
    ax2.set_title('超前校正 — 相位超前（正相角）', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, which='both')
    ax2.set_ylim(-5, 60)

    # --- Lag - Magnitude ---
    ax3.semilogx(w, mag_lag, color=COLORS[1], linewidth=2)
    ax3.axhline(y=0, color='gray', linewidth=0.5, linestyle=':', alpha=0.5)
    ax3.axhline(y=-20*np.log10(beta), color='red', linewidth=0.8, linestyle='--', alpha=0.4)
    ax3.axvline(x=1/(beta*T_lag), color='red', linewidth=0.8, linestyle=':', alpha=0.5)
    ax3.axvline(x=1/T_lag, color='red', linewidth=0.8, linestyle=':', alpha=0.5)
    ax3.annotate(f'$\\omega_1=1/(\\beta T)$', xy=(1/(beta*T_lag), 0),
                xytext=(0.05, -5), fontsize=8, color='red')
    ax3.annotate(f'$\\omega_2=1/T$', xy=(1/T_lag, 0),
                xytext=(1.5, -5), fontsize=8, color='red')
    ax3.set_ylabel('$L(\\omega)$ / dB', fontsize=11)
    ax3.set_title(f'滞后校正 $G_c(s)=\\frac{{Ts+1}}{{\\beta Ts+1}}$ ($\\beta={beta}$, $T={T_lag}$)\n最大衰减 $20\\lg\\beta = {20*np.log10(beta):.1f}$ dB',
                 fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3, which='both')

    # --- Lag - Phase ---
    ax4.semilogx(w, phase_lag, color=COLORS[1], linewidth=2)
    ax4.axhline(y=0, color='gray', linewidth=0.5, linestyle=':', alpha=0.5)
    w_m_lag = 1 / (T_lag * np.sqrt(beta))
    phi_m_lag = -np.degrees(np.arcsin((beta-1)/(beta+1)))
    ax4.axvline(x=w_m_lag, color='red', linewidth=0.8, linestyle=':', alpha=0.5)
    ax4.scatter(w_m_lag, phi_m_lag, s=60, color='red', zorder=5)
    ax4.annotate(f'$\\omega_m$\n$\\phi_m={phi_m_lag:.1f}°$', xy=(w_m_lag, phi_m_lag),
                xytext=(w_m_lag*0.3, phi_m_lag+15), fontsize=9, color='red',
                arrowprops=dict(arrowstyle='->', color='red'))
    ax4.set_xlabel('$\\omega$ (rad/s)', fontsize=11)
    ax4.set_ylabel('$\\varphi(\\omega)$ / °', fontsize=11)
    ax4.set_title('滞后校正 — 相位滞后（负相角）', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3, which='both')
    ax4.set_ylim(-60, 5)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_9_lead_lag_comparison.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_9_lead_lag_comparison.png')


def fig5_9_correction_example():
    """校正设计综合示例：校正前后对比"""
    w = np.logspace(-2, 3, 3000)
    s = 1j * w

    # 原始系统: G0(s) = 10/[s(s+1)]
    G0 = 10 / (s * (s + 1))
    mag0 = 20 * np.log10(np.abs(G0))
    phase0 = np.degrees(np.angle(G0))

    # 超前校正: Gc(s) = (0.5s+1)/(0.05s+1) → α=10, T=0.05
    # Pole at 20, zero at 2
    Gc = (0.5 * s + 1) / (0.05 * s + 1)

    # Corrected: G(s) = Gc(s) * G0(s)
    G_corrected = Gc * G0
    mag_corr = 20 * np.log10(np.abs(G_corrected))
    phase_corr = np.degrees(np.angle(G_corrected))

    # Find margins
    # Original
    mag0_abs = np.abs(G0)
    idx_gc0 = np.argmin(np.abs(mag0_abs - 1.0))
    w_gc0 = w[idx_gc0]
    pm0 = 180 + phase0[idx_gc0]

    # Corrected
    mag_c_abs = np.abs(G_corrected)
    idx_gc1 = np.argmin(np.abs(mag_c_abs - 1.0))
    w_gc1 = w[idx_gc1]
    pm1 = 180 + phase_corr[idx_gc1]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), sharex=True)

    # Magnitude
    ax1.semilogx(w, mag0, color=COLORS[1], linewidth=2, linestyle='--', label=f'校正前 (PM$={pm0:.1f}°$)')
    ax1.semilogx(w, mag_corr, color=COLORS[0], linewidth=2.5, label=f'校正后 (PM$={pm1:.1f}°$)')
    ax1.axhline(y=0, color='gray', linewidth=0.8, linestyle=':', alpha=0.5)
    ax1.axvline(x=w_gc0, color=COLORS[1], linewidth=0.8, linestyle=':', alpha=0.5)
    ax1.axvline(x=w_gc1, color=COLORS[0], linewidth=0.8, linestyle=':', alpha=0.5)
    ax1.annotate(f'$\\omega_{{c0}}={w_gc0:.1f}$', xy=(w_gc0, 0), xytext=(w_gc0*0.7, 15),
                fontsize=10, color=COLORS[1])
    ax1.annotate(f'$\\omega_{{c1}}={w_gc1:.1f}$', xy=(w_gc1, 0), xytext=(w_gc1*1.2, 15),
                fontsize=10, color=COLORS[0])
    ax1.set_ylabel('$L(\\omega)$ / dB', fontsize=12)
    ax1.set_title('串联超前校正 — 校正前后 Bode 图对比\n$G_0(s)=\\frac{10}{s(s+1)}$,  $G_c(s)=\\frac{0.5s+1}{0.05s+1}$',
                 fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.legend(fontsize=11, loc='lower left')

    # Phase
    ax2.semilogx(w, phase0, color=COLORS[1], linewidth=2, linestyle='--', label=f'校正前')
    ax2.semilogx(w, phase_corr, color=COLORS[0], linewidth=2.5, label=f'校正后')
    ax2.axhline(y=-180, color='gray', linewidth=0.8, linestyle=':', alpha=0.5)
    ax2.axvline(x=w_gc0, color=COLORS[1], linewidth=0.8, linestyle=':', alpha=0.5)
    ax2.axvline(x=w_gc1, color=COLORS[0], linewidth=0.8, linestyle=':', alpha=0.5)

    # PM annotations
    ax2.annotate('', xy=(w_gc0, -180), xytext=(w_gc0, phase0[idx_gc0]),
                arrowprops=dict(arrowstyle='<->', color=COLORS[1], lw=1.5))
    ax2.annotate(f'PM$_0$={pm0:.1f}°', xy=(w_gc0, (phase0[idx_gc0]-180)/2),
                xytext=(w_gc0*0.5, (phase0[idx_gc0]-180)/2+20), fontsize=10, color=COLORS[1], fontweight='bold')

    ax2.annotate('', xy=(w_gc1, -180), xytext=(w_gc1, phase_corr[idx_gc1]),
                arrowprops=dict(arrowstyle='<->', color=COLORS[0], lw=1.5))
    ax2.annotate(f'PM$_1$={pm1:.1f}°', xy=(w_gc1, (phase_corr[idx_gc1]-180)/2),
                xytext=(w_gc1*1.5, (phase_corr[idx_gc1]-180)/2+20), fontsize=10, color=COLORS[0], fontweight='bold')

    ax2.set_xlabel('$\\omega$ (rad/s)', fontsize=12)
    ax2.set_ylabel('$\\varphi(\\omega)$ / °', fontsize=12)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.legend(fontsize=11, loc='upper right')
    ax2.set_ylim(-270, 0)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_9_correction_before_after.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_9_correction_before_after.png')


def fig5_9_pid_frequency():
    """PID控制的频域解释"""
    w = np.logspace(-3, 3, 3000)
    s = 1j * w

    # P, PI, PID comparison
    Kp, Ki, Kd = 2.0, 1.0, 0.5

    G_P = Kp * np.ones_like(s, dtype=complex)
    G_PI = Kp + Ki / s
    G_PID = Kp + Ki / s + Kd * s

    names = ['P (比例)', 'PI (比例-积分)', 'PID (比例-积分-微分)']
    G_list = [G_P, G_PI, G_PID]
    colors = [COLORS[0], COLORS[2], COLORS[4]]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

    for i, (G, name, c) in enumerate(zip(G_list, names, colors)):
        mag = 20 * np.log10(np.abs(G))
        phase = np.degrees(np.angle(G))

        ax1.semilogx(w, mag, color=c, linewidth=2, label=name)
        ax2.semilogx(w, phase, color=c, linewidth=2, label=name)

    ax1.set_ylabel('$L(\\omega)$ / dB', fontsize=12)
    ax1.set_title('PID 控制器的频域特性 ($K_p=2, K_i=1, K_d=0.5$)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.legend(fontsize=10)

    # P: flat, PI: +20dB/dec at low freq, PID: +20 at low, flat at high
    ax1.annotate('PI: 低频高增益\n→ 消除稳态误差', xy=(0.05, 30), fontsize=9, color=COLORS[2],
                bbox=dict(boxstyle='round', fc='#d1fae5', alpha=0.7))
    ax1.annotate('PID: 高频增益\n→ 微分作用', xy=(200, 8), fontsize=9, color=COLORS[4],
                bbox=dict(boxstyle='round', fc='#ede9fe', alpha=0.7))

    ax2.set_xlabel('$\\omega$ (rad/s)', fontsize=12)
    ax2.set_ylabel('$\\varphi(\\omega)$ / °', fontsize=12)
    ax2.axhline(y=0, color='gray', linewidth=0.5, linestyle=':', alpha=0.5)
    ax2.axhline(y=-90, color='gray', linewidth=0.5, linestyle=':', alpha=0.5)
    ax2.axhline(y=90, color='gray', linewidth=0.5, linestyle=':', alpha=0.5)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.legend(fontsize=10)
    ax2.set_ylim(-110, 110)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_9_pid_frequency.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_9_pid_frequency.png')


def fig5_x_correction_design_flow():
    """校正设计流程图（纯示意图）"""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('串联校正设计流程图', fontsize=16, fontweight='bold', pad=20)

    boxes = [
        (5, 9.5, '明确设计指标\n($e_{ss}$, $M_p$, $t_s$, PM, GM)', COLORS[0]),
        (5, 8.0, '绘制原系统开环 Bode 图\n计算 $\\omega_c$, PM, GM', COLORS[0]),
        (5, 6.5, '比较指标\n满足要求？', COLORS[3]),
        (3, 5.0, '$\checkmark$ 满足\n设计完成', COLORS[2]),
        (7, 5.0, '$\times$ 不满足\n需要校正', COLORS[1]),
        (7, 3.5, '确定校正方案\nPM不足 → 超前校正\n稳态精度不足 → 滞后校正\n都需要 → 滞后-超前', COLORS[4]),
        (7, 2.0, '计算校正参数\n$\\alpha, T$ (超前) / $\\beta, T$ (滞后)\n验证校正后性能', COLORS[4]),
        (5, 0.7, '$\checkmark$ 满足要求 → 实现', COLORS[2]),
    ]

    for x, y, text, color in boxes:
        ax.annotate(text, xy=(x, y), fontsize=9, ha='center', va='center', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor=f'#{color[1:]}20', edgecolor=color, linewidth=1.5),
                   color=color)

    # Arrows
    arrows = [(5,9,5,8.6), (5,7.6,5,7.2), (6.3,6.5,6.7,5.5), (3.7,6.5,3.3,5.5),
              (7,4.6,7,4.2), (7,3.1,7,2.7), (6.3,2.0,5.3,1.3), (3,4.6,3,1.3),
              (3,1.0,4.7,1.0)]
    for x1, y1, x2, y2 in arrows:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.5))

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_x_correction_design_flow.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_x_correction_design_flow.png')


def fig5_x_nyquist_openloop_summary():
    """开环Nyquist图（串联环节）"""
    # Example: G(s)=K/[s(s+1)(2s+1)] with K=1,2,5
    w = np.logspace(-2, 3, 3000)
    K_vals = [1, 2, 5]

    fig, ax = plt.subplots(figsize=(8, 8))

    for K, c in zip(K_vals, COLORS):
        s = 1j * w
        G = K / (s * (s + 1) * (2 * s + 1))
        ax.plot(G.real, G.imag, color=c, linewidth=2, label=f'$K={K}$')
        ax.scatter(G.real[-1], G.imag[-1], color=c, s=15)

    ax.scatter(-1, 0, s=120, marker='*', color='red', zorder=6, edgecolors='darkred', linewidths=2)
    ax.annotate('$(-1, j0)$', xy=(-1, 0), xytext=(-1.15, 0.15), fontsize=12, color='red', fontweight='bold')

    ax.axhline(y=0, color='gray', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='gray', linewidth=0.5, alpha=0.3)
    ax.set_xlabel('Re', fontsize=12)
    ax.set_ylabel('Im', fontsize=12)
    ax.set_title('开环 Nyquist 图 — 增益 $K$ 的影响\n$G(s)=\\frac{K}{s(s+1)(2s+1)}$', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-4, 1)
    ax.set_ylim(-3, 1)
    ax.set_aspect('equal')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'fig5_x_nyquist_openloop_summary.png'), dpi=150)
    plt.close(fig)
    print('[OK] fig5_x_nyquist_openloop_summary.png')


# ============================================================
# 主函数
# ============================================================

if __name__ == '__main__':
    print('='*60)
    print('《自动控制原理》第5章 图表生成')
    print('='*60)

    print('\n--- 5.1 频率特性基本概念 ---')
    fig5_1_sine_response()

    print('\n--- 5.2 Nyquist图 (典型环节) ---')
    fig5_2_nyquist_elements()
    fig5_x_nyquist_openloop_summary()

    print('\n--- 5.3 Bode图 (典型环节) ---')
    fig5_3_bode_elements()

    print('\n--- 5.3 开环Bode图绘制 ---')
    fig5_3_openloop_bode_construction()

    print('\n--- 5.3 最小相位系统 ---')
    fig5_3_minphase_comparison()

    print('\n--- 5.4 Nyquist稳定判据 ---')
    fig5_4_nyquist_criterion()
    fig5_4_nyquist_with_integrator()

    print('\n--- 5.5 稳定裕度 ---')
    fig5_5_stability_margins()

    print('\n--- 5.6 开环频域三频段 ---')
    fig5_6_openloop_freq_regions()

    print('\n--- 5.7-5.8 闭环频率特性 ---')
    fig5_7_closed_loop_response()

    print('\n--- 5.9 校正设计 ---')
    fig5_9_lead_lag_comparison()
    fig5_9_correction_example()
    fig5_9_pid_frequency()
    fig5_x_correction_design_flow()

    print('\n' + '='*60)
    print('全部图表生成完毕！')
    print(f'输出路径: {OUT_DIR}')
    print('='*60)
