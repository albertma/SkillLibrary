"""
二叉树三种遍历 — 递归 & 迭代 完整模板 + 应用场景
"""
from typing import Optional, List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# ============================================================
# 示例树：
#         1
#        / \
#       2   3
#      / \
#     4   5
#
# 前序:  1→2→4→5→3
# 中序:  4→2→5→1→3
# 后序:  4→5→2→3→1
# ============================================================

def build_sample_tree() -> TreeNode:
    n4 = TreeNode(4)
    n5 = TreeNode(5)
    n2 = TreeNode(2, n4, n5)
    n3 = TreeNode(3)
    n1 = TreeNode(1, n2, n3)
    return n1


# ============================================================
# 1️⃣ 前序遍历 (Preorder) — 根 → 左 → 右
# ============================================================
def preorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """递归前序"""
    if not root:
        return []
    return [root.val] + preorder_recursive(root.left) + preorder_recursive(root.right)

def preorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """迭代前序 — 用栈模拟"""
    if not root:
        return []
    stack, res = [root], []
    while stack:
        node = stack.pop()
        res.append(node.val)
        if node.right:      # 先右后左，因为栈是LIFO
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return res


# ============================================================
# 2️⃣ 中序遍历 (Inorder) — 左 → 根 → 右
# ============================================================
def inorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """递归中序"""
    if not root:
        return []
    return inorder_recursive(root.left) + [root.val] + inorder_recursive(root.right)

def inorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """迭代中序 — 关键：一路向左压栈"""
    stack, res = [], []
    cur = root
    while stack or cur:
        while cur:                  # 一直往左走
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()          # 弹出，访问
        res.append(cur.val)
        cur = cur.right             # 转向右子树
    return res


# ============================================================
# 3️⃣ 后序遍历 (Postorder) — 左 → 右 → 根
# ============================================================
def postorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """递归后序"""
    if not root:
        return []
    return postorder_recursive(root.left) + postorder_recursive(root.right) + [root.val]

def postorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """迭代后序 — 前序的变体 (根→右→左 然后反转)"""
    if not root:
        return []
    stack, res = [root], []
    while stack:
        node = stack.pop()
        res.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return res[::-1]  # 反转 = 左→右→根


# ============================================================
# 4️⃣ 层序遍历 (Level Order / BFS)
# ============================================================
def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """BFS逐层"""
    if not root:
        return []
    from collections import deque
    q, res = deque([root]), []
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level)
    return res


# ============================================================
# 执行 + 对比
# ============================================================
if __name__ == "__main__":
    root = build_sample_tree()

    print("         1")
    print("        / \\")
    print("       2   3")
    print("      / \\")
    print("     4   5")
    print()

    print(f"{'遍历方式':<10} {'递归':<20} {'迭代':<20}")
    print("-" * 50)
    print(f"{'前序':<10} {str(preorder_recursive(root)):<20} {str(preorder_iterative(root)):<20}")
    print(f"{'中序':<10} {str(inorder_recursive(root)):<20} {str(inorder_iterative(root)):<20}")
    print(f"{'后序':<10} {str(postorder_recursive(root)):<20} {str(postorder_iterative(root)):<20}")
    print(f"{'层序':<10} {str(level_order(root)):<20}")
