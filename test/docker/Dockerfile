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

ARG TEST_IMAGE

FROM ${TEST_IMAGE}

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && yes | unminimize
RUN apt-get install -y python3 python3-venv
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

# Create virtual environment
WORKDIR /
RUN python -m venv venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install pytest simpletap

# Store diagnostics
RUN ( \
    python --version ; \
    task diagnostics ; \
    timew diagnostics ; \
    /venv/bin/pip freeze ; \
    ) > diagnostics.txt 2>&1

# Copy on-modify-hook
ADD . /task-on-modify-hook
WORKDIR /task-on-modify-hook

# Install on-modify-hook
RUN mkdir -p ~/.task/hooks
RUN cp on_modify.py ~/.task/hooks/on-modify.timewarrior
RUN chmod +x ~/.task/hooks/on-modify.timewarrior

RUN echo "timew: $( timew --version )" ; \
    echo "task: $( task --version )"

# Run tests
ENV TASK_USE_PATH=true TIMEW_USE_PATH=true
CMD [ "bash", "-c", "/venv/bin/pytest /task-on-modify-hook/test/test_on-modify_e2e.py"]
