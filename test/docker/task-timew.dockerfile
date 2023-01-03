ARG TASK_IMAGE
ARG TIMEW_IMAGE

FROM ${TIMEW_IMAGE} AS timew

FROM ${TASK_IMAGE} AS task

# Install Timewarrior
COPY --from=timew /usr/local/bin/timew /usr/local/bin

# Initialize Timewarrior
WORKDIR /root/
RUN timew :yes
