from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

def max_depth_iterative(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    
    stack = [(root, 1)]  # 栈中存储节点和当前深度
    max_depth = 0

    while stack:
        node, depth = stack.pop()
        max_depth = max(max_depth, depth)

        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))

    return max_depth
    
    
def is_binary_bst(root: Optional[TreeNode]) -> bool:
    def validate(node, low, high):
        if not node:
            print("Reached a leaf node, returning True")
            return True
        print(f"Validating node with value {node.val} in range ({low}, {high})")
        if node.val <= low or node.val >= high:
            print(f"Node value {node.val} is out of range ({low}, {high}), returning False")
            return False
        
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)

    return validate(root, -float('inf'), float('inf'))

# 236. 二叉树的最近公共祖先
def lowest_common_ancestor(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    if not root and not p and not q:
        return None
    if root == p or root == q:
        return root
    
    
    

if __name__ == "__main__":
    root = TreeNode(5)
    root.left = TreeNode(1)
    root.right = TreeNode(7)
    root.right.left = TreeNode(4)
    root.right.right = TreeNode(8)
    print(is_binary_bst(root))