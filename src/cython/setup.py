# 这个文件用于编译 key.pyx 文件: python setup.py build_ext --inplace

from Cython.Build import cythonize
from setuptools import setup, Extension

# 定义 Cython 扩展模块
extensions = [
    Extension(
        name="key",  # 扩展模块的名称
        sources=["key.pyx"],  # Cython 源文件
    )
]

# 使用 cythonize 来编译 Cython 文件
setup(
    name="key",  # 项目名称
    ext_modules=cythonize(extensions),  # 通过 cythonize 生成扩展模块
    zip_safe=False,  # 是否可以被打包到 .egg 文件中
)
