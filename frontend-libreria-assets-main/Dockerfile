# Frontend Dockerfile
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
COPY . .
RUN npm install
RUN npm run build

# Serve with Vite preview
EXPOSE 4173
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]