FROM python:3.8-slim

ARG UID=1000
ARG GID=1000
ENV USER=appuser
ENV WORKDIR=/opt/appuser
ENV HOST="0.0.0.0"
ENV PORT="8000"

RUN mkdir $WORKDIR \
  && apt update \
  && pip install --upgrade pip \
  && groupadd -g $GID $USER \
  && useradd -g $GID -u $UID -d $WORKDIR -s /bin/bash $USER

ADD requirements.txt $WORKDIR/requirements.txt
RUN pip3 install -r $WORKDIR/requirements.txt

ADD . $WORKDIR
USER appuser
WORKDIR $WORKDIR
CMD ["/bin/bash", "run.sh"]
