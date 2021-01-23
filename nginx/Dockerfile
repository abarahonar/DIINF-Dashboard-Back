FROM nginx:1.19.0-alpine
RUN mkdir -p /etc/ssl
COPY config /etc/ssl/
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d