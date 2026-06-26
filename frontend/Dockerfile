# ============================================================
#  Zarix AgentOS — Frontend Dockerfile
# ============================================================
FROM node:20-alpine

WORKDIR /app

# Dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Application code
COPY . .

# Expose port
EXPOSE 3000

# Development server
CMD ["npm", "run", "dev"]
