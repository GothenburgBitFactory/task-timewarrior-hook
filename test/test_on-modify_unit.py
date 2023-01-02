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
import json
import subprocess
from unittest.mock import call

import on_modify


def test_hook_should_process_annotate(mocker):
    """on-modify hook should process 'task annotate'"""

    mocker.patch('subprocess.call')
    on_modify.main(
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T201911Z",
            "modified": "20190820T201911Z",
            "start": "20190820T201911Z",
            "status": "pending",
            "uuid": "3495a755-c4c6-4106-aabe-c0d3d128b65a"
            }'''),
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T201911Z",
            "modified": "20190820T201911Z",
            "start": "20190820T201911Z",
            "status": "pending",
            "uuid": "3495a755-c4c6-4106-aabe-c0d3d128b65a",
            "annotations":[{"entry": "20190820T201911Z", "description": "Annotation"}]
            }''')
    )

    subprocess.call.assert_called_once_with(['timew', 'annotate', '@1', 'Annotation'])


def test_hook_should_process_append(mocker):
    """on-modify hook should process 'task append'"""

    mocker.patch('subprocess.call')
    on_modify.main(
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T201911Z",
            "modified": "20190820T201911Z",
            "start": "20190820T201911Z",
            "status": "pending",
            "uuid": "da603270-ce2b-4a5a-9273-c67c2d2d0067"
            }'''),
        json.loads(
            '''{
            "description": "Foo Bar",
            "entry": "20190820T201911Z",
            "modified": "20190820T201911Z",
            "start": "20190820T201911Z",
            "status": "pending",
            "uuid": "da603270-ce2b-4a5a-9273-c67c2d2d0067"
            }''')
    )

    subprocess.call.assert_has_calls([
        call(['timew', 'untag', '@1', 'Foo', ':yes']),
        call(['timew', 'tag', '@1', 'Foo Bar', ':yes'])
    ])


def test_hook_should_process_delete(mocker):
    """on-modify hook should process 'task delete'"""

    mocker.patch('subprocess.call')
    on_modify.main(
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T201911Z",
            "modified": "20190820T201911Z",
            "start": "20190820T201911Z",
            "status": "pending",
            "uuid": "25b66283-96e0-42b4-b835-8efd0ea1043c"
            }'''),
        json.loads(
            '''{
            "description": "Foo",
            "end": "20190820T201911Z",
            "entry": "20190820T201911Z",
            "modified": "20190820T201911Z",
            "start": "20190820T201911Z",
            "status": "deleted",
            "uuid": "25b66283-96e0-42b4-b835-8efd0ea1043c"
            }''')
    )

    subprocess.call.assert_called_once_with(['timew', 'stop', 'Foo', ':yes'])


def test_hook_should_process_denotate(mocker):
    """on-modify hook should process 'task denotate'"""

    mocker.patch('subprocess.call')
    on_modify.main(
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T201911Z",
            "modified": "20190820T201911Z",
            "start": "20190820T201911Z",
            "status": "pending",
            "uuid": "8811cc93-a495-4fa6-993e-2b96cffc48e0",
            "annotations": [{"entry": "20190820T201911Z", "description": "Annotation"}]
            }'''),
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T201911Z",
            "modified": "20190820T201911Z",
            "start": "20190820T201911Z",
            "status": "pending",
            "uuid": "8811cc93-a495-4fa6-993e-2b96cffc48e0"
            }''')
    )

    subprocess.call.assert_called_once_with(['timew', 'annotate', '@1', "''"])


def test_hook_should_process_done(mocker):
    """on-modify hook should process 'task done'"""

    mocker.patch('subprocess.call')
    on_modify.main(
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T201912Z",
            "modified": "20190820T201912Z",
            "start": "20190820T201912Z",
            "status": "pending",
            "uuid": "c418b958-5c3c-4633-89a4-4a2f678d74d0"
            }'''),
        json.loads(
            '''{
            "description": "Foo",
            "end": "20190820T201912Z",
            "entry": "20190820T201912Z",
            "modified": "20190820T201912Z",
            "status": "completed",
            "uuid": "c418b958-5c3c-4633-89a4-4a2f678d74d0"
            }''')
    )

    subprocess.call.assert_called_once_with(['timew', 'stop', 'Foo', ':yes'])


def test_hook_should_process_modify_desc(mocker):
    """on-modify hook should process 'task modify' for changing description"""

    mocker.patch('subprocess.call')
    on_modify.main(
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T203416Z",
            "modified": "20190820T203416Z",
            "start": "20190820T203416Z",
            "status": "pending",
            "uuid": "189e6745-04e0-4b17-949f-900cf63ab8d9"
            }'''),
        json.loads(
            '''{
            "description": "Bar",
            "entry": "20190820T203416Z",
            "modified": "20190820T203416Z",
            "start": "20190820T203416Z",
            "status": "pending",
            "uuid": "189e6745-04e0-4b17-949f-900cf63ab8d9"
            }''')
    )

    subprocess.call.assert_has_calls([
        call(["timew", "untag", "@1", "Foo", ":yes"]),
        call(['timew', 'tag', '@1', 'Bar', ':yes'])
    ])


def test_hook_should_process_modify_tags(mocker):
    """on-modify hook should process 'task modify' for changing tags"""

    mocker.patch('subprocess.call')
    on_modify.main(
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T203620Z",
            "modified": "20190820T203620Z",
            "start": "20190820T203620Z",
            "status": "pending",
            "tags":["Tag", "Bar"],
            "uuid": "6cab88f0-ac12-4a87-995a-0e7d39810c05"
            }'''),
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T203620Z",
            "modified": "20190820T203620Z",
            "start": "20190820T203620Z",
            "status": "pending",
            "tags":["Tag", "Baz"],
            "uuid": "6cab88f0-ac12-4a87-995a-0e7d39810c05"
            }''')
    )

    subprocess.call.assert_has_calls([
        call(['timew', 'untag', '@1', 'Foo', 'Tag', 'Bar', ':yes']),
        call(['timew', 'tag', '@1', 'Foo', 'Tag', 'Baz', ':yes'])
    ])


def test_hook_should_process_modify_project(mocker):
    """on-modify hook should process 'task modify' for changing project"""

    mocker.patch('subprocess.call')
    on_modify.main(
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T203842Z",
            "modified": "20190820T203842Z",
            "project": "dummy",
            "start": "20190820T203842Z",
            "status": "pending",
            "uuid": "d95dc7a0-6189-4692-b58a-4ab60d539c8d"
            }'''),
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T203842Z",
            "modified": "20190820T203842Z",
            "project": "test",
            "start": "20190820T203842Z",
            "status": "pending",
            "uuid": "d95dc7a0-6189-4692-b58a-4ab60d539c8d"
            }''')
    )

    subprocess.call.assert_has_calls([
        call(['timew', 'untag', '@1', 'Foo', 'dummy', ':yes']),
        call(['timew', 'tag', '@1', 'Foo', 'test', ':yes'])
    ])


def test_hook_should_process_prepend(mocker):
    """on-modify hook should process 'task prepend'"""

    mocker.patch('subprocess.call')
    on_modify.main(
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T203842Z",
            "modified": "20190820T203842Z",
            "start": "20190820T203842Z",
            "status": "pending",
            "uuid": "02bc8839-b304-49f9-ac1a-29ac4850583f"
            }'''),
        json.loads(
            '''{
            "description": "Prefix Foo",
            "entry": "20190820T203842Z",
            "modified": "20190820T203842Z",
            "start": "20190820T203842Z",
            "status": "pending",
            "uuid": "02bc8839-b304-49f9-ac1a-29ac4850583f"
            }''')
    )

    subprocess.call.assert_has_calls([
        call(['timew', 'untag', '@1', 'Foo', ':yes']),
        call(['timew', 'tag', '@1', 'Prefix Foo', ':yes'])
    ])


def test_hook_should_process_start(mocker):
    """on-modify hook should process 'task start'"""

    mocker.patch('subprocess.call')
    on_modify.main(
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T203842Z",
            "modified": "20190820T203842Z",
            "status": "pending",
            "uuid": "16af44c5-57d2-43bf-97ed-cf2e541d927f"
            }'''),
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T203842Z",
            "modified": "20190820T203842Z",
            "start": "20190820T203842Z",
            "status": "pending",
            "uuid": "16af44c5-57d2-43bf-97ed-cf2e541d927f"
            }''')
    )

    subprocess.call.assert_called_once_with(['timew', 'start', 'Foo', ':yes'])


def test_hook_should_process_stop(mocker):
    """on-modify hook should process 'task stop'"""

    mocker.patch('subprocess.call')
    on_modify.main(
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T203842Z",
            "modified": "20190820T203842Z",
            "start": "20190820T203842Z",
            "status": "pending",
            "uuid": "13f83e99-f6a2-4857-9e00-bdeede064772"
            }'''),
        json.loads(
            '''{
            "description": "Foo",
            "entry": "20190820T203842Z",
            "modified": "20190820T203842Z",
            "status": "pending",
            "uuid": "13f83e99-f6a2-4857-9e00-bdeede064772"
            }''')
    )

    subprocess.call.assert_called_once_with(['timew', 'stop', 'Foo', ':yes'])
