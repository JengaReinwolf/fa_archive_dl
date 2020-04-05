FROM osminogin/tor-simple

USER root

RUN apk add --no-cache python3 py3-pip


# Setup env
RUN mkdir -p "/srv/fa_archive_dl/"
WORKDIR "/srv/fa_archive_dl/"
COPY . .
RUN chown -R tor . && \
    chmod 744 "fa_archive_dl.py" "entrypoint.sh" "env_setup.py"
RUN pip3 install -r "requirements.txt"

USER tor

ENTRYPOINT [ "/srv/fa_archive_dl/entrypoint.sh" ]
