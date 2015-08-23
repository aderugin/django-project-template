# -*- coding: utf-8 -*-
from datetime import datetime
import os

from fabric.api import task
from fabric.api import run
from fabric.api import local
from fabric.api import env
from fabric.api import cd
from fabric.api import get
from fabric.api import lcd
from fabric.api import prefix
from fabric.api import sudo
from fabric.api import hide
from fabric.api import shell_env

from fabric.contrib.files import append
from fabric.contrib.files import exists


# TODO: Дамп media

# TODO: Обновление базы данных и media на локальном компьютере

# TODO: Перенести все медиа на s3 на локальном компьютере


REQUIREMENTS_NAME = 'requierements.txt'
# Папка для дампа db на сервере
DB_BACKUPS_ROOT = 'db_backups/'  # <path>/

MARKUP_DIRECTORY = ''

LOCAL_SSH_KEY_PATH = os.path.expanduser('~/.ssh/id_rsa.pub')

ENVIRONMENT = {
    'staging': '',
    'production': {
        # Пользователь на сервере
        'user': 'autosignal',
        # Хосты на которых расположен проект.
        'host': [''],  # django@127.0.0.1
        # Ветка
        'branch': 'master',
        # Путь до папки с media
        'media_root': '',
        # Папка с проектом на сервере
        'root_dir': '',
        # Путь до virtualenv директории на серверах
        'venv': 'source <path>/bin/activate',
        # Пользователь базы данных
        'db_user': 'root',
        # Пароль базы данных
        'db_password': '',
        # Имя базы данных
        'db_name': '',
        # Название процесс supervisor
        'supervisor_name': '<>:site'
    },
}


env.key_filename = LOCAL_SSH_KEY_PATH


def active_env(name):
    """
    Подготовка окружения
    """
    local_env = ENVIRONMENT.get(name, None)
    if not local_env:
        raise RuntimeError("Не найдено окружение")

    env.user = local_env['user']
    env.hosts = local_env['host']
    env.root = local_env['root_dir']
    env.media_root = local_env['media_root']
    env.branch = local_env['branch']
    env.activate = local_env['venv']
    env.db_user = local_env['db_user']
    env.db_password = local_env['db_password']
    env.db_name = local_env['db_name']
    env.supervisor_name = local_env['supervisor_name']


@task
def staging():
    """
    Подготовка окружения тестового сервера
    """
    active_env('staging')


@task
def production():
    """
    Подготовка окружения рабочего сервера
    """
    active_env('production')


@task
def push_ssh_key():
    """
    Загрузка ssh ключа
    """
    with open(LOCAL_SSH_KEY_PATH, 'r') as keyf:
        key = keyf.read()
        with cd('~/.ssh/'):
            append('authorized_keys', key)


@task
def deploy():
    # Пушим все локальные изменения
    local('git push origin master')
    # Если верстка отдельный репозиторий
    if MARKUP_DIRECTORY:
        with lcd(MARKUP_DIRECTORY):
            local('git push origin master')

    # Заливаем изменения на сервер
    with cd(env.root):
        run('git pull origin master')
        # Заливаем верстку
        if MARKUP_DIRECTORY:
            with cd(MARKUP_DIRECTORY):
                run('git pull origin master')

    # Если папки для дмапов нет, то создаем ее
    if not exists('~/%s' % DB_BACKUPS_ROOT):
        run('mkdir ~/%s' % DB_BACKUPS_ROOT)
    # Дамп базы данных
    run('mysqldump -u %s -p%s %s > ~/%s%s' %
        (env.db_user, env.db_password, env.db_name, DB_BACKUPS_ROOT,
            '{0}_{1}.sql'.format(env.db_name, datetime.strftime(datetime.now(), '%d.%m.%y_%M:%S'))))

    # Выполняем команды django
    with cd(env.root):
        with prefix(env.activate):
            run('python manage.py collectstatic --noinput')
            run('python manage.py migrate')

    # Перезагружаем web сервер
    sudo('supervisorctl restart ' + env.supervisor_name)
    # TODO: логирование


@task
def install():
    """
    Установка зависимостей

    Аргументы:
        - :branch: Ветка из которой берутся изменения, по умолчанию текущий для окружения
    """
    with cd(env.root):
        # Обновляем зависимости для проекта
        with prefix(env.activate):
            run('pip install -r ' + REQUIREMENTS_NAME)


@task
def dump_db():
    """
    Создание дампа базы данных и его загрузка
    """
    dump_name = '{0}_{1}'.format(env.db_name, datetime.strftime(datetime.now(), '%d.%m.%y_%M:%S'))

    run('mysqldump -u %s -p%s %s > ~/%s%s' %
        (env.db_user, env.db_password, env.db_name, DB_BACKUPS_ROOT,
            '{0}_{1}.sql'.format(env.db_name, dump_name)))

    get('~/%s%s' % (DB_BACKUPS_ROOT, dump_name), 'db/')


@task
def dump_media():
    """
    Создание дампа media и его загрузка
    """
    pass
