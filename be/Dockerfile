FROM node:lts

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

# Build TypeScript
RUN npm run build

EXPOSE 3000

# Run production build
CMD ["npm", "start"]
