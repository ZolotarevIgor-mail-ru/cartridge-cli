import os
import shutil

from utils import Cli
from utils import get_instance_id, get_stateboard_name
from utils import check_instances_running, check_instances_stopped
from utils import DEFAULT_CFG
from utils import DEFAULT_SCRIPT
from utils import STATUS_NOT_STARTED, STATUS_RUNNING, STATUS_STOPPED
from utils import wait_instances
from utils import write_conf


# #####
# Tests
# #####
def test_start_interactive_by_id(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')

    # start instance-1
    cli.start(project, [ID1])
    check_instances_running(cli, project, [ID1])


def test_start_stop_by_id(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    ID2 = get_instance_id(project.name, 'instance-2')

    # start instance-1
    cli.start(project, [ID1], daemonized=True)
    cli.start(project, [ID2], daemonized=True)
    # cli.start(project, [ID1, ID2], daemonized=True)
    check_instances_running(cli, project, [ID1, ID2], daemonized=True)

    # stop instance-1
    cli.stop(project, [ID1])
    check_instances_running(cli, project, [ID2], daemonized=True)
    check_instances_stopped(cli, project, [ID1])


def test_start_interactive_by_id_with_stateboard(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    # ID2 = get_instance_id(project.name, 'instance-2')

    # start instance-1
    cli.start(project, [ID1], stateboard=True)
    check_instances_running(cli, project, [ID1], stateboard=True)


def test_start_interactive_stateboard_only(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    # start with stateboard-only flag
    cli.start(project, stateboard_only=True)
    check_instances_running(cli, project, stateboard_only=True)


def test_start_stop_by_id_with_stateboard(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    ID2 = get_instance_id(project.name, 'instance-2')

    # start instance-1 and stateboard
    cli.start(project, [ID1], daemonized=True, stateboard=True)
    # start instance-2
    cli.start(project, [ID2], daemonized=True)
    check_instances_running(cli, project, [ID1, ID2], daemonized=True, stateboard=True)

    # stop instance-1 and stateboard
    cli.stop(project, [ID1], stateboard=True)
    check_instances_running(cli, project, [ID2], daemonized=True)
    check_instances_stopped(cli, project, [ID1], stateboard=True)


def test_start_stop_stateboard_only(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    # start with stateboard-only flag
    cli.start(project, daemonized=True, stateboard_only=True)
    check_instances_running(cli, project, daemonized=True, stateboard_only=True)

    # stop stateboard
    cli.stop(project, stateboard_only=True)
    check_instances_stopped(cli, project, stateboard_only=True)


def test_start_interactive_from_conf(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    ID2 = get_instance_id(project.name, 'instance-2')

    write_conf(os.path.join(project.path, DEFAULT_CFG), {
        ID1: {},
        ID2: {},
    })

    # start instances
    cli.start(project)
    check_instances_running(cli, project, [ID1, ID2])


def test_start_stop_from_conf(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    ID2 = get_instance_id(project.name, 'instance-2')

    write_conf(os.path.join(project.path, DEFAULT_CFG), {
        ID1: {},
        ID2: {},
    })

    # start instances
    cli.start(project, daemonized=True)
    check_instances_running(cli, project, [ID1, ID2], daemonized=True)

    # stop instances
    cli.stop(project)
    check_instances_stopped(cli, project, [ID1, ID2])


def test_start_interactive_from_conf_with_stateboard(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    ID2 = get_instance_id(project.name, 'instance-2')

    write_conf(os.path.join(project.path, DEFAULT_CFG), {
        ID1: {},
        ID2: {},
    })

    # start instances
    cli.start(project, stateboard=True)
    check_instances_running(cli, project, [ID1, ID2], stateboard=True)


def test_start_interactive_from_conf_stateboard_only(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    ID2 = get_instance_id(project.name, 'instance-2')

    write_conf(os.path.join(project.path, DEFAULT_CFG), {
        ID1: {},
        ID2: {},
    })

    # start instances
    cli.start(project, stateboard_only=True)
    check_instances_running(cli, project, stateboard_only=True)


def test_start_stop_from_conf_with_stateboard(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    ID2 = get_instance_id(project.name, 'instance-2')

    write_conf(os.path.join(project.path, DEFAULT_CFG), {
        ID1: {},
        ID2: {},
    })

    # start instances
    cli.start(project, daemonized=True, stateboard=True)
    check_instances_running(cli, project, [ID1, ID2], daemonized=True, stateboard=True)

    # stop instances
    cli.stop(project, stateboard=True)
    check_instances_stopped(cli, project, [ID1, ID2], stateboard=True)


def test_start_stop_from_conf_stateboard_only(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    ID2 = get_instance_id(project.name, 'instance-2')

    write_conf(os.path.join(project.path, DEFAULT_CFG), {
        ID1: {},
        ID2: {},
    })

    # start instances
    cli.start(project, daemonized=True, stateboard_only=True)
    check_instances_running(cli, project, daemonized=True, stateboard_only=True)

    # stop instances
    cli.stop(project, stateboard=True)
    check_instances_stopped(cli, project, stateboard_only=True)


def test_status_by_id(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    # ID2 = get_instance_id(project.name, 'instance-2')
    STATEBOARD_ID = get_stateboard_name(project.name)

    # get status w/o stateboard
    status = cli.get_status(project, [ID1])
    assert len(status) == 1
    assert status.get(ID1) == STATUS_NOT_STARTED
    # assert status.get(ID2) == STATUS_NOT_STARTED

    # get status w/ stateboard
    status = cli.get_status(project, [ID1], stateboard=True)
    assert len(status) == 2
    assert status.get(ID1) == STATUS_NOT_STARTED
    assert status.get(STATEBOARD_ID) == STATUS_NOT_STARTED

    # get status stateboard-only
    status = cli.get_status(project, stateboard_only=True)
    assert len(status) == 1
    assert status.get(STATEBOARD_ID) == STATUS_NOT_STARTED

    # start instance-1 and stateboard
    cli.start(project, [ID1], stateboard=True, daemonized=True)
    wait_instances(cli, project, [ID1], stateboard=True)

    # get status w/o stateboard
    status = cli.get_status(project, [ID1])
    assert len(status) == 1
    assert status.get(ID1) == STATUS_RUNNING

    # get status w/ stateboard
    status = cli.get_status(project, [ID1], stateboard=True)
    assert len(status) == 2
    assert status.get(ID1) == STATUS_RUNNING
    assert status.get(STATEBOARD_ID) == STATUS_RUNNING

    # get status stateboard-only
    status = cli.get_status(project, stateboard_only=True)
    assert len(status) == 1
    assert status.get(STATEBOARD_ID) == STATUS_RUNNING

    # stop instance-1
    cli.stop(project, [ID1])

    # get status w/o stateboard
    status = cli.get_status(project, [ID1])
    assert len(status) == 1
    assert status.get(ID1) == STATUS_STOPPED

    # get status w/ stateboard
    status = cli.get_status(project, [ID1], stateboard=True)
    assert len(status) == 2
    assert status.get(ID1) == STATUS_STOPPED
    assert status.get(STATEBOARD_ID) == STATUS_RUNNING

    # get status stateboard-only
    status = cli.get_status(project, stateboard_only=True)
    assert len(status) == 1
    assert status.get(STATEBOARD_ID) == STATUS_RUNNING


def test_status_from_conf(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    ID2 = get_instance_id(project.name, 'instance-2')
    STATEBOARD_ID = get_stateboard_name(project.name)

    write_conf(os.path.join(project.path, DEFAULT_CFG), {
        ID1: {},
        ID2: {},
    })

    # get status w/o stateboard
    status = cli.get_status(project)
    assert len(status) == 2
    assert status.get(ID1) == STATUS_NOT_STARTED
    assert status.get(ID2) == STATUS_NOT_STARTED

    # get status w/ stateboard
    status = cli.get_status(project, stateboard=True)
    assert len(status) == 3
    assert status.get(ID1) == STATUS_NOT_STARTED
    assert status.get(ID2) == STATUS_NOT_STARTED
    assert status.get(STATEBOARD_ID) == STATUS_NOT_STARTED

    # get status stateboard-only
    status = cli.get_status(project, stateboard_only=True)
    assert len(status) == 1
    assert status.get(STATEBOARD_ID) == STATUS_NOT_STARTED

    # start instance-1 and stateboard
    cli.start(project, [ID1], stateboard=True, daemonized=True)
    wait_instances(cli, project, [ID1], stateboard=True)

    # get status w/o stateboard
    status = cli.get_status(project)
    assert len(status) == 2
    assert status.get(ID1) == STATUS_RUNNING
    assert status.get(ID2) == STATUS_NOT_STARTED

    # get status w/ stateboard
    status = cli.get_status(project, stateboard=True)
    assert len(status) == 3
    assert status.get(ID1) == STATUS_RUNNING
    assert status.get(ID2) == STATUS_NOT_STARTED
    assert status.get(STATEBOARD_ID) == STATUS_RUNNING

    # get status stateboard-only
    status = cli.get_status(project, stateboard_only=True)
    assert len(status) == 1
    assert status.get(STATEBOARD_ID) == STATUS_RUNNING

    # stop instance-1
    cli.stop(project, [ID1])

    # get status w/o stateboard
    status = cli.get_status(project)
    assert len(status) == 2
    assert status.get(ID1) == STATUS_STOPPED
    assert status.get(ID2) == STATUS_NOT_STARTED

    # get status w/ stateboard
    status = cli.get_status(project, stateboard=True)
    assert len(status) == 3
    assert status.get(ID1) == STATUS_STOPPED
    assert status.get(ID2) == STATUS_NOT_STARTED
    assert status.get(STATEBOARD_ID) == STATUS_RUNNING

    # get status stateboard-only
    status = cli.get_status(project, stateboard_only=True)
    assert len(status) == 1
    assert status.get(STATEBOARD_ID) == STATUS_RUNNING


def test_start_interactive_cfg(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    ID2 = get_instance_id(project.name, 'instance-2')
    CFG = 'my-conf.yml'

    write_conf(os.path.join(project.path, CFG), {
        ID1: {},
        ID2: {},
    })

    cli.start(project, stateboard=True, cfg=CFG)
    check_instances_running(
        cli, project,
        [ID1, ID2],
        stateboard=True, cfg=CFG
    )


def test_start_stop_status_cfg(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    ID2 = get_instance_id(project.name, 'instance-2')
    CFG = 'my-conf.yml'

    write_conf(os.path.join(project.path, CFG), {
        ID1: {},
        ID2: {},
    })

    status = cli.get_status(project, cfg=CFG)
    assert status.get(ID1) == STATUS_NOT_STARTED
    assert status.get(ID2) == STATUS_NOT_STARTED

    cli.start(project, stateboard=True, daemonized=True, cfg=CFG)
    check_instances_running(
        cli, project,
        [ID1, ID2],
        stateboard=True, cfg=CFG,
        daemonized=True,
    )

    status = cli.get_status(project, cfg=CFG)
    assert status.get(ID1) == STATUS_RUNNING
    assert status.get(ID2) == STATUS_RUNNING

    cli.stop(project, stateboard=True, cfg=CFG)
    check_instances_stopped(cli, project, [ID1, ID2])

    status = cli.get_status(project, cfg=CFG)
    assert status.get(ID1) == STATUS_STOPPED
    assert status.get(ID2) == STATUS_STOPPED


def test_start_interactive_run_dir(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    # ID2 = get_instance_id(project.name, 'instance-2')
    RUN_DIR = 'my-run'

    cli.start(project, [ID1], stateboard=True, run_dir=RUN_DIR)
    check_instances_running(
        cli, project,
        [ID1],
        stateboard=True, run_dir=RUN_DIR
    )


def test_start_stop_status_run_dir(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    # ID2 = get_instance_id(project.name, 'instance-2')
    RUN_DIR = 'my-run'

    status = cli.get_status(project, [ID1], run_dir=RUN_DIR)
    assert status.get(ID1) == STATUS_NOT_STARTED
    # assert status.get(ID2) == STATUS_NOT_STARTED

    cli.start(project, [ID1], stateboard=True, daemonized=True, run_dir=RUN_DIR)
    check_instances_running(
        cli, project,
        [ID1],
        stateboard=True, run_dir=RUN_DIR,
        daemonized=True
    )

    status = cli.get_status(project, [ID1], run_dir=RUN_DIR)
    assert status.get(ID1) == STATUS_RUNNING
    # assert status.get(ID2) == STATUS_RUNNING

    cli.stop(project, [ID1], stateboard=True, run_dir=RUN_DIR)
    check_instances_stopped(cli, project, [ID1], run_dir=RUN_DIR)

    status = cli.get_status(project, [ID1], run_dir=RUN_DIR)
    assert status.get(ID1) == STATUS_STOPPED
    # assert status.get(ID2) == STATUS_STOPPED


# def test_start_interactive_data_dir(cartridge_cmd, project_with_patched_init):
#     project = project_with_patched_init
#     cli = Cli(cartridge_cmd)

#     ID1 = get_instance_id(project.name, 'instance-1')
#     ID2 = get_instance_id(project.name, 'instance-2')
#     DATA_DIR = 'my-data'

#     cli.start(project, [ID1, ID2], stateboard=True, data_dir=DATA_DIR)
#     check_instances_running(
#         cli, project,
#         [ID1, ID2],
#         stateboard=True, data_dir=DATA_DIR
#     )


def test_start_script(cartridge_cmd, project_with_patched_init):
    project = project_with_patched_init
    cli = Cli(cartridge_cmd)

    ID1 = get_instance_id(project.name, 'instance-1')
    # ID2 = get_instance_id(project.name, 'instance-2')

    SCRIPT = 'my-init.lua'
    shutil.copyfile(os.path.join(project.path, DEFAULT_SCRIPT), os.path.join(project.path, SCRIPT))

    cli.start(project, [ID1], stateboard=True, script=SCRIPT)
    check_instances_running(
        cli, project,
        [ID1],
        stateboard=True, script=SCRIPT
    )
