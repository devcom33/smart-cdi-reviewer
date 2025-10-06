FROM node:22.17.1-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
#build command to create a production-ready app
RUN npm run build
RUN npm install -g serve
EXPOSE 5173
CMD ["serve", "-s", "dist", "-l", "5173"]
