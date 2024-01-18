import numpy as np

def write_vtk(filename, temperature_field, dx, dy, dz):
    nx, ny, nz = temperature_field.shape

    with open(filename, 'w') as vtk_file:
        # 1. VTK文件头部信息
        vtk_file.write("# vtk DataFile Version 3.0\n")
        vtk_file.write("Temperature Field\n")
        vtk_file.write("ASCII\n")
        vtk_file.write("DATASET STRUCTURED_GRID\n")
        vtk_file.write(f"DIMENSIONS {nx+1} {ny+1} {nz+1}\n")
        vtk_file.write(f"POINTS {(nx+1)*(ny+1)*(nz+1)} float\n")

        # 2. VTK文件数据结构
        for k in range(nz+1):
            for j in range(ny+1):
                for i in range(nx+1):
                    vtk_file.write(f"{i*dx} {j*dy} {k*dz}\n")

        vtk_file.write("\nCELL_DATA " + str(nx * ny * nz) + "\n")
        vtk_file.write("SCALARS Temperature float 1\n")
        vtk_file.write("LOOKUP_TABLE default\n")

        # 3. 将温度场数据存储在网格中心
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    vtk_file.write(str(temperature_field[i, j, k]) + "\n")

# 示例使用
# 生成一个示例的三维数组温度场数据
temperature_field = np.random.rand(5, 5, 5)

# 自定义dx、dy、dz的值
dx, dy, dz = 1.0, 1.0, 1.0

# 生成VTK文件
write_vtk("temperature_field.vtk", temperature_field, dx, dy, dz)
