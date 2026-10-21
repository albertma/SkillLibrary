"""
LeetCode 42 - Trapping Rain Water (接雨水)
最优解：双指针法，O(n) 时间，O(1) 空间
"""
def trap(height: list[int]) -> int:
    """计算能接住的雨水总量"""
    if not height:          # 边界情况：空数组
        return 0

    left, right = 0, len(height) - 1  # 左右双指针
    water = 0                         # 累计雨水总量
    left_max, right_max = height[left], height[right]  # 左右两侧最高柱子

    while left < right:
        # 更新当前左右两侧的最高值
        left_max = max(left_max, height[left])
        right_max = max(right_max, height[right])

        # 核心逻辑：哪边"短板"决定了当前能接多少水
        if left_max < right_max:
            # 左边是短板，left位置的水量 = 左侧最高 - 当前高度
            water += left_max - height[left]
            left += 1   # 左指针右移
        else:
            # 右边是短板（含相等情况），right位置的水量 = 右侧最高 - 当前高度
            water += right_max - height[right]
            right -= 1  # 右指针左移

    return water


if __name__ == "__main__":
    # 测试用例 1：经典示例
    height1 = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(f"height = {height1}")
    print(f"接雨水量: {trap(height1)}")  # 预期: 6

    # 测试用例 2：简单递增，接不住水
    height2 = [0, 1, 1, 2]
    print(f"\nheight = {height2}")
    print(f"接雨水量: {trap(height2)}")  # 预期: 0

    # 测试用例 3：经典凹槽
    height3 = [5, 0, 5]
    print(f"\nheight = {height3}")
    print(f"接雨水量: {trap(height3)}")  # 预期: 5

    # 测试用例 4：平顶
    height4 = [5, 5, 5, 5]
    print(f"\nheight = {height4}")
    print(f"接雨水量: {trap(height4)}")  # 预期: 0

    # 测试用例 5：空数组
    height5 = []
    print(f"\nheight = {height5}")
    print(f"接雨水量: {trap(height5)}")  # 预期: 0

    # 测试用例 6：单元素
    height6 = [3]
    print(f"\nheight = {height6}")
    print(f"接雨水量: {trap(height6)}")  # 预期: 0
