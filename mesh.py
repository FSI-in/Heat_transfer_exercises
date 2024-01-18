# 网格代码

import numpy as np
from output_vtk import *

class Mesh_geometry(object):
    def __init__(self):
        pass

    def set_mesh_data(self, geometry_x, geometry_y, geometry_z):
        """设置几何边界值"""

        self.geometry_x = geometry_x
        self.geometry_y = geometry_y
        self.geometry_z = geometry_z

    def set_cell_data(self, x_cell, y_cell, z_cell):
        """设置网格数量"""

        self.x_cell = x_cell
        self.y_cell = y_cell
        self.z_cell = z_cell

        # 网格间距
        self.dx = self.geometry_x / self.x_cell
        self.dy = self.geometry_y / self.y_cell
        self.dz = self.geometry_z / self.z_cell

    def set_t_cell(self, t_data):
        """设置温度场"""

        # 温度场
        self.t_1 = np.ones((self.x_cell, self.y_cell, self.z_cell))
        #self.t_1 = np.ones((self.x_cell, self.y_cell, self.z_cell))

        # 更新初始场
        self.t_1 = self.t_1 * t_data

    def set_bo_t(self, n_t, s_t, w_t, e_t, b_t, t_t):
        """设置边界温度"""

        self.n_t = n_t
        self.s_t = s_t
        self.w_t = w_t
        self.e_t = e_t
        self.b_t = b_t
        self.t_t = t_t

    def set_frequency(self,frequency, file_number):

        self.frequency = frequency
        self.file_number = file_number


    def a_numbre(self):

        self.a_x = np.ones((self.x_cell, self.y_cell, self.z_cell, 8))

        # 网格面积
        self.a_xy = self.dx * self.dy
        self.a_yz = self.dy * self.dz
        self.a_xz = self.dx * self.dz

    def set_thermal_conduction(self, tou_h):

        self.tou_h = tou_h

    def compute(self):

        self.a_w = self.tou_h * self.a_yz / self.dx
        self.a_e = self.tou_h * self.a_yz / self.dx

        self.a_n = self.tou_h * self.a_xz / self.dy
        self.a_s = self.tou_h * self.a_xz / self.dy

        self.a_b = self.tou_h * self.a_xy / self.dz
        self.a_t = self.tou_h * self.a_xy / self.dz

        self.a_p = self.a_w + self.a_e + self.a_n + self.a_s + self.a_b + self.a_t

    def input_a_numbre(self):

        for i in range(self.x_cell):
            for j in range(self.y_cell):
                for k in range(self.z_cell):

                    self.a_x[i, j, k, 0] = self.a_w
                    self.a_x[i, j, k, 1] = self.a_e
                    self.a_x[i, j, k, 2] = self.a_n
                    self.a_x[i, j, k, 3] = self.a_s
                    self.a_x[i, j, k, 4] = self.a_b
                    self.a_x[i, j, k, 5] = self.a_t
                    self.a_x[i, j, k, 6] = self.a_p
                    self.a_x[i, j, k, 7] = 0

                    if i == 0:
                        self.a_x[i, j, k, 0] = 0
                        self.a_x[i, j, k, 6] = self.a_x[i, j, k, 6] + self.a_w
                        self.a_x[i, j, k, 7] = self.a_x[i, j, k, 7] + 2*self.a_w * self.w_t
                    if j == 0:
                        self.a_x[i, j, k, 3] = 0
                        self.a_x[i, j, k, 6] = self.a_x[i, j, k, 6] + self.a_s
                        self.a_x[i, j, k, 7] = self.a_x[i, j, k, 7] + 2*self.a_s * self.s_t
                    if k == 0:
                        self.a_x[i, j, k, 4] = 0
                        self.a_x[i, j, k, 6] = self.a_x[i, j, k, 6] + self.a_b
                        self.a_x[i, j, k, 7] = self.a_x[i, j, k, 7] + 2*self.a_b * self.b_t
                    if i == self.x_cell - 1:
                        self.a_x[i, j, k, 1] = 0
                        self.a_x[i, j, k, 6] = self.a_x[i, j, k, 6] + self.a_e
                        self.a_x[i, j, k, 7] = self.a_x[i, j, k, 7] + 2*self.a_e * self.e_t
                    if j == self.y_cell - 1:
                        self.a_x[i, j, k, 2] = 0
                        self.a_x[i, j, k, 6] = self.a_x[i, j, k, 6] + self.a_n
                        self.a_x[i, j, k, 7] = self.a_x[i, j, k, 7] + 2*self.a_n * self.n_t
                    if k == self.z_cell - 1:
                        self.a_x[i, j, k, 5] = 0
                        self.a_x[i, j, k, 6] = self.a_x[i, j, k, 6] + self.a_t
                        self.a_x[i, j, k, 7] = self.a_x[i, j, k, 7] + 2*self.a_t * self.t_t

    # 雅克比迭代
    def yakeb_run(self):
        out_number = 0
        for run in range(1, self.frequency + 1):
            print(run)
            self.t_0 = self.t_1.copy()
            for i in range(self.x_cell):
                for j in range(self.y_cell):
                    for k in range(self.z_cell):
                        if i == 0:
                            self.t_w = 0
                        else:
                            self.t_w = self.t_0[i - 1, j, k]
                        if i == self.x_cell - 1:
                            self.t_e = 0
                        else:
                            self.t_e = self.t_0[i + 1, j, k]

                        if j == 0:
                            self.t_s = 0
                        else:
                            self.t_s = self.t_0[i, j - 1, k]
                        if j == self.y_cell - 1:
                            self.t_n = 0
                        else:
                            self.t_n = self.t_0[i, j + 1, k]

                        if k == 0:
                            self.t_b = 0
                        else:
                            self.t_b = self.t_0[i, j, k - 1]
                        if k == self.z_cell - 1:
                            self.t_t = 0
                        else:
                            self.t_t = self.t_0[i, j, k + 1]

                        t_new = (                                 \
                                  self.a_x[i, j, k, 0] * self.t_w \
                                + self.a_x[i, j, k, 1] * self.t_e \
                                + self.a_x[i, j, k, 2] * self.t_n \
                                + self.a_x[i, j, k, 3] * self.t_s \
                                + self.a_x[i, j, k, 4] * self.t_b \
                                + self.a_x[i, j, k, 5] * self.t_t \
                                + self.a_x[i, j, k, 7]            \
                                )
                        t_new = t_new / self.a_x[i, j, k, 6]
                        self.t_1[i, j, k] = t_new
            if run % self.file_number == 0 or run == self.frequency + 1:
                out_number += 1
                # 生成VTK文件
                write_vtk("temperature_field{}.vtk".format(out_number), self.t_1, self.dx, self.dy, self.dz)




