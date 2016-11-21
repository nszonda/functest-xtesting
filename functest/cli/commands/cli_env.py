#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import os

import click
import git

import functest.utils.functest_utils as ft_utils
import functest.utils.functest_constants as ft_constants


class CliEnv:

    def __init__(self):
        pass

    def prepare(self):
        if self.status(verbose=False) == 0:
            answer = raw_input("It seems that the environment has been "
                               "already prepared. Do you want to do "
                               "it again? [y|n]\n")
            while True:
                if answer.lower() in ["y", "yes"]:
                    os.remove(ft_constants.ENV_FILE)
                    break
                elif answer.lower() in ["n", "no"]:
                    return
                else:
                    answer = raw_input("Invalid answer. Please type [y|n]\n")

        cmd = ("python %s/functest/ci/prepare_env.py start" %
               ft_constants.FUNCTEST_REPO_DIR)
        ft_utils.execute_command(cmd)

    def show(self):
        CI_INSTALLER_TYPE = ft_constants.CI_INSTALLER_TYPE
        if CI_INSTALLER_TYPE is None:
            CI_INSTALLER_TYPE = "Unknown"
        CI_INSTALLER_IP = ft_constants.CI_INSTALLER_IP
        if CI_INSTALLER_IP is None:
            CI_INSTALLER_IP = "Unknown"
        CI_INSTALLER = ("%s, %s" % (CI_INSTALLER_TYPE, CI_INSTALLER_IP))

        CI_SCENARIO = ft_constants.CI_SCENARIO
        if CI_SCENARIO is None:
            CI_SCENARIO = "Unknown"

        CI_NODE = ft_constants.CI_NODE
        if CI_NODE is None:
            CI_NODE = "Unknown"

        repo = git.Repo(ft_constants.FUNCTEST_REPO_DIR)
        branch = repo.head.reference
        GIT_BRANCH = branch.name
        GIT_HASH = branch.commit.hexsha

        CI_BUILD_TAG = ft_constants.CI_BUILD_TAG
        if CI_BUILD_TAG is not None:
            CI_BUILD_TAG = CI_BUILD_TAG.lstrip(
                "jenkins-").lstrip("functest").lstrip("-")

        CI_DEBUG = ft_constants.CI_DEBUG
        if CI_DEBUG is None:
            CI_DEBUG = "false"

        STATUS = "not ready"
        if self.status(verbose=False) == 0:
            STATUS = "ready"

        click.echo("+======================================================+")
        click.echo("| Functest Environment info                            |")
        click.echo("+======================================================+")
        click.echo("|  INSTALLER: %s|" % CI_INSTALLER.ljust(41))
        click.echo("|   SCENARIO: %s|" % CI_SCENARIO.ljust(41))
        click.echo("|        POD: %s|" % CI_NODE.ljust(41))
        click.echo("| GIT BRACNH: %s|" % GIT_BRANCH.ljust(41))
        click.echo("|   GIT HASH: %s|" % GIT_HASH.ljust(41))
        if CI_BUILD_TAG:
            click.echo("|  BUILD TAG: %s|" % CI_BUILD_TAG.ljust(41))
        click.echo("| DEBUG FLAG: %s|" % CI_DEBUG.ljust(41))
        click.echo("+------------------------------------------------------+")
        click.echo("|     STATUS: %s|" % STATUS.ljust(41))
        click.echo("+------------------------------------------------------+")
        click.echo("")

    def status(self, verbose=True):
        ret_val = 0
        if not os.path.isfile(ft_constants.ENV_FILE):
            if verbose:
                click.echo("Functest environment is not installed.\n")
            ret_val = 1
        elif verbose:
            click.echo("Functest environment ready to run tests.\n")

        return ret_val
