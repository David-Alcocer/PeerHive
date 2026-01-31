FROM nginx:alpine

# Copy static assets (HTML, CSS, JS) to Nginx root
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY src /usr/share/nginx/html/src/

# Expose port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
