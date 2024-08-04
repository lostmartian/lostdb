import os

def get_page_size():
    try:
        page_size = os.sysconf('SC_PAGE_SIZE')
        return page_size
    except (AttributeError, ValueError, OSError):
        print("Could not determine the page size")
        return None
    
PAGE_NUM_SIZE = get_page_size()

class Item:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Node:
    def __init__(self, dal=None, page_num=None, items=None, child_nodes=None):
        self.dal = dal
        self.page_num = page_num
        self.items = items if items is not None else []
        self.child_nodes = child_nodes if child_nodes is not None else []

    @classmethod
    def new_empty_node(cls):
        return cls()

    @staticmethod
    def new_item(key, value):
        return Item(key, value)

    def is_leaf(self):
        return len(self.child_nodes) == 0
    
    def serialize(self, buf):
        left_pos = 0
        right_pos = len(buf) - 1
        # Add page header: isLeaf, key-value pairs count
        is_leaf = self.is_leaf()
        buf[left_pos] = 1 if is_leaf else 0
        left_pos += 1
        # Key value pair
        buf[left_pos:] = len(self.items).to_bytes(2, byteorder='little')
        left_pos += 2

        # Serialize key-value pairs and child pointers if present
        for i in range(len(self.items)):
            item = self.items[i]
            if not is_leaf:
                child_node = self.child_nodes[i]
                buf[left_pos:] = child_node.to_bytes(PAGE_NUM_SIZE, byteorder='little')
                left_pos += PAGE_NUM_SIZE
        
        klen = len(item.key)
        vlen = len(item.value)
        offset = right_pos - klen - vlen - 2
        buf[left_pos:left_pos + 2] = offset.to_bytes(2, byteorder='little')
        left_pos += 2


# Example usage
node = Node.new_empty_node()
item = Node.new_item(b'key', b'value')
print(node.is_leaf())  # True
