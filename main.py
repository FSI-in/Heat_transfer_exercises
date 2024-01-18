# 主程序

from mesh import *


# _____________________
#        设置

# 网格三维尺寸
geometry_x = 50
geometry_y = 50
geometry_z = 50

# 网格数量
x_cell = 50
y_cell = 50
z_cell = 50

# 初始温度场
t_data = 0

# 热传导系数
tou_h = 81

# 边界温度场
n_t = 10
s_t = 0
w_t = 0
e_t = 0
b_t = 0
t_t = 0

# 迭代次数
frequency = 2000

# 设置输出间隔步
file_number = 10
# ____________________

# 这里默认网格厚度为dx和dy的最小值。

# 创建网格对象
mesh = Mesh_geometry()

# 设置网格边界
mesh.set_mesh_data(geometry_x, geometry_y, geometry_z)

# 设置网格尺寸
mesh.set_cell_data(x_cell, y_cell, z_cell)

# 设置初始温度场
mesh.set_t_cell(t_data)

# 设置边界温度
mesh.set_bo_t(n_t, s_t, w_t, e_t, b_t, t_t)

# 设置热传导系数
mesh.set_thermal_conduction(tou_h)

# 设置迭代次数
mesh.set_frequency(frequency, file_number)

mesh.a_numbre()

mesh.compute()

mesh.input_a_numbre()

mesh.yakeb_run()



