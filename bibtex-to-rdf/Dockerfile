FROM openjdk:17-alpine3.14

WORKDIR /app

COPY .mvn/ .mvn
COPY mvnw pom.xml ./
RUN ./mvnw dependency:go-offline

COPY src ./src
COPY .env ./

CMD ./mvnw spring-boot:run