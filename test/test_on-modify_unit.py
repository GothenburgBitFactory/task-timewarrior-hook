#!/usr/bin/env python3

###############################################################################
#
# Copyright 2023, Gothenburg Bit Factory
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

import pytest
from mockito import unstub, verify, when

import on_modify


@pytest.fixture
def teardown():
    yield
    unstub()


@pytest.mark.usefixtures("teardown")
def test_hook_should_process_annotate():
    """on-modify hook should process 'task annotate'"""

    when(subprocess).call(...)
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

    verify(subprocess).call(['timew', 'annotate', '@1', 'Annotation'])


@pytest.mark.usefixtures("teardown")
def test_hook_should_process_append():
    """on-modify hook should process 'task append'"""

    when(subprocess).call(...)
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

    verify(subprocess).call(['timew', 'untag', '@1', 'Foo', ':yes'])
    verify(subprocess).call(['timew', 'tag', '@1', 'Foo Bar', ':yes'])


@pytest.mark.usefixtures("teardown")
def test_hook_should_process_delete():
    """on-modify hook should process 'task delete'"""

    when(subprocess).call(...)
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

    verify(subprocess).call(['timew', 'stop', 'Foo', ':yes'])


@pytest.mark.usefixtures("teardown")
def test_hook_should_process_denotate():
    """on-modify hook should process 'task denotate'"""

    when(subprocess).call(...)
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

    verify(subprocess).call(['timew', 'annotate', '@1', "''"])


@pytest.mark.usefixtures("teardown")
def test_hook_should_process_done():
    """on-modify hook should process 'task done'"""

    when(subprocess).call(...)
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

    verify(subprocess).call(['timew', 'stop', 'Foo', ':yes'])


@pytest.mark.usefixtures("teardown")
def test_hook_should_process_modify_desc():
    """on-modify hook should process 'task modify' for changing description"""

    when(subprocess).call(...)
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

    verify(subprocess).call(["timew", "untag", "@1", "Foo", ":yes"])
    verify(subprocess).call(['timew', 'tag', '@1', 'Bar', ':yes'])


@pytest.mark.usefixtures("teardown")
def test_hook_should_process_modify_tags():
    """on-modify hook should process 'task modify' for changing tags"""

    when(subprocess).call(...)
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

    verify(subprocess).call(['timew', 'untag', '@1', 'Foo', 'Tag', 'Bar', ':yes'])
    verify(subprocess).call(['timew', 'tag', '@1', 'Foo', 'Tag', 'Baz', ':yes'])


@pytest.mark.usefixtures("teardown")
def test_hook_should_process_modify_project():
    """on-modify hook should process 'task modify' for changing project"""

    when(subprocess).call(...)
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

    verify(subprocess).call(['timew', 'untag', '@1', 'Foo', 'dummy', ':yes'])
    verify(subprocess).call(['timew', 'tag', '@1', 'Foo', 'test', ':yes'])


@pytest.mark.usefixtures("teardown")
def test_hook_should_process_prepend():
    """on-modify hook should process 'task prepend'"""

    when(subprocess).call(...)
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

    verify(subprocess).call(['timew', 'untag', '@1', 'Foo', ':yes'])
    verify(subprocess).call(['timew', 'tag', '@1', 'Prefix Foo', ':yes'])


@pytest.mark.usefixtures("teardown")
def test_hook_should_process_start():
    """on-modify hook should process 'task start'"""

    when(subprocess).call(...)
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

    verify(subprocess).call(['timew', 'start', 'Foo', ':yes'])


@pytest.mark.usefixtures("teardown")
def test_hook_should_process_stop():
    """on-modify hook should process 'task stop'"""

    when(subprocess).call(...)
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

    verify(subprocess).call(['timew', 'stop', 'Foo', ':yes'])
