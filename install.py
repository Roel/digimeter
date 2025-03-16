import patch_ng
import os
import requests


current_dir = os.path.dirname(__name__)
lib_dir = os.path.join(current_dir, 'lib')

output_path = os.path.join(lib_dir, 'p1.py')
diff_path = os.path.join(lib_dir, 'p1_patch.diff')

with open(output_path, 'wb') as output_file:
    r = requests.get(
        'https://raw.githubusercontent.com/Roel/belgian_digitalmeter_p1/refs/heads/main/read_p1.py')
    output_file.write(r.content)

p = patch_ng.fromfile(diff_path)
p.apply(root=lib_dir)
