#!/usr/bin/env python3

###############################################################################
#
# Copyright 2019, Thomas Lauf, Paul Beckingham, Federico Hernandez.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# https://www.opensource.org/licenses/mit-license.php
#
###############################################################################

import os.path

from basetest import Timew, Task, TestCase


class TestOnModifyHookScript(TestCase):

    def setUp(self):
        if os.path.exists("/root/.local/share/timewarrior"):
            datadir = "/root/.local/share/timewarrior"
            configdir = "/root/.config/timewarrior"
        else:
            datadir = "/root/.timewarrior"
            configdir = "/root/.timewarrior"

        self.timew = Timew(datadir=datadir, configdir=configdir)
        self.timew.reset(keep_config=True)

        self.task = Task(datadir="/root/.task", taskrc="/root/.taskrc")
        self.task.reset(keep_config=True, keep_hooks=True)

    def test_hook_should_process_annotate(self):
        """on-modify hook should process 'task annotate'"""
        self.task.deactivate_hooks()
        self.task("add Foo")
        self.task("start 1")
        self.timew("start 10min ago Foo")
        self.task.activate_hooks()

        self.task("1 annotate Annotation")

        j = self.timew.export()
        self.assertEqual(len(j), 1)
        self.assertOpenInterval(j[0], expectedTags=["Foo"], expectedAnnotation="Annotation")

    def test_hook_should_process_append(self):
        """on-modify hook should process 'task append'"""
        self.task.deactivate_hooks()
        self.task("add Foo")
        self.task("1 start")
        self.timew("start 10min ago Foo")
        self.task.activate_hooks()

        self.task("1 append Bar")

        j = self.timew.export()
        self.assertEqual(len(j), 1)
        self.assertOpenInterval(j[0], expectedTags=["Foo Bar"])

    def test_hook_should_process_delete(self):
        """on-modify hook should process 'task delete'"""
        self.task.deactivate_hooks()
        self.task("add Foo")
        self.task("start 1")
        self.timew("start 10min ago Foo")
        self.task.activate_hooks()

        self.task("rc.confirmation=off delete 1")

        j = self.timew.export()
        self.assertEqual(len(j), 1)
        self.assertClosedInterval(j[0], expectedTags=["Foo"])

    def test_hook_should_process_denotate(self):
        """on-modify hook should process 'task denotate'"""
        self.task.deactivate_hooks()
        self.task("add Foo")
        self.task("1 start")
        self.task("1 annotate Annotation")
        self.timew("start 10min ago Foo")
        self.timew("annotate @1 Annotation")
        self.task.activate_hooks()

        self.task("1 denotate")

        j = self.timew.export()
        self.assertEqual(len(j), 1)
        self.assertOpenInterval(j[0], expectedTags=["Foo"], expectedAnnotation="")

    def test_hook_should_process_done(self):
        """on-modify hook should process 'task done'"""
        self.task.deactivate_hooks()
        self.task("add Foo")
        self.task("1 start")
        self.timew("start 10min ago Foo")
        self.task.activate_hooks()

        self.task("1 done")

        j = self.timew.export()
        self.assertEqual(len(j), 1)
        self.assertClosedInterval(j[0], expectedTags=["Foo"])

    def test_hook_should_process_modify_description(self):
        """on-modify hook should process 'task modify' for changing description"""
        self.task.deactivate_hooks()
        self.task("add Foo")
        self.task("1 start")
        self.timew("start 10min ago Foo")
        self.task.activate_hooks()

        self.task("1 modify /Foo/Bar/")

        j = self.timew.export()
        self.assertEqual(len(j), 1)
        self.assertOpenInterval(j[0], expectedTags=["Bar"])

    def test_hook_should_process_modify_tags(self):
        """on-modify hook should process 'task modify' for changing tags"""
        self.task.deactivate_hooks()
        self.task("add Foo")
        self.task("1 start")
        self.task("1 modify +Bar +Tag")
        self.timew("start 10min ago Foo Tag Bar")
        self.task.activate_hooks()

        self.task("1 modify -Bar +Baz")

        j = self.timew.export()
        self.assertEqual(len(j), 1)
        self.assertOpenInterval(j[0], expectedTags=["Foo", "Tag", "Baz"])

    def test_hook_should_process_modify_project(self):
        """on-modify hook should process 'task modify' for changing project"""
        self.task.deactivate_hooks()
        self.task("add Foo project:dummy")
        self.task("1 start")
        self.timew("start 10min ago Foo dummy")
        self.task.activate_hooks()

        self.task("1 modify project:test")

        j = self.timew.export()
        self.assertEqual(len(j), 1)
        self.assertOpenInterval(j[0], expectedTags=["Foo", "test"])

    def test_hook_should_process_prepend(self):
        """on-modify hook should process 'task prepend'"""
        self.task.deactivate_hooks()
        self.task("add Foo")
        self.task("1 start")
        self.timew("start 10min ago Foo")
        self.task.activate_hooks()

        self.task("1 prepend 'Prefix '")

        j = self.timew.export()
        self.assertEqual(len(j), 1)
        self.assertOpenInterval(j[0], expectedTags=["Prefix Foo"])

    def test_hook_should_process_start(self):
        """on-modify hook should process 'task start'"""
        self.task.deactivate_hooks()
        self.task("add Foo")
        self.task.activate_hooks()

        self.task("1 start")

        j = self.timew.export()
        self.assertEqual(len(j), 1)
        self.assertOpenInterval(j[0], expectedTags=["Foo"])

    def test_hook_should_process_stop(self):
        """on-modify hook should process 'task stop'"""
        self.task.deactivate_hooks()
        self.task("add Foo")
        self.task("1 start")
        self.timew("start 10min ago Foo")
        self.task.activate_hooks()

        self.task("1 stop")

        j = self.timew.export()
        self.assertEqual(len(j), 1)
        self.assertClosedInterval(j[0], expectedTags=["Foo"])
