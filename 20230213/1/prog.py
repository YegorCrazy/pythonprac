import sys, zlib, glob

def print_tree_file(tree_file, base_address, recursive=False):
    tree_file_decompressed = zlib.decompress(tree_file.read())
    result = {}
    id_len = 20
    tree_file_content = tree_file_decompressed.partition(b'\x00')[2]
    while tree_file_content:
        tree_file_content_splitted = tree_file_content.partition(b'\x00')
        item_file_name = tree_file_content_splitted[0].split()[-1].decode()
        item_type_code = tree_file_content_splitted[0].split()[0]
        if item_type_code == b'40000':
            item_type = 'tree'
        else:
            item_type = 'blob'
        item_file_id = tree_file_content_splitted[2][:id_len]
        result[item_file_name] = [item_file_id.hex(), item_type]
        tree_file_content = tree_file_content_splitted[2][id_len:]
    for item_file_name in result:
        print(item_type, result[item_file_name][0], item_file_name)
    print('', end='\n')
    if recursive:
        for item_file_name in result:
            if result[item_file_name][1] == 'tree':
                with open(base_address +
                          '/.git/objects/' +
                          result[item_file_name][0][:2] +
                          '/' +
                          result[item_file_name][0][2:],
                          'rb') as new_tree_file:
                    print('subtree', result[item_file_name][0])
                    print_tree_file(new_tree_file, base_address, recursive)

if len(sys.argv) == 1:
    print('path to directory with .git unspecified')

if len(sys.argv) == 2:
    for file_name in glob.iglob(sys.argv[1] + '/.git/refs/heads/*', recursive=True):
        branch_name = file_name.split('/')[-1]
        if branch_name != '.':
            print(branch_name)
    exit()
else:
    branch_name = sys.argv[2]
    with open(sys.argv[1] + '/.git/refs/heads/' + branch_name, 'r') as head_file:
        last_commit_id = head_file.read().split()[0]
    while last_commit_id:
        with open(sys.argv[1] +
                  '/.git/objects/' +
                  last_commit_id[:2] +
                  '/' +
                  last_commit_id[2:],
                  'rb') as commit_file:
            commit_file_decompressed = zlib.decompress(commit_file.read())
            commit_file_payload = commit_file_decompressed.partition(b'\x00')[2].decode().strip()
            print(commit_file_payload, end='\n\n')
            tree_id = commit_file_payload.split('tree', 1)[1].split()[0]
            print('TREE for commit', last_commit_id)
            if commit_file_payload.find('parent') != -1:
                last_commit_id = commit_file_payload.split('parent', 1)[1].split()[0]
            else:
                last_commit_id = ''
            with open(sys.argv[1] +
                      '/.git/objects/' +
                      tree_id[:2] +
                      '/' +
                      tree_id[2:],
                      'rb') as tree_file:
                print_tree_file(tree_file, sys.argv[1], True)
    exit()
