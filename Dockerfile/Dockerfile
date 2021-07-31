#Latest image always
FROM alpine:latest

RUN apk update \
  && apk upgrade \
  && apk add --no-cache \
             rsync \
             p7zip \
             openssh \
             ca-certificates \
 && update-ca-certificates \
 && rm -rf /var/cache/apk/*




