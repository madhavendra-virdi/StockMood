# Stage 1: Build the Vue app
FROM node:18 as builder

WORKDIR /app
COPY . .

RUN npm install
RUN npm run build

# Stage 2: Serve it with NGINX
FROM nginx:alpine

# Remove default NGINX page
RUN rm -rf /usr/share/nginx/html/*

# Copy built files from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Optional: use your own NGINX config
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
