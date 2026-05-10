## RoPE旋转位置实现
## 原理、NTK、YARN需掌握
```python
def precompute_freqs_cis(dim, end, theta=1e6):
    """预计算旋转位置编码的复数频率

    Args:
        dim: head_dim（注意不是 d_model），MiniMind 中为 96
        end: 最大序列长度
        theta: 基础频率，MiniMind 使用 1e6（较大，利于长文本）

    Returns:
        freqs_cis: (end, dim//2) 的复数张量，每个元素 = e^{i*m*θ_k}
    """
    # 计算 48 组（dim//2=96//2=48）不同频率
    # 频率公式: θ_k = 1 / theta^(2k/dim), k=0,1,...,47
    # 低维度组(k小) → θ_k大 → 旋转快 → 捕捉近距离关系
    # 高维度组(k大) → θ_k小 → 旋转慢 → 捕捉远距离关系
    freqs = 1.0 / (theta ** (torch.arange(0, dim, 2)[: (dim // 2)].float() / dim))

    # 位置索引: [0, 1, 2, ..., end-1]
    t = torch.arange(end, device=freqs.device)

    # 外积: freqs[m, k] = m * θ_k，即位置 m 在第 k 组的旋转角度
    freqs = torch.outer(t, freqs)  # (end, dim//2)

    # 转为复数: e^{i*角度} = cos(角度) + i*sin(角度)
    # 复数乘法天然实现二维旋转
    freqs_cis = torch.polar(torch.ones_like(freqs), freqs)
    return freqs_cis


def apply_rotary_emb(xq, xk, freqs_cis):
    """将旋转位置编码应用到 Q 和 K 上

    核心技巧：将相邻两个实数维度视为一个复数，
    然后用复数乘法完成旋转（比手写旋转矩阵更简洁高效）
    """
    # 将最后一维两两配对成复数: (..., dim) → (..., dim//2) complex
    xq_ = torch.view_as_complex(xq.float().reshape(*xq.shape[:-1], -1, 2))
    xk_ = torch.view_as_complex(xk.float().reshape(*xk.shape[:-1], -1, 2))

    # 复数乘法 = 旋转！
    # (a + bi) * (cosθ + i sinθ) = (a cosθ - b sinθ) + i(a sinθ + b cosθ)
    xq_out = torch.view_as_real(xq_ * freqs_cis).flatten(-2)
    xk_out = torch.view_as_real(xk_ * freqs_cis).flatten(-2)

    return xq_out.type_as(xq), xk_out.type_as(xk)
```
