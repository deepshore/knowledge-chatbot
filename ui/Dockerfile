FROM nginx:1.25

LABEL org.opencontainers.image.source = "https://github.com/deepshore/knowledge-chatbot"

# Copy the build output to replace the default nginx contents.
COPY dist /usr/share/nginx/html

COPY /webserver/nginx.conf  /etc/nginx/conf.d/default.conf

EXPOSE 80
