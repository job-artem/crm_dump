FROM node:lts-alpine as develop-stage
WORKDIR /frontend
COPY package*.json ./
RUN yarn install
COPY . .

FROM develop-stage as build-stage
RUN yarn build


FROM nginx:stable-alpine as production-stage
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build-stage /frontend/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]