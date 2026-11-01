# 验证脚本

Python 3，仅使用标准库，无需安装第三方依赖。

| 脚本 | 作用 |
|---|---|
| `exact_worst_case.py N` | 精确穷举 n=3~6 在保底规则下的最坏尝试次数与最坏消耗 |
| `sim2.py` | 单关蒙特卡洛：固定答案 / 绿 / 黄 / 橙 / 红档的消耗分布 |
| `run.py` | 整局模拟：不同初始药水下的失败率、干预率、平均消耗与 P_fail 表 |
| `walk.py` | 复现 V1.1 文档中 55 瓶示例的逐关权重 |
| `trace.py` | 搜索并校验符合理性约束的排列与标记序列 |

```bash
python exact_worst_case.py 4
python sim2.py
python run.py
python walk.py
python trace.py
```

`exact_worst_case.py 6` 需要数分钟（约 36.6 万个搜索状态）。

这些脚本对应 **V1.1 基线模型**（保底进展 + DDA，无随机 T/cap，推荐初始 55 瓶）。最终 Demo 的随机 T/cap + 60 瓶版本由开发者面板内置的模拟器验证；两者的关系和完整结果见 [`../docs/VERIFICATION.md`](../docs/VERIFICATION.md)。
