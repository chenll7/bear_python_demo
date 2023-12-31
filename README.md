# Bear Python Demo

Python项目示例。

## Getting Started

1. 虚拟环境初始化：执行`.\tool\install_venv.cmd`。

2. 交互模式进入虚拟环境：执行`.\venv\Scripts\activate`。

3. 下载所有三方依赖包：执行`.\tool\download_dep.cmd`。

4. 以editable方式安装当前包到虚拟环境，并安装三方依赖包：执行`.\tool\install_for_dev.cmd`。

5. 当前包打包到package目录，三方依赖包复制到package目录：执行`.\tool\package.cmd`。

6. 构建安装包，生成升级包：执行`.\tool\release.cmd`。

7. 升级包复制到发布目录，并执行升级操作：执行`.\tool\publish.cmd`。