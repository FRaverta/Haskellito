FROM python:3.12-slim

WORKDIR /var/task

ENV HOME=/tmp \
    TMPDIR=/tmp \
    XDG_CACHE_HOME=/tmp/.cache

RUN apt-get update \
    && apt-get install -y --no-install-recommends ghc ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /tmp/backend-requirements.txt
COPY serverless/lambdas/playground/requirements.txt /tmp/lambda-requirements.txt

RUN pip install --no-cache-dir \
    -r /tmp/backend-requirements.txt \
    -r /tmp/lambda-requirements.txt

COPY backend ./backend
COPY serverless ./serverless
RUN cp backend/ghci/config.hs ./ghci.ghci

ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"]
CMD ["serverless.lambdas.playground.handler.handler"]
