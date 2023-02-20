import subprocess

folders = ['20220913', '20220920', '20220927', '20221004', '20221011', '20221018', '20221025', '20221101', '20221108', '20221115', '20221122', '20221129']
tasks = [2, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 2]

links = ['https://github.com/anti-monium/pythonprac/tree/main/',
         'https://gitlab.com/venticinque/pythonprac/-/tree/main/',
         'https://git.cs.msu.ru/s02200328/pythonprac/-/tree/main/']

for folder_num in range(len(folders)):
    for task_num in range(tasks[folder_num]):
        with open('URLS', 'w') as file:
            for url in links:
                file.write(url + folders[folder_num] + '/' + str(task_num + 1) + '/tests\n')
        subprocess.run(['mv', 'URLS', './' + folders[folder_num] + '/' + str(task_num + 1)])


