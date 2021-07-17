FROM ubuntu:20.04
ARG TASK_BRANCH
ARG TIMEW_BRANCH

RUN echo "Building image task-${TASK_BRANCH}-timew-${TIMEW_BRANCH}"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && yes | unminimize
RUN apt-get install -y \
            asciidoctor \
            build-essential \
            cmake \
            faketime \
            g++ \
            git \
            libgnutls28-dev \
            locales \
            man \
            man-db \
            python3 \
            python3-dateutil \
            python3-venv \
            tzdata \
            uuid-dev

# Setup environment
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10
RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

# Setup language environment
RUN locale-gen "en_US.UTF-8"
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Install Taskwarrior
WORKDIR /
RUN git clone --recursive -b ${TASK_BRANCH} https://github.com/GothenburgBitFactory/taskwarrior.git
WORKDIR /taskwarrior
RUN cmake -DCMAKE_BUILD_TYPE=debug .
RUN make -j8
RUN make install

# Install Timewarrior
WORKDIR /
RUN git clone --recursive -b ${TIMEW_BRANCH} https://github.com/GothenburgBitFactory/timewarrior.git
WORKDIR /timewarrior
RUN cmake -DCMAKE_BUILD_TYPE=debug .
RUN make -j8
RUN make install

# Copy on-modify-hook
ADD . /task-on-modify-hook
WORKDIR /task-on-modify-hook
#RUN git clean -dfx

# Install on-modify-hook
RUN mkdir -p ~/.task/hooks && echo > ~/.taskrc
RUN mkdir -p ~/.timewarrior/

RUN cp on-modify.py ~/.task/hooks/on-modify.timewarrior
RUN chmod +x ~/.task/hooks/on-modify.timewarrior

# Run tests
WORKDIR /
RUN python -m venv venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install pytest simpletap
RUN ( \
    task diagnostics ; \
    timew diagnostics ; \
    /venv/bin/pip freeze ; \
    ) > diagnostics.txt 2>&1

ENV TASK_USE_PATH=true TIMEW_USE_PATH=true
CMD [ "bash", "-c", "/venv/bin/pytest /task-on-modify-hook/test/test_on-modify_e2e.py"]



