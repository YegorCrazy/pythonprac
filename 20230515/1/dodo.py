DOIT_CONFIG = {"default_tasks": ["html"]}

def task_extract():
    return {
        'actions': [
            'pybabel extract -o ./moodserver/moodserver/l10n.pot ./moodserver/moodserver/text_to_translate.py',
            ],
        'targets': [
            'l10n.pot',
            ],
        }


def task_update():
    return {
        'actions': [
            'pybabel update -D l10n -d ./moodserver/moodserver/l10n -l ru -i ./moodserver/moodserver/l10n.pot',
            ],
        'task_dep': [
            'extract',
            ],
        }


def task_compile():
    return {
        'actions': [
            'pybabel update -D l10n -d ./moodserver/moodserver/l10n -l ru -i ./moodserver/moodserver/l10n.pot',
            ],
        'task_dep': [
            'update',
            ],
        'targets': [
            'l10n.mo',
            ],
        }


def task_l10n():
    return {
        'actions': [],
        'task_dep': [
            'compile',
            ],
        }


def task_test():
    return {
        'actions': [
            'python3 -m unittest client_tests.py',
            ],
        'task_dep': [
            'l10n',
            ],
        }


def task_html():
    return {
        'actions': [
            'make html',
            ],
        }


def task_wheel_server():
    return {
        'actions': ['python3 -m build -n -w moodserver'],
        }


def task_wheel_client():
    return {
        'actions': ['python3 -m build -n -w moodclient'],
        }


def task_wheels():
    return {
        'actions': [],
        'task_dep': ['wheel_server', 'wheel_client'],
        }
