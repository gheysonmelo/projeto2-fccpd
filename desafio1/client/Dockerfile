FROM alpine:3.18

RUN apk add --no-cache curl bash

WORKDIR /app

COPY curl-loop.sh .

RUN chmod +x curl-loop.sh

CMD ["./curl-loop.sh"]
