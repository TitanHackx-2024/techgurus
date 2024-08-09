# Use an official Node runtime as a parent image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package.json package-lock.json /app/

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . /app/

# Build the application
RUN npm run build

# Expose the port the app runs on
EXPOSE 3000

# Start the application from the /app directory
CMD ["sh", "-c", "cd /app && npm start"]
