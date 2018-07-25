# -*- coding: utf-8 -*-
from fabric.api import task, run, local, env, cd, prefix

ENVIRONMENT = {
    'staging': '',
    'production': {
        'user': 'user',
        'hosts': ['127.0.0.1'],
        'branch': 'master',
        'root': '',
        'venv': None,
        'docker': None,
        'supervisor': None,
        'run_command': None,
        'requirements': 'requirements/production.txt'
    },
}


def active_env(name):
    """
    Подготовка окружения
    """
    local_env = ENVIRONMENT.get(name, None)
    if not local_env:
        raise RuntimeError('Не найдено окружение')
    for key, value in local_env.iteritems():
        setattr(env, key, value)


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
def deploy(branch=None, build=False):
    branch = branch or env.branch

    # Пушим все локальные изменения
    local('git push origin %s' % branch)

    # Заливаем изменения на сервер
    with cd(env.root):
        run('git fetch origin %s' % branch)
        run('git checkout %s' % branch)
        run('git pull origin %s' % branch)

    # TODO: Дамп базы данных перед миграциями

    # Выполняем команды django
    with cd(env.root):
        if env.docker is not None:
            if build:
                run('%s build' % env.docker)
                run('%s down' % env.docker)
            run('%s up -d' % env.docker)
            run('%s python manage.py collectstatic --noinput' % env.docker)
            run('%s python manage.py migrate' % env.docker)
        elif env.venv:
            with prefix(env.venv):
                run('python manage.py collectstatic --noinput')
                run('python manage.py migrate')
            run('supervisorctl restart %s' % env.supervisor)

        if env.run_command:
            if not isinstance(env.run_command, list):
                env.run_command = [env.run_command]
            for command in env.run_command:
                run(command)


# ==============================================================================
# Docker
# ==============================================================================

@task
def build():
    local('docker-compose build')


@task
def start(port='8000'):
    with prefix('export APP_PORT=%s' % port):
        local('docker-compose up -d')


@task
def stop():
    local('docker-compose down')


@task
def status():
    local('docker-compose ps')


@task
def migrate(app='', fake=False):
    local('docker-compose exec django python manage.py migrate %s %s' % (
        app, '--fake-initial' if fake else ''
    ))


@task
def makemigrations(app=''):
    local('docker-compose exec django python manage.py makemigrations %s' % app)


@task
def runserver():
    local('docker-compose exec django python manage.py runserver 0.0.0.0:8000')


@task
def celeryw():
    local('docker-compose exec django celery -A {{ project_name }} worker -l info -B')


@task
def celeryb():
    local('docker-compose exec django celery -A {{ project_name }} beat')


@task
def shell():
    local('docker-compose exec django python manage.py shell')


@task
def manage(command):
    local('docker-compose exec django python manage.py %s' % command)


@task
def runtests(app=''):
    local('docker-compose exec django python manage.py test %s --keepdb' % app)
