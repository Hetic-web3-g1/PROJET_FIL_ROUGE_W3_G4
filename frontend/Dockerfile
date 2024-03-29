FROM node:18-alpine AS development

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project to the container
COPY . .

# Set environment variables
ENV NODE_ENV=development
ENV FRONTEND_PORT=3000

# Start the development server
CMD ["npm", "run", "dev"]

# # ------------------------------------------------------------------------

FROM node:18 AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project to the container
COPY . .

# Set environment variables
ENV FRONTEND_PORT=80

# Build the React app
RUN npm run build

# # ------------------------------------------------------------------------

# Use Nginx to serve the built app
FROM nginx:latest as production

# Copy the built app from the builder stage to the nginx server
COPY --from=builder /app/dist /usr/share/nginx/html

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]

# # ------------------------------------------------------------------------
# Dummy stage for testing
FROM alpine:3 AS test