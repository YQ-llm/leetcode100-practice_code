# 1.两数之和
给定一个整数数组 $nums$ 和一个整数目标值 $target$，请你在该数组中找出 和为目标值 $target$  的那 两个 整数，并返回它们的数组下标。
你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。你可以按任意顺序返回答案。\
解决这个问题最有效的方法是使用 哈希表（Hash Map / 字典）。我们可以将时间复杂度从暴力解法的 $O\left(n^2\right)$ 降低到 $O(n)$
## 算法思路（一遍哈希表）
我们在遍历数组的过程中，对于当前的数字 $num$，我们去计算它需要的“另一半”也就是 $complement = target - num$。
如果我们发现这个“另一半”已经在我们的哈希表里了，说明我们找到了这两个数，直接返回它们的下标即可。
如果“另一半”不在哈希表里，我们就把当前的数字 $num$ 和它的下标 $i$ 存入哈希表中，供后面的数字来查找
## Python3代码实现
```python
from typing import List
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # 创建一个字典用于存储已经遍历过的数字及其下标
        # 格式为 {数字: 它的下标}
        num_dict = {}
        
        for i, num in enumerate(nums):
            # 计算当前数字需要的“另一半”
            complement = target - num
            
            # 如果“另一半”已经在字典中，说明我们找到了这一对数字
            if complement in num_dict:
                return [num_dict[complement], i]
            
            # 如果不在字典中，将当前数字及其下标存入字典，留给后面的数字查找
            num_dict[num] = i
            
        return []

# --- 测试代码 ---
if __name__ == "__main__":
    sol = Solution()
    
    # 测试用例 1
    nums1 = [2, 7, 11, 15]
    target1 = 9
    print(f"输入: nums={nums1}, target={target1}")
    print(f"输出: {sol.twoSum(nums1, target1)}")  # 预期输出: [0, 1]
    
    # 测试用例 2
    nums2 = [3, 2, 4]
    target2 = 6
    print(f"\n输入: nums={nums2}, target={target2}")
    print(f"输出: {sol.twoSum(nums2, target2)}")  # 预期输出: [1, 2]
    
    # 测试用例 3 (测试包含重复元素的情况)
    nums3 = [3, 3]
    target3 = 6
    print(f"\n输入: nums={nums3}, target={target3}")
    print(f"输出: {sol.twoSum(nums3, target3)}")  # 预期输出: [0, 1]
```
## 逻辑图解（以 $nums = [3, 2, 4], target = 6$ 为例）
1.初始状态: num_dict = {}\
2.第 0 步: i = 0, num = 3\
    &emsp;&emsp;需要找的另一半 complement = 6 - 3 = 3。\
    &emsp;&emsp;字典是空的，3 不在字典里。\
    &emsp;&emsp;把当前的 3 存入字典：num_dict = {3: 0}。\
3.第 1 步: i = 1, num = 2\
   &emsp;&emsp; 需要找的另一半 complement = 6 - 2 = 4。\
    &emsp;&emsp;4 不在字典里。\
    &emsp;&emsp;把当前的 2 存入字典：num_dict = {3: 0, 2: 1}。\
4.第 2 步: i = 2, num = 4\
    &emsp;&emsp;需要找的另一半 complement = 6 - 4 = 2。\
    &emsp;&emsp;2 在字典里！ 字典告诉我们 2 的下标是 1。\
    &emsp;&emsp;直接返回 [1, 2]。结束。
## 复杂度分析
时间复杂度: $O(n)$。我们只需要遍历数组一次。字典（哈希表）的查找时间平均为 O(1)，所以总时间复杂度是线性的。\
空间复杂度: $O(n)$。在最坏的情况下（即我们要找的两个数在数组的最后），我们需要将前面 n−1个元素全部存入字典中。
