import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

figsize_main=(8,4)
figsize_sub=(8,4)

def exp_1_1():
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
    ax1.set_ylabel('吞吐量 (GOPS)', color='black',fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 450)  # 调整Y轴范围
    ax1.tick_params(axis='y', labelcolor='black')

    # 创建右Y轴并绘制加速比（折线图）
    ax2 = ax1.twinx()
    ax2.set_ylabel('加速比', color='black',fontsize=14, fontweight='bold')
    lines = ax2.plot(index[2:], speedups[2:], 'o-', color='salmon', label='加速比')

    # 标注加速比（仅标注 LUT-InnerFP32 及其后续设备/方法）
    for i in range(2, len(devices)):
        ax2.text(index[i], speedups[i] + 0.1, f'x{speedups[i]:.1f}', ha='left', va='top', color='black',fontsize=12, fontweight='bold')

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
    plt.show()

def exp_1_2():
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
                color='black', fontsize=12, fontweight='bold')

    # 设置X轴
    ax.set_xticks(index)
    ax.set_xticklabels(devices, fontsize=10)

    # 设置Y轴
    ax.set_ylabel('能效比 (GOPS/W)', fontsize=12, fontweight='bold')
    ax.set_ylim(0, max(efficiencies) * 1.2)  # Y轴范围根据最大值动态调整

    # 添加水平实线（CPU基准）
    ax.axhline(y=cpu_efficiency, color='skyblue', linestyle='-', label='CPU基准能效比')
    ax.text(-0.5, cpu_efficiency, '1', color='black', va='center', ha='center', 
            fontsize=10, fontweight='bold')

    # 添加图例
    ax.legend(loc='upper left', fontsize=10)

    # 美化图表
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # 显示图表
    plt.show()

def exp_1_3():
    # 数据准备
    lut_types = ['UPMEM-FP32', 'LUT-FP4', 'LUT-M', 'LUT-W-C', 'LUT-W-R']
    ipc = [0.965875191, 0.998003594, 0.921964628, 0.858607134, 0.77689699]
    mem_util = [0.009789265, 0.166713826, 0.118756781, 0.300449624, 0.503408529]

    # 转换为百分比
    ipc_percent = [x * 100 for x in ipc]
    mem_util_percent = [x * 100 for x in mem_util]

    # 创建图形和左轴
    fig, ax1 = plt.subplots(figsize=figsize_sub)

    # 设置横轴和左纵轴（IPC）
    ax1.set_ylabel('计算利用率(IPC, %)', color='black', fontsize=12, fontweight='bold')
    ax1.plot(lut_types, ipc_percent, color='skyblue', label='IPC', 
            marker='o', markeredgecolor='black', markerfacecolor='skyblue')
    ax1.tick_params(axis='y', labelcolor='black')

    # 标注 IPC 数值
    for i, txt in enumerate(ipc_percent):
        ax1.annotate(f'{txt:.2f}', (lut_types[i], ipc_percent[i]), 
                    textcoords="offset points", xytext=(0,10), ha='center')

    # 创建右纵轴（Mem Utilization）
    ax2 = ax1.twinx()
    ax2.set_ylabel('内存带宽利用率(MBU, %)', color='black', fontsize=12, fontweight='bold')
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
    ax2.set_ylim(0, 60)
    ax2.set_yticks([0, 10, 20, 30, 40, 50, 60])

    # 添加图例并上移
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.95), ncol=2)

    # 调整布局
    fig.tight_layout()

    # 显示图像
    plt.show()

def exp_2_1():
    # 数据
    algorithms = ['LUT-M', 'LUT-W-C', 'LUT-W-R', 'LUT-FP4']
    before_opt = [98.57806193, 118.1539588, 354.4696776, 145.4954436]  # 优化前数据
    algorithms_opt = ['LUT-M FLA', 'LUT-W-C FLA', 'LUT-W-R FLA', 'LUT-SIMD']
    after_opt = [116.8794509, 139.4392998, 354.4696776, 2297.898708]   # 优化后数据

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
        ax1.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')

    for bar in bars_after:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')

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
    ax1.set_ylabel('吞吐量 (GOPS)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('优化提升 (%)', fontsize=12, fontweight='bold')

    # 设置图例
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')

    # 调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()

def exp_3_1():
    # 数据准备
    algorithms = ['UPMEM-FP32', 'LUT-FP4', 'LUT-M', 'LUT-W-C', 'LUT-W-R']
    tasklets = [1, 2, 4, 8, 16]

    # 模拟数据（延迟，单位：ms）
    data = {
        1: [115.442148, 6.505045, 6.492662, 4.117653, 2.122165],
        2: [57.506754, 3.252839, 3.498259, 2.116764, 1.068728],
        4: [28.752809, 1.626508, 1.773641, 1.113842, 0.576683],
        8: [14.376392, 0.813344, 0.915873, 0.60799, 0.339071],
        16: [10.447618, 0.589588, 0.698698, 0.467624, 0.29882]
    }

    # 创建图表
    fig, ax = plt.subplots(figsize=figsize_main)

    # 设置颜色方案
    colors = ['#FF595E', '#FFCA3A', '#8AC926', '#1982C4', '#6A4C93']

    # 设置柱状图位置
    num_algorithms = len(algorithms)
    num_tasklets = len(tasklets)
    bar_width = 0.15
    group_width = num_tasklets * bar_width + 0.2  # 每个算法组的总宽度
    x = np.arange(num_algorithms) * group_width

    # 绘制柱状图
    for i, tasklet in enumerate(tasklets):
        values = [data[tasklet][j] for j in range(num_algorithms)]
        ax.bar(x + i * bar_width, values, width=bar_width, label=f'{tasklet} Tasklets', color=colors[i])

    # 设置横轴
    ax.set_xticks(x + (num_tasklets * bar_width) / 2)
    ax.set_xticklabels(algorithms, rotation=0)  # 算法标签水平显示

    # 设置纵轴为对数刻度，并自定义刻度
    ax.set_yscale('log')
    ax.set_yticks([0.1,0.2,0.4,0.8,1.6, 3.2, 6.4, 12.8, 25.6, 51.2, 102.4, 204.8])
    ax.set_yticklabels([0.1,0.2,0.4,0.8,1.6, 3.2, 6.4, 12.8, 25.6, 51.2, 102.4, 204.8])

    # 设置横轴和纵轴标题
    ax.set_ylabel('执行时间(s)', fontsize=12, fontweight='bold')

    # 设置图例
    ax.legend(title='线程数量', loc='upper right')

    # 只为大刻度显示水平网格线
    ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.7)

    # 调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()

def exp_3_2_1():
    # 数据
    data_text = """
    size	UPMEM-FP32	LUT-FP4	LUT-M	LUT-W-C	LUT-W-R
    4096x128	0.32664	0.018675	0.08981	0.103594	0.000491
    4096x256	0.652888	0.037097	0.108022	0.115706	0.00048
    4096x512	1.305717	0.073903	0.144751	0.13867	0.03395
    4096x1024	2.610115	0.147585	0.217757	0.181888	0.060546
    4096x2048	5.221183	0.294896	0.384521	0.27091	0.119204
    4096x4096	10.447618	0.589588	0.698698	0.467624	0.29882
    """

    # 解析数据
    lines = data_text.strip().split('\n')
    header = lines[0].split('\t')
    algorithms = header[1:]  # ['LUT-InnerFP32', 'LUT-InnerFP4', 'LUT-M', 'LUT-W-C', 'LUT-W-R']

    data = {}
    for line in lines[1:]:
        parts = line.split('\t')
        size = parts[0]
        _, cols = map(int, size.split('x'))  # 提取列数
        values = list(map(float, parts[1:]))
        data[cols] = values

    # 列数列表
    cols_list = sorted(data.keys())  # [128, 256, 512, 1024, 2048, 4096]

    # 配色方案 - 为不同列数分配颜色
    colors = ['#FF595E', '#FFCA3A', '#8AC926', '#1982C4', '#6A4C93', '#DB6BCF']

    # 创建图表
    fig, ax = plt.subplots(figsize=figsize_sub)

    # 设置柱状图位置
    num_algorithms = len(algorithms)
    num_cols = len(cols_list)
    bar_width = 0.15
    group_width = num_cols * bar_width + 0.2
    x = np.arange(num_algorithms) * group_width

    # 绘制柱状图
    for col_idx, col in enumerate(cols_list):
        y_values = [data[col][algo_idx] for algo_idx in range(num_algorithms)]
        x_positions = x + col_idx * bar_width
        ax.bar(x_positions, y_values, width=bar_width, color=colors[col_idx], label=f'{col}')

    # 设置横轴
    ax.set_xticks(x + (num_cols * bar_width) / 2)
    ax.set_xticklabels(algorithms, rotation=0)

    # 设置纵轴为对数刻度
    ax.set_yscale('log')
    ax.set_ylim(0.0004, 15)
    ax.set_yticks([0.0004, 0.0008, 0.0016, 0.0032, 0.0064, 0.0128, 0.0256, 0.0512, 0.1024, 0.2048, 0.4096, 0.8192, 1.6384, 3.2768, 6.5536,13.1072])
    ax.set_yticklabels([0.0004, 0.0008, 0.0016, 0.0032, 0.0064, 0.0128, 0.0256, 0.0512, 0.1024, 0.2048, 0.4096, 0.8192, 1.6384, 3.2768, 6.5536,13.1072])

    # 只显示大刻度的水平网格线
    ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.7)

    # 设置图例
    ax.legend(title='矩阵列数', loc='upper right')

    # 设置标题和轴标签
    ax.set_ylabel('执行时间(s)')

    # 调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()

def exp_3_2_2():
    # 数据
    data_text = """
    size	UPMEM-FP32	LUT-FP4	LUT-M	LUT-W-C	LUT-W-R
    128x4096	0.325388	0.014401	0.023434	0.015973	0.009058
    256x4096	0.650344	0.027497	0.04519	0.030757	0.01694
    512x4096	1.30349	0.053754	0.088426	0.059659	0.03269
    1024x4096	2.609546	0.148311	0.176105	0.118497	0.064308
    2048x4096	5.22335	0.294922	0.384645	0.270924	0.130478
    4096x4096	10.447618	0.589588	0.698698	0.467624	0.29882
    """

    # 解析数据
    lines = data_text.strip().split('\n')
    header = lines[0].split('\t')
    algorithms = header[1:]  # ['LUT-InnerFP32', 'LUT-InnerFP4', 'LUT-M', 'LUT-W-C', 'LUT-W-R']

    data = {}
    for line in lines[1:]:
        parts = line.split('\t')
        size = parts[0]
        rows, _ = map(int, size.split('x'))  # 提取行数
        values = list(map(float, parts[1:]))
        data[rows] = values

    # 行数列表
    rows_list = sorted(data.keys())  # [128, 256, 512, 1024, 2048, 4096]

    # 配色方案 - 为不同行数分配颜色
    colors = ['#FF595E', '#FFCA3A', '#8AC926', '#1982C4', '#6A4C93', '#DB6BCF']

    # 创建图表
    fig, ax = plt.subplots(figsize=figsize_sub)

    # 设置柱状图位置
    num_algorithms = len(algorithms)
    num_rows = len(rows_list)
    bar_width = 0.15
    group_width = num_rows * bar_width + 0.2
    x = np.arange(num_algorithms) * group_width

    # 绘制柱状图
    for row_idx, row in enumerate(rows_list):
        y_values = [data[row][algo_idx] for algo_idx in range(num_algorithms)]
        x_positions = x + row_idx * bar_width
        ax.bar(x_positions, y_values, width=bar_width, color=colors[row_idx], label=f'{row}')

    # 设置横轴
    ax.set_xticks(x + (num_rows * bar_width) / 2)
    ax.set_xticklabels(algorithms, rotation=0)

    # 设置纵轴为对数刻度
    ax.set_yscale('log')
    ax.set_ylim(0.0064, 13)
    ax.set_yticks([0.0064, 0.0128, 0.0256, 0.0512, 0.1024, 0.2048, 0.4096, 0.8192, 1.6384, 3.2768, 6.5536,13.1072])
    ax.set_yticklabels([0.0064, 0.0128, 0.0256, 0.0512, 0.1024, 0.2048, 0.4096, 0.8192, 1.6384, 3.2768, 6.5536,13.1072])

    # 只显示大刻度的水平网格线
    ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.7)

    # 设置图例
    ax.legend(title='矩阵行数', loc='upper right')

    # 设置标题和轴标签
    ax.set_ylabel('执行时间(s)')

    # 调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()

exp_1_1()
exp_1_2()
exp_1_3()
exp_2_1()
exp_3_1()
exp_3_2_1()
exp_3_2_2()