# Шаг 1: Используем официальный образ Node.js для сборки
#FROM node:18 AS build-stage

# Устанавливаем рабочую директорию
#WORKDIR /frontend/

# Копируем package.json и package-lock.json
#COPY ./frontend/package.json ./frontend/package-lock.json ./

# Устанавливаем зависимости
#RUN npm install

# Копируем все остальные файлы в контейнер
#COPY ./frontend/ .

#RUN npm run build

# Шаг 2: Используем минимальный сервер на Nginx для размещения собранного приложения
#FROM nginx:alpine AS production-stage

# Копируем собранное приложение из предыдущего образа
#COPY --from=build-stage /frontend/dist /usr/share/nginx/html

# Экспонируем 80 порт
#EXPOSE 8080

# Указываем команду для запуска Nginx
#CMD ["nginx", "-g", "daemon off;"]


FROM nginx:alpine

COPY ./frontend/dist  /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

