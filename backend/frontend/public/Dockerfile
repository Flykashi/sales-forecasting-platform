# Use Node base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of code
COPY . .

# Build app
RUN npm run build

# Install serve to run build
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Run app
CMD ["serve", "-s", "build"]