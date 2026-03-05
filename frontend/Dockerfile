FROM nginx:alpine

COPY index.html style.css script.js /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

USER nginx

EXPOSE 80
