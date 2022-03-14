ARG TASK_BRANCH
ARG TIMEW_BRANCH

FROM ghcr.io/lauft/task-timew:${TASK_BRANCH}-${TIMEW_BRANCH}

ARG TASK_BRANCH
ARG TIMEW_BRANCH

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && yes | unminimize
RUN apt-get install -y python3 python3-venv
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

RUN echo "Testing on task-${TASK_BRANCH}/timew-${TIMEW_BRANCH}"

# Copy on-modify-hook
ADD .. /task-on-modify-hook
WORKDIR /task-on-modify-hook

# Install on-modify-hook
RUN mkdir -p ~/.task/hooks
RUN cp on_modify.py ~/.task/hooks/on-modify.timewarrior
RUN chmod +x ~/.task/hooks/on-modify.timewarrior

# Run tests
WORKDIR /
RUN python -m venv venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install pytest simpletap
RUN ( \
    python --version ; \
    task diagnostics ; \
    timew diagnostics ; \
    /venv/bin/pip freeze ; \
    ) > diagnostics.txt 2>&1

ENV TASK_USE_PATH=true TIMEW_USE_PATH=true
CMD [ "bash", "-c", "/venv/bin/pytest /task-on-modify-hook/test/test_on-modify_e2e.py"]
