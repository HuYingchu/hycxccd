Pyxccd教程
==========

本教程将指导您如何使用pyxccd处理HLS影像数据，生成年度扰动图、最近扰动图和首次扰动图。整个过程分为三个主要步骤。

准备工作
--------

1. 安装pyxccd：
~~~~~~~~~~~~~~~

::

   pip install pyxccd

2. 数据组织结构
~~~~~~~~~~~~~~~

准备好下载的HLS文件，确保数据按如下结构组织：（示例提供2019-2024六年的HLS数据）

::

   HLS根目录/
   └── 瓦片ID (如51RTP)/
       └── HLS影像文件 (如HLS.S30.T51RTP.2021001.v2.0.B02.tif)

3. 配置文件
~~~~~~~~~~~

准备配置文件config_hls.yaml，可根据需要调整config_hls.yaml中的区块大小参数（示例文件分为30×30块）：

.. code:: yaml

   DATASETINFO:
     n_rows: 3660
     n_cols: 3660
     n_block_x: 30
     n_block_y: 30

第一步：影像堆叠处理
--------------------

功能说明
~~~~~~~~

将HLS影像按时间序列堆叠，为后续变化检测做准备。

操作步骤
~~~~~~~~

1. 确认瓦片列表文件tile_list内容为要处理的瓦片ID，若有多个则每行一个（示例文件为51RTP）。

2. 运行堆叠处理脚本step1_stack.py：

.. code:: bash

   python step1_stack.py --tile_list_fn ./tile_list \
                        --meta_path /path/to/hls/data \
                        --yaml_path ./config_hls.yaml \
                        --out_path /stack \
                        --low_date_bound 2019-01-01 \
                        --upp_date_bound 2024-12-31 \
                        --n_cores 16

参数说明
~~~~~~~~

::

   --tile_list_fn: 瓦片列表文件路径
   --meta_path: HLS数据根目录
   --yaml_path: 配置文件路径
   --out_path: 堆叠结果输出目录
   --low_date_bound: 处理的时间范围下限(YYYY-MM-DD)
   --upp_date_bound: 处理的时间范围上限(YYYY-MM-DD)
   --n_cores: 使用的CPU核心数

输出结果
~~~~~~~~

在out_path目录（默认为stack文件夹）下会为每个瓦片生成一个{瓦片ID}_stack文件夹，包含按区块组织的堆叠数据。

第二步：SCCD与COLD变化检测处理
------------------------------

SCCD算法
~~~~~~~~

功能说明
^^^^^^^^

使用pyxccd的SCCD算法检测每个像素的变化。

操作步骤
^^^^^^^^

1. 确保已完成上一步的堆叠处理
2. 运行变化检测脚本step2_sccd.py：

.. code:: bash

   python step2_sccd.py --tile_list_fn ./tile_list \
                        --stack_path /stack \
                        --result_parent_path /sccd_results \
                        --yaml_path /config_hls.yaml \
                        --low_datebound 2019-01-01 \
                        --upper_datebound 2024-12-31 \
                        --n_cores 16

参数说明
^^^^^^^^

::

   --stack_path: 上一步生成的堆叠数据目录
   --result_parent_path: SCCD结果输出目录
   其他参数与第一步相同

输出结果
^^^^^^^^

在result_parent_path目录（默认为sccd_results
文件夹）下会为每个瓦片生成一个{瓦片ID}_sccd文件夹，包含:

::

   record_change_x{区块X}_y{区块Y}_sccd.npy: 每个区块的变化检测结果
   SCCD_block{区块编号}_finished.txt: 区块处理完成标记文件

COLD算法
~~~~~~~~

功能说明
^^^^^^^^

使用pyxccd的COLD算法检测每个像素的变化。

操作步骤
^^^^^^^^

1. 确保已完成上一步的堆叠处理
2. 运行变化检测脚本step2_cold.py：

.. code:: bash

   python step2_cold.py --tile_list_fn ./tile_list \
                        --stack_path /stack \
                        --result_parent_path /cold_results \
                        --yaml_path ./config_hls.yaml \
                        --low_datebound 2019-01-01 \
                        --upper_datebound 2024-12-31 \
                        --n_cores 16

参数说明
^^^^^^^^

::

   --stack_path: 上一步生成的堆叠数据目录
   --result_parent_path: COLD结果输出目录
   其他参数与第一步相同

输出结果
^^^^^^^^

在result_parent_path目录（默认为cold_results
文件夹）下会为每个瓦片生成一个{瓦片ID}_cold文件夹，包含:

::

   record_change_x{区块X}_y{区块Y}_cold.npy: 每个区块的变化检测结果
   COLD_block{区块编号}_finished.txt: 区块处理完成标记文件

第三步：生成扰动图
------------------

功能说明
~~~~~~~~

将变化检测结果转换为年度扰动图、最近扰动图和首次扰动图。

操作步骤
~~~~~~~~

1. 确保已完成前两步处理
2. 运行扰动制作脚本step3_disturbance_map.py：

.. code:: bash

   python step3_disturbance_map.py --source_dir /hls \
                                  --result_path /sccd_results/51RTP_sccd \
                                  --out_path /disturbance_maps \
                                  --yaml_path /config_hls.yaml \
                                  --year_lowbound 2019 \
                                  --year_uppbound 2024 \
                                  --n_cores 16

参数说明
~~~~~~~~

::

   --source_dir: HLS数据根目录(用于获取空间参考)
   --result_path: 第二步生成的SCCD结果目录(具体到瓦片)
   --out_path: 扰动图输出目录
   --year_lowbound: 起始年份
   --year_uppbound: 结束年份
   --n_cores: 使用的CPU核心数

输出结果
~~~~~~~~

在out_path目录（默认为disturbance_maps文件夹）下会生成以下文件:

::

   {年份}_break_map_SCCDOFFLINE.tif: 年度扰动图
   recent_disturbance_map_SCCDOFFLINE.tif: 最近扰动图(显示最近发生扰动的年份)
   first_disturbance_map_SCCDOFFLINE.tif: 首次扰动图(显示首次发生扰动的年份)

结果解读
~~~~~~~~

年度扰动图
^^^^^^^^^^

| 像元值 = 扰动类型×1000 + 年积日
| 扰动类型1表示植被扰动
| 扰动类型2表示非植被扰动

最近扰动图
^^^^^^^^^^

| 显示每个像素最近发生扰动的年份
| 无扰动区域值为0

首次扰动图
^^^^^^^^^^

| 显示每个像素首次发生扰动的年份
| 无扰动区域值为0

注意事项
--------

1. 处理大型区域时，建议分批次处理瓦片，避免内存不足。
2. 可根据需要调整config_hls.yaml中的区块大小参数，平衡处理速度和内存使用。
3. 如果处理中断，可以重新运行脚本，程序会自动跳过已完成的区块。

示例效果
--------

2019-2024首次扰动图（sccd）

.. figure:: first_disturb1.png
   :alt: First Disturbance Map

   First Disturbance Map
