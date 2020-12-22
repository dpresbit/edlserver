FROM alpine

RUN apk update \
    && apk add lighttpd \
    && rm -rf /var/cache/apk/*

CMD ["lighttpd","-D","-f","/etc/lighttpd/lighttpd.conf"]
