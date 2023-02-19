import sys, zlib, glob

for file_name in glob.iglob(sys.argv[1] + '/.git/objects/??/*'):
    with open(file_name, 'rb') as file:
        print(file_name + ':', end='\n\n')
        file_decompressed = zlib.decompress(file.read())
        if file_decompressed[:6] == b'commit':
            print(file_decompressed.decode().split('\n', 1)[1], end='\n\n')
        elif file_decompressed[:4] == b'tree':
            result = {}
            id_len = 20
            file_content = file_decompressed.split(b'\x00', 1)[1]
            while file_content:
                file_content_splitted = file_content.split(b'\x00', 1)
                commit_file_name = file_content_splitted[0].decode().split()[-1]
                commit_file_id = file_content_splitted[1][:id_len]
                result[commit_file_name] = commit_file_id
                file_content = file_content[id_len:]
            for commit_file_name in result:
                print(commit_file_name + ':' + result[commit_file_name])
            print('', end='\n\n')
        else:
            print(file_decompressed, end='\n\n')
            
            
