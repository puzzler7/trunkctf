FROM redpwn/jail

COPY --from=ubuntu / /srv
COPY ./babyrop /srv/app/babyrop
COPY ./wrapper.sh /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run
RUN chmod 744 /srv/app/flag.txt

ENV JAIL_TIME 60
ENV JAIL_MEM 20M
ENV JAIL_PORT 10003