# Use the Node.js 16 Alpine image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files first
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --silent

# Copy the rest of the application code
COPY . .

# Expose the port for the frontend
EXPOSE 3000

# Define the command to run the application
CMD ["npm", "start"]
