# ARG 行动链路动态演示与成片脚本

这是一个知识分享类动态 HTML，用“Agent 参与 ARG 游戏”的方式介绍 ARG 行动链路。

## 预览

直接打开：

```text
index.html
```

自动播放：

```text
index.html?autoplay=1
```

指定页码截图：

```text
index.html?slide=3&recording=1
```

## 控制

- `← / →`：上一页 / 下一页
- `Space`：播放 / 暂停
- `N`：显示 / 隐藏演讲稿
- `R`：录屏模式
- `F`：全屏

## 成片

`make_video.py` 会：

1. 用 Chrome/Edge 对每页 HTML 截图；
2. 调用阿里百炼 `qwen3-tts-instruct-flash` 的 `multimodal-generation/generation` 接口生成旁白；
   默认音色为 `Kai`，并通过 `instructions` 让语速偏快、节奏更适合知识分享视频；
3. 用 `ffmpeg` 合成最终 MP4。

运行：

```bash
python make_video.py
```

默认读取仓库上级目录的 `阿里tts-apikey.txt`，也可以使用环境变量 `DASHSCOPE_API_KEY`。

输出：

```text
arg-action-chain-intro.mp4
```
