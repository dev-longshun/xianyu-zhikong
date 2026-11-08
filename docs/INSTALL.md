# 闲鱼智控安装指南

[返回产品介绍](../README.md) · [下载最新版](https://github.com/dev-longshun/xianyu-zhikong/releases/latest)

## Mac（Apple 芯片）

适用于 Apple M 系列芯片、macOS 11 及以上系统，暂不支持 Intel Mac。

1. 在 [Releases](https://github.com/dev-longshun/xianyu-zhikong/releases/latest) 下载文件名带 `mac-arm64.dmg` 的安装包。
2. 打开 DMG，将「闲鱼智控」拖进「应用程序」。
3. 在「应用程序」中打开闲鱼智控。系统首次询问是否打开从互联网下载的 App 时，确认打开。
4. 可以先查看界面；需要登录闲鱼店铺时，联系作者购买激活码并完成激活。

客户端运行并联网时，自动化任务才会工作。需要长时间运行时，可在客户端设置里开启「挂机不休眠」。

## Windows（64 位）

适用于 64 位 Windows 10 / 11。

1. 在 [Releases](https://github.com/dev-longshun/xianyu-zhikong/releases/latest) 下载文件名带 `windows-x64.exe` 的安装包。
2. 运行安装包，按向导选择安装目录并完成安装。
3. 从桌面快捷方式或开始菜单打开「闲鱼智控」。
4. 可以先查看界面；需要登录闲鱼店铺时，联系作者购买激活码并完成激活。

当前 Windows 安装包没有微软代码签名。若 SmartScreen 显示「Windows 已保护你的电脑」，先确认文件来自本仓库 Releases 或官网，并核对校验值；确认来源后，可在「更多信息」中选择「仍要运行」。遇到其他安全软件提示，请先核对来源与具体提示，再联系作者。

第一次安装也可以参考官网提供的 [Windows 图文安装与激活教程](https://xianyu.dongeai.com/tutorials/windows/)，包含完整操作截图。

## 下载慢或中断

可改用官网备用下载：

- [Mac · Apple 芯片](https://dl.longjinapi.com/xianyu-zhikong-mac-arm64.dmg)
- [Windows · 64 位](https://dl.longjinapi.com/xianyu-zhikong-windows-x64.exe)

## 校验下载文件

每个 GitHub Release 附有 `SHA256SUMS.txt`，记录该版本安装包的 SHA-256。下载完成后计算文件摘要，与同一 Release 中的记录比较。

Mac 终端：

```sh
shasum -a 256 ~/Downloads/xianyu-zhikong-1.6.0-mac-arm64.dmg
```

Windows PowerShell：

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\xianyu-zhikong-1.6.0-windows-x64.exe" -Algorithm SHA256
```

## 激活与联系

基础版 **19 元 / 月**（每台电脑登录 1 个闲鱼账号），高级版 **29 元 / 月**（账号数量不限），一份授权都可激活两台电脑，详见[价格页](https://xianyu.dongeai.com/pricing/)。微信：`OxRabbitno1`（首字母为大写字母 O）。

[返回购买与联系](../README.md#购买与联系)
