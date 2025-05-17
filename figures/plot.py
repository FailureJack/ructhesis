import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# plt.minorticks_off()

figsize_main=(8,4)
figsize_sub=(8,4)

def exp_1_1():
    plt.rcParams["font.size"] = 15  # 默认字体大小
    plt.rcParams["axes.titlesize"] = 15  # 标题字体大小
    plt.rcParams["axes.labelsize"] = 15  # 坐标轴标签字体大小
    plt.rcParams["xtick.labelsize"] = 13  # x轴刻度字体大小
    plt.rcParams["ytick.labelsize"] = 13  # y轴刻度字体大小
    plt.rcParams["legend.fontsize"] = 12  # 图例字体大小
    
    # 数据
    devices = ['MKL', 'cuBlas', 'UPMEM-FP32', 'LUT-M', 'LUT-W-C','LUT-W-R',  'LUT-FP4']
    throughputs = [24.14528848, 365.8131084, 8.224560152, 98.57806193, 118.1539588,354.4696776,  145.4954436]
    fp32_throughput = throughputs[2]
    speedups = [throughput / fp32_throughput for throughput in throughputs]

    # 设置图表
    fig, ax1 = plt.subplots(figsize=figsize_main)  # 调整宽度以适应水平标签

    # 绘制吞吐量（柱状图）
    bar_width = 0.5  # 调宽柱状图
    index = np.arange(len(devices)) * 0.7  # 调整X轴间距，使坐标更紧凑
    bars = ax1.bar(index, throughputs, bar_width, label='吞吐量', color='skyblue')

    # 设置X轴（横轴标签水平显示）
    ax1.set_xticks(index)
    ax1.set_xticklabels(devices, ha='center', color='black')  # 设置为水平显示

    # 设置左Y轴（吞吐量）
    ax1.set_ylabel('吞吐量 (GOPS)', color='black',fontweight='bold')
    ax1.set_ylim(0, 450)  # 调整Y轴范围
    ax1.tick_params(axis='y', labelcolor='black')

    # 创建右Y轴并绘制加速比（折线图）
    ax2 = ax1.twinx()
    ax2.set_ylabel('加速比', color='black',fontweight='bold')
    lines = ax2.plot(index[2:], speedups[2:], 'o-', color='salmon', label='加速比')

    # 标注加速比（仅标注 LUT-InnerFP32 及其后续设备/方法）
    for i in range(2, len(devices)):
        ax2.text(index[i], speedups[i] + 0.1, f'x{speedups[i]:.1f}', ha='right', va='top', color='black', fontweight='bold')

    # 添加水平虚线（理论上限）
    theoretical_limit = 381
    ax1.axhline(y=theoretical_limit, color='red', linestyle='--', label='理论上限')

    # 在左Y轴用红色字体标注381 GOPS
    ax1.text(-0.5, theoretical_limit, '381 GOPS', color='red', va='center', ha='right')

    # 设置坐标轴线条颜色为黑色
    for spine in ax1.spines.values():
        spine.set_color('black')
    for spine in ax2.spines.values():
        spine.set_color('black')

    # 添加图例
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # 美化图表
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tight_layout()

    # 显示图表
    # plt.show()
    plt.savefig('./Exp1-1.pdf', format='pdf')

def exp_1_2():
    plt.rcParams["font.size"] = 18  # 默认字体大小
    plt.rcParams["axes.titlesize"] = 18  # 标题字体大小
    plt.rcParams["axes.labelsize"] = 18  # 坐标轴标签字体大小
    plt.rcParams["xtick.labelsize"] = 15  # x轴刻度字体大小
    plt.rcParams["ytick.labelsize"] = 15  # y轴刻度字体大小
    plt.rcParams["legend.fontsize"] = 18  # 图例字体大小
    # 数据（示例）
    devices = ['MKL', 'cuBlas', 'UPMEM-FP32', 'LUT-M', 'LUT-W-C','LUT-W-R',  'LUT-FP4']
    efficiencies = [1, 7.575248244, 0.19958669, 2.392209279, 2.867260638, 8.601971224, 3.530760733]  # 归一化效率 (GOPS/W)
    cpu_efficiency = efficiencies[0]  # CPU效率为1 GOPS/W

    # 设置图表
    fig, ax = plt.subplots(figsize=figsize_sub)

    # 绘制柱状图（低于实线用蓝色，高于实线用橙色）
    bar_width = 0.5
    index = np.arange(len(devices))*0.7
    for i, efficiency in enumerate(efficiencies):
        # 低于实线的部分（蓝色系）
        ax.bar(index[i], min(efficiency, cpu_efficiency), bar_width, color='skyblue')
        # 高于实线的部分（橙色系）
        if efficiency > cpu_efficiency:
            ax.bar(index[i], efficiency - cpu_efficiency, bar_width, bottom=cpu_efficiency, color='orange')

    # 标注柱状图数值（字体调大并加粗）
    for i, efficiency in enumerate(efficiencies):
        ax.text(index[i], efficiency + 0.2, f'{efficiency:.1f}', ha='center', va='bottom', 
                color='black', fontweight='bold')

    # 设置X轴
    ax.set_xticks(index)
    ax.set_xticklabels(devices)

    # 设置Y轴
    ax.set_ylabel('能效比 (GOPS/W)', fontweight='bold')
    ax.set_ylim(0, max(efficiencies) * 1.2)  # Y轴范围根据最大值动态调整

    # 添加水平实线（CPU基准）
    ax.axhline(y=cpu_efficiency, color='skyblue', linestyle='-', label='CPU基准能效比')
    ax.text(-0.5, cpu_efficiency, '1', color='black', va='center', ha='center', fontweight='bold')

    # 添加图例
    ax.legend(loc='upper left')

    # 美化图表
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # 显示图表
    # plt.show()
    plt.savefig('./Exp1-2-1.pdf', format='pdf')

def exp_1_3():
    plt.rcParams["font.size"] = 15  # 默认字体大小
    plt.rcParams["axes.titlesize"] = 18  # 标题字体大小
    plt.rcParams["axes.labelsize"] = 18  # 坐标轴标签字体大小
    plt.rcParams["xtick.labelsize"] = 15  # x轴刻度字体大小
    plt.rcParams["ytick.labelsize"] = 15  # y轴刻度字体大小
    plt.rcParams["legend.fontsize"] = 18  # 图例字体大小
    # 数据准备
    lut_types = ['UPMEM-FP32', 'LUT-FP4', 'LUT-M', 'LUT-W-C', 'LUT-W-R']
    ipc = [0.96588065, 0.997993581, 0.96958947, 0.843769578, 0.769674711]
    mem_util = [0.009754456, 0.04321273, 0.037034307, 0.116628352, 0.106576313]

    # 转换为百分比
    ipc_percent = [x * 100 for x in ipc]
    mem_util_percent = [x * 100 for x in mem_util]

    # 创建图形和左轴
    fig, ax1 = plt.subplots(figsize=figsize_sub)

    # 设置横轴和左纵轴（IPC）
    ax1.set_ylabel('计算利用率(IPC, %)', color='black', fontweight='bold')
    ax1.plot(lut_types, ipc_percent, color='skyblue', label='IPC', 
            marker='o', markeredgecolor='black', markerfacecolor='skyblue')
    ax1.tick_params(axis='y', labelcolor='black')

    # 标注 IPC 数值
    for i, txt in enumerate(ipc_percent):
        ax1.annotate(f'{txt:.2f}', (lut_types[i], ipc_percent[i]), 
                    textcoords="offset points", xytext=(0,10), ha='center')

    # 创建右纵轴（Mem Utilization）
    ax2 = ax1.twinx()
    ax2.set_ylabel('内存带宽利用率(MBU, %)', color='black', fontweight='bold')
    ax2.plot(lut_types, mem_util_percent, color='orange', label='MBU', 
            marker='s', markeredgecolor='black', markerfacecolor='orange')
    ax2.tick_params(axis='y', labelcolor='black')

    # 标注 Mem Utilization 数值
    for i, txt in enumerate(mem_util_percent):
        ax2.annotate(f'{txt:.2f}', (lut_types[i], mem_util_percent[i]), 
                    textcoords="offset points", xytext=(0,10), ha='center')

    # 调整 IPC 纵轴刻度
    ax1.set_ylim(70, 110)
    ax1.set_yticks([70, 80, 90, 100])

    # 调整 Mem Utilization 纵轴刻度
    ax2.set_ylim(0, 25)
    # ax2.set_yticks([0, 10, 20, 30, 40, 50, 60])

    # 添加图例并上移
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.95), ncol=2)

    # 调整布局
    fig.tight_layout()

    # 显示图像
    # plt.show()
    plt.savefig('./Exp1-2-2.pdf', format='pdf')

def exp_2_1():
    plt.rcParams["font.size"] = 18  # 默认字体大小
    plt.rcParams["axes.titlesize"] = 18  # 标题字体大小
    plt.rcParams["axes.labelsize"] = 20  # 坐标轴标签字体大小
    plt.rcParams["xtick.labelsize"] = 15  # x轴刻度字体大小
    plt.rcParams["ytick.labelsize"] = 15  # y轴刻度字体大小
    plt.rcParams["legend.fontsize"] = 20  # 图例字体大小
    # 数据
    algorithms = ['LUT-M', 'LUT-W-C', 'LUT-W-R', 'LUT-FP4']
    before_opt = [122.9420235,183.6931935,287.4618363,145.6938505]  # 优化前数据
    algorithms_opt = ['LUT-M FLA', 'LUT-W-C FLA', 'LUT-W-R FLA', 'LUT-SIMD']
    after_opt = [140.2985283, 234.8044279, 287.4618363, 2301.817144]   # 优化后数据

    # 计算提升倍数和百分比
    improvement = [after / before if after is not None else 1 for before, after in zip(before_opt, after_opt)]
    improvement_percent = [(imp - 1) * 100 for imp in improvement]

    # 创建图表
    fig, ax1 = plt.subplots(figsize=(12,6))

    # 设置柱状图位置
    bar_width = 0.35
    x = np.arange(len(algorithms))

    # 绘制优化前的柱子
    bars_before = ax1.bar(x - bar_width/2, before_opt, bar_width, label='优化前吞吐', color='skyblue')

    # 绘制优化后的柱子
    bars_after = ax1.bar(x + bar_width/2, after_opt, bar_width, label='优化后吞吐', color='orange')

    # 在柱子上方标注数值
    for bar in bars_before:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom', fontweight='bold')

    for bar in bars_after:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom', fontweight='bold')

    # 设置左纵轴为对数刻度
    ax1.set_yscale('log')
    ax1.set_ylim(64, 2700)
    ax1.set_yticks([64, 128, 256, 512, 1024, 2048])
    ax1.set_yticklabels([64, 128, 256, 512, 1024, 2048])

    # 设置横轴标签，显示 algorithms 和 algorithms_opt，使用换行符分隔
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"   {alg}   {alg_opt}" for alg, alg_opt in zip(algorithms, algorithms_opt)])

    # 创建右纵轴
    ax2 = ax1.twinx()

    # 设置右纵轴为对数刻度
    ax2.set_yscale('log')
    ax2.set_ylim(0.5, 32)
    ax2.set_yticks([1, 2, 4, 8, 16])
    ax2.set_yticklabels([1, 2, 4, 8, 16])

    # 绘制折线图（优化提升）
    for i, imp in enumerate(improvement):
        if imp != 1:  # 仅对有提升的算法绘制折线
            ax2.plot([x[i] - bar_width/2, x[i] + bar_width/2], [1, imp], marker='o', color='lightcoral', 
                    markeredgecolor='black', markersize=8, linewidth=2)
            # 标注提升百分比，位置调整到右侧
            ax2.text(x[i] + bar_width/2 + 0.05, imp, f'+{improvement_percent[i]:.2f}%', ha='left', va='center', color='black')

    # 添加虚拟折线图用于图例
    ax2.plot([], [], color='lightcoral', marker='o', markeredgecolor='black', markersize=8, linewidth=2, 
            label='优化提升')

    # 设置标题和轴标签
    ax1.set_ylabel('吞吐量 (GOPS)', fontweight='bold')
    ax2.set_ylabel('优化提升 (%)', fontweight='bold')

    # 设置图例
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')

    # 调整布局
    plt.tight_layout()

    # 显示图表
    # plt.show()
    plt.savefig('./Exp2-1.pdf', format='pdf')

def exp_2_2():
    # 数据
    algorithms = ['LUT-M', 'LUT-W-C', 'LUT-W-R', 'LUT-FP4']
    before_opt = [99.15211704,83.26153716,78.5078334,88.40628288]  # 优化前数据
    algorithms_opt = ['LUT-M FLA', 'LUT-W-C FLA', 'LUT-W-R FLA', 'LUT-SIMD']
    after_opt = [116.6419367, 97.14350083, 89.29461206, 1396.730863]   # 优化后数据

    # 计算提升倍数和百分比
    improvement = [after / before if after is not None else 1 for before, after in zip(before_opt, after_opt)]
    improvement_percent = [(imp - 1) * 100 for imp in improvement]

    # 创建图表
    fig, ax1 = plt.subplots(figsize=(12,6))

    # 设置柱状图位置
    bar_width = 0.35
    x = np.arange(len(algorithms))

    # 绘制优化前的柱子
    bars_before = ax1.bar(x - bar_width/2, before_opt, bar_width, label='优化前吞吐', color='skyblue')

    # 绘制优化后的柱子
    bars_after = ax1.bar(x + bar_width/2, after_opt, bar_width, label='优化后吞吐', color='orange')

    # 在柱子上方标注数值
    for bar in bars_before:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='top', fontweight='bold')

    for bar in bars_after:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='top', fontweight='bold')

    # 设置左纵轴为对数刻度
    ax1.set_yscale('log')
    ax1.set_ylim(64, 1700)
    ax1.set_yticks([64, 128, 256, 512, 1024])
    ax1.set_yticklabels([64, 128, 256, 512, 1024])

    # 设置横轴标签，显示 algorithms 和 algorithms_opt，使用换行符分隔
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"   {alg}   {alg_opt}" for alg, alg_opt in zip(algorithms, algorithms_opt)])

    # 创建右纵轴
    ax2 = ax1.twinx()

    # 设置右纵轴为对数刻度
    ax2.set_yscale('log')
    ax2.set_ylim(0.5, 32)
    ax2.set_yticks([1, 2, 4, 8, 16])
    ax2.set_yticklabels([1, 2, 4, 8, 16])

    # 绘制折线图（优化提升）
    for i, imp in enumerate(improvement):
        if imp != 1:  # 仅对有提升的算法绘制折线
            ax2.plot([x[i] - bar_width/2, x[i] + bar_width/2], [1, imp], marker='o', color='lightcoral', 
                    markeredgecolor='black', markersize=8, linewidth=2)
            # 标注提升百分比，位置调整到右侧
            ax2.text(x[i] + bar_width/2 + 0.05, imp, f'+{improvement_percent[i]:.2f}%', ha='left', va='center', color='black')

    # 添加虚拟折线图用于图例
    ax2.plot([], [], color='lightcoral', marker='o', markeredgecolor='black', markersize=8, linewidth=2, 
            label='优化提升')

    # 设置标题和轴标签
    ax1.set_ylabel('吞吐量 (GOPS)', fontweight='bold')
    ax2.set_ylabel('优化提升 (%)', fontweight='bold')

    # 设置图例
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')

    # 调整布局
    plt.tight_layout()

    # 显示图表
    # plt.show()
    plt.savefig('./Exp2-2.pdf', format='pdf')
    
def exp_3_1():
    plt.rcParams["font.size"] = 15  # 默认字体大小
    plt.rcParams["axes.titlesize"] = 18  # 标题字体大小
    plt.rcParams["axes.labelsize"] = 18  # 坐标轴标签字体大小
    plt.rcParams["xtick.labelsize"] = 15  # x轴刻度字体大小
    plt.rcParams["ytick.labelsize"] = 15  # y轴刻度字体大小
    plt.rcParams["legend.fontsize"] = 15  # 图例字体大小
   # 数据
    tasklets = [1, 2, 4, 8, 16]  # 线程数量
    data = {
        'LUT-InnerFP32': [115.442148, 57.506754, 28.752809, 14.376392, 10.447618],
        'LUT-InnerFP4': [6.505045, 3.252839, 1.626508, 0.813344, 0.589588],
        'LUT-M': [6.492662, 3.498259, 1.773641, 0.915873, 0.698698],
        'LUT-W-C': [4.117653, 2.116764, 1.113842, 0.60799, 0.467624],
        'LUT-W-R': [2.122165, 1.068728, 0.576683, 0.339071, 0.29882]
    }

    # 颜色和标记
    colors = ['#FF595E', '#FFCA3A', '#8AC926', '#1982C4', '#6A4C93', '#DB6BCF']
    markers = ['o', 's', '^', 'D', 'x']  # 圆圈、正方形、三角形、菱形、叉形

    # 创建图形
    plt.figure(figsize=(8,5))

    # 绘制每条折线
    for i, (algo, times) in enumerate(data.items()):
        plt.plot(tasklets, times, color=colors[i], marker=markers[i], label=algo)

    # 设置对数坐标
    plt.xscale('log')
    plt.yscale('log')

   # 设置 x 轴刻度为数据中出现的列数
    plt.xticks(tasklets, labels=tasklets)

    # 获取所有 y 轴数据（时间值）并去重
    all_times =[0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8, 25.6, 51.2, 102.4, 204.8]
    plt.yticks(all_times, labels=all_times)  # 设置 y 轴刻度为数据中出现的时间

    # 设置坐标轴范围（稍微扩展以显示所有点）
    plt.xlim(min(tasklets) * 0.9, max(tasklets) * 1.1)
    plt.ylim(min(all_times) * 0.9, max(all_times) * 1.5)

    # 添加标签和标题
    plt.xlabel('线程数量')
    plt.ylabel('执行时间(ms)')

    # 添加图例
    plt.legend(loc='upper right')

    # 显示图形
    # plt.show()
    plt.savefig('./Exp3-1.pdf', format='pdf')

def exp_3_2_1():
    plt.rcParams["font.size"] = 15  # 默认字体大小
    plt.rcParams["axes.titlesize"] = 20  # 标题字体大小
    plt.rcParams["axes.labelsize"] = 20  # 坐标轴标签字体大小
    plt.rcParams["xtick.labelsize"] = 18  # x轴刻度字体大小
    plt.rcParams["ytick.labelsize"] = 15  # y轴刻度字体大小
    plt.rcParams["legend.fontsize"] = 18  # 图例字体大小
    # 数据
    columns = [128, 256, 512, 1024, 2048, 4096]  # x 轴数据
    data = {
        'LUT-InnerFP32': [0.32664, 0.652888, 1.305717, 2.610115, 5.221183, 10.447618],
        'LUT-InnerFP4': [0.018675, 0.037097, 0.073903, 0.147585, 0.294896, 0.589588],
        'LUT-M': [0.08981, 0.108022, 0.144751, 0.217757, 0.384521, 0.698698],
        'LUT-W-C': [0.103594, 0.115706, 0.13867, 0.181888, 0.27091, 0.467624],
        'LUT-W-R': [0.014985, 0.021235, 0.03395, 0.060546, 0.119204, 0.29882]
    }

    # 颜色和标记
    colors = ['#FF595E', '#FFCA3A', '#8AC926', '#1982C4', '#6A4C93', '#DB6BCF']
    markers = ['o', 's', '^', 'D', 'x']  # 圆圈、正方形、三角形、菱形、叉形

    # 创建图形
    plt.figure(figsize=(8,6))

    # 绘制每条折线
    for i, (algo, times) in enumerate(data.items()):
        plt.plot(columns, times, color=colors[i], marker=markers[i], label=algo)

    # 设置对数坐标
    plt.xscale('log')
    plt.yscale('log')

    # 设置 x 轴刻度为数据中出现的列数
    plt.xticks(columns, labels=columns)

    # 获取所有 y 轴数据（时间值）并去重
    all_times = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.28, 2.56, 5.12, 10.24, 20.48]
    # all_times = sorted(set(time for times in data.values() for time in times))  # 提取所有时间并排序去重
    plt.yticks(all_times, labels=all_times)  # 设置 y 轴刻度为数据中出现的时间

    # 设置坐标轴范围（稍微扩展以显示所有点）
    plt.xlim(min(columns) * 0.9, max(columns) * 1.1)
    plt.ylim(min(all_times) * 0.9, max(all_times) * 1.1)

    # 添加标签和标题
    plt.xlabel('矩阵列数')
    plt.ylabel('执行时间(ms)')

    # 添加图例
    plt.legend()

    # 显示图形
    # plt.show()
    plt.savefig('./Exp3-2-1.pdf', format='pdf')

def exp_3_2_2():
    # 数据准备
    rows = [128, 256, 512, 1024, 2048, 4096]  # x 轴：矩阵行数
    data = {
        'LUT-InnerFP32': [0.325388, 0.650344, 1.30349, 2.609546, 5.22335, 10.447618],
        'LUT-InnerFP4': [0.014401, 0.027497, 0.053754, 0.148311, 0.294922, 0.589588],
        'LUT-M': [0.023434, 0.04519, 0.088426, 0.176105, 0.384645, 0.698698],
        'LUT-W-C': [0.015973, 0.030757, 0.059659, 0.118497, 0.270924, 0.467624],
        'LUT-W-R': [0.009058, 0.01694, 0.03269, 0.064308, 0.130478, 0.29882]
    }

    # 颜色和标记
    colors = ['#FF595E', '#FFCA3A', '#8AC926', '#1982C4', '#6A4C93', '#DB6BCF']
    markers = ['o', 's', '^', 'D', 'x']  # 圆圈、正方形、三角形、菱形、叉形

    # 创建图形
    plt.figure(figsize=(8,6))

    # 绘制每条折线
    for i, (algo, times) in enumerate(data.items()):
        plt.plot(rows, times, color=colors[i], marker=markers[i], label=algo)

    # 设置对数坐标
    plt.xscale('log')
    plt.yscale('log')

    # 设置 x 轴刻度
    plt.xticks(rows, labels=rows)

    # 获取所有 y 轴数据（时间值）并去重
    all_times = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.28, 2.56, 5.12, 10.24, 20.48]
    plt.yticks(all_times, labels=all_times)

    # 设置坐标轴范围
    plt.xlim(100, 5000)  # 略大于 128 到 4096
    plt.ylim(0.005, 20)  # 略大于 0.009058 到 10.447618

    # 添加标签和标题
    # 添加标签和标题
    plt.xlabel('矩阵行数')
    plt.ylabel('执行时间(ms)')

    # 添加图例
    plt.legend()

    # 显示图形
    # plt.show()
    plt.savefig('./Exp3-2-2.pdf', format='pdf')

exp_1_1()
exp_1_2()
exp_1_3()
exp_2_1()
exp_2_2()
exp_3_1()
exp_3_2_1()
exp_3_2_2()