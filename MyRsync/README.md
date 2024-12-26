# Sync Tools in HPC

这个东西的功能是将集群中的一个文件夹、文件原封不动地拷贝到另一个集群中，当parent dir 没有创建时会自动创建。

## 编译

```bash
cd MySync
pip install pyinstaller
./build.sh
```

## 添加到系统PATH

```bash
export PATH=$HOME/work/MyRsync/dist:$PATH
```

在 .bashrc 中添加

```
alias push='myrsync -m push -c'
alias pull='myrsync -m pull -c'
```

## 使用

```
# 在引力 可以使用push
push <文件夹 | 文件名 | 正则表达式>

# 在强磁场 可以使用pull
pull <文件夹 | 文件名 | 正则表达式> # 一般不怎么用
```

## 注意

最好是自己申请一个cpu实例 挂在后台进行拷贝 可以配合使用 nrun 命令
