"""
LeetCode 236 — Lowest Common Ancestor of a Binary Tree
后序遍历，自底向上
"""
from typing import Optional

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def lowestCommonAncestor(root: Optional[TreeNode],
                         p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    # Step 1: 遇到 p 或 q 或空 → 直接返回
    if not root or root == p or root == q:
        return root

    # Step 2: 后序 — 先问左右子树
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)

    # Step 3: 核心判断
    if left and right:      # p 和 q 在左右两侧 → 当前就是 LCA
        return root
    return left or right    # 否则上传非空的那一侧


# ---- 测试 ----
if __name__ == "__main__":
    # 构造树
    n3 = TreeNode(3); n5 = TreeNode(5); n1 = TreeNode(1)
    n6 = TreeNode(6); n2 = TreeNode(2); n0 = TreeNode(0)
    n8 = TreeNode(8); n7 = TreeNode(7); n4 = TreeNode(4)
    n3.left, n3.right = n5, n1
    n5.left, n5.right = n6, n2
    n1.left, n1.right = n0, n8
    n2.left, n2.right = n7, n4

    print(f"p=5, q=1 → LCA = {lowestCommonAncestor(n3, n5, n1).val}  (预期: 3)")
    print(f"p=5, q=4 → LCA = {lowestCommonAncestor(n3, n5, n4).val}  (预期: 5)")
    print(f"p=6, q=4 → LCA = {lowestCommonAncestor(n3, n6, n4).val}  (预期: 5)")
    print(f"p=7, q=8 → LCA = {lowestCommonAncestor(n3, n7, n8).val}  (预期: 3)")
