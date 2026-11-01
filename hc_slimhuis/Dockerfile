ARG BUILD_FROM=ghcr.io/home-assistant/base:latest
FROM $BUILD_FROM
RUN apk add --no-cache python3
COPY agent.py run.sh /
RUN chmod a+x /run.sh
CMD ["/run.sh"]
