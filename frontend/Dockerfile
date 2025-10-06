FROM node:22.17.1-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN apk add --no-cache dos2unix && \
  find . -type f -exec dos2unix {} \; 2>/dev/null || true && \
  apk del dos2unix

RUN npm run build

RUN npm install -g serve

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]
