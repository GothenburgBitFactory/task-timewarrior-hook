#!/usr/bin/env python3

###############################################################################
#
# Copyright 2016 - 2021, 2023, Gothenburg Bit Factory
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
import sys

# Hook should extract all the following for use as Timewarrior tags:
#   UUID
#   Project
#   Tags
#   Description
#   UDAs

try:
    input_stream = sys.stdin.buffer
except AttributeError:
    input_stream = sys.stdin


# Extract attributes for use as tags.
def extract_tags(json_obj):
    tags = []
    if 'description' in json_obj:
        tags.append(json_obj['description'])
    if 'project' in json_obj:
        tags.append(json_obj['project'])
    if 'tags' in json_obj:
        tags.extend(json_obj['tags'])
    return tags


def extract_annotation(json_obj):
    if 'annotations' not in json_obj:
        return '\'\''
    return json_obj['annotations'][0]['description']


def extract_start(json_obj):
    return json_obj['start']


# Check that Timewarrior's interval has the given tags
# Returns 0 if they don't match, 1 if they match and 2 if there is no active tracking
def active_interval_has(tags):
    out = subprocess.run(['timew', 'get', 'dom.active.tag.count'], capture_output=True, text=True).stdout
    if not out:
        return 2
    active_tag_count = int(out)
    match = True
    if len(tags) != active_tag_count:
        return 0
    for i in range(1, active_tag_count+1):
        if subprocess.run(['timew', 'get', 'dom.active.tag.' + str(i)], capture_output=True, text=True).stdout[:-1] not in tags:
            return 0
    return 1


def main(old, new):
    new_tags = extract_tags(new)
    old_tags = extract_tags(old)
    check = active_interval_has(old_tags)
    # Running
    if 'start' in new:
        start = extract_start(new)

        if not check:
            sys.exit(0)

        # Started task.
        if 'start' not in old or check == 2:
            subprocess.call(['timew', 'start', start] + new_tags + [':yes'])

        # Task modified
        else:
            if old_tags != new_tags:
                subprocess.call(['timew', 'untag', '@1'] + old_tags + [':yes'])
                subprocess.call(['timew', 'tag', '@1'] + new_tags + [':yes'])

            if start != extract_start(old):
                print('Updating Timewarrior start time to ' + start)
                subprocess.call(['timew', 'modify', 'start', '@1', start])

            old_annotation = extract_annotation(old)
            new_annotation = extract_annotation(new)
            if old_annotation != new_annotation:
                subprocess.call(['timew', 'annotate', '@1', new_annotation])

    # Stopped task.
    elif 'start' in old:
        if check == 1:
            subprocess.call(['timew', 'stop'] + new_tags + [':yes'])


if __name__ == "__main__":
    # Hook is called with two lines input ('old', 'new') in case of an on-modify event,
    # but only with one line ('new') in case of an on-add event.
    # We want to call the hook with an emtpy 'old' ('{}') in the latter case.
    # Prepending '{}' makes sure this happens if only one line is added...
    lines = ['{}'] + [line.decode("utf-8", errors="replace") for line in input_stream.readlines()]

    new = json.loads(lines.pop())
    old = json.loads(lines.pop())

    print(json.dumps(new))
    main(old, new)
