#Latest image always
FROM alpine:latest

RUN apk update \
  && apk upgrade \
  && apk add --no-cache \
             rsync \
             xz \
 && rm -rf /var/cache/apk/*




