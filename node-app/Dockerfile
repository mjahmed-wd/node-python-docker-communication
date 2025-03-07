FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

# Install all dependencies including devDependencies
RUN npm install

COPY . .

EXPOSE 3000

# CMD is now specified in docker-compose.yml
CMD ["npm", "run", "dev"] 