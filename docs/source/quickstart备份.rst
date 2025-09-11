=================
Python Tutorial
=================

本教程将指导您如何使用pyxccd处理HLS影像数据，生成年度扰动图、最近扰动图和首次扰动图。整个过程分为三个主要步骤。

准备工作
=================

1.安装必要的Python库：
~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: console

    pip install numpy pandas click rasterio pyxccd scipy...

2.准备好下载的HLS文件，确保数据按如下结构组织：（示例提供2019-2024六年的HLS数据）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HLS根目录/
└── 瓦片ID (如51RTP)/
└── HLS影像文件 (如HLS.S30.T51RTP.2021001.v2.0.B02.tif)

3.准备配置文件config_hls.yaml，可根据需要调整config_hls.yaml中的区块大小参数（示例文件分为30×30块）：
~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: console

    DATASETINFO:
        n_rows: 3660
        n_cols: 3660
        n_block_x: 30
        n_block_y: 30

第一步：影像堆叠处理
=====================

功能说明：
~~~~~~~~~~~~~~~~~~~~~~~~
将HLS影像按时间序列堆叠，为后续变化检测做准备。