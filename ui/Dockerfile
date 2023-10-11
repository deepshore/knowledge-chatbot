FROM nginx:latest

# Copy the build output to replace the default nginx contents.
COPY dist /usr/share/nginx/html

COPY /webserver/nginx.conf  /etc/nginx/conf.d/default.conf

EXPOSE 80
