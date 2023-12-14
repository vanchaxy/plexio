FROM node:18.2.0-alpine as build

WORKDIR /app

COPY package.json ./

RUN npm install

COPY . ./
RUN npm run build

FROM nginx:stable-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]