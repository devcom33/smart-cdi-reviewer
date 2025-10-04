FROM maven:3.9.5-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests


FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

COPY --from=build target/*.jar smartcdi-image.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "smartcdi-image.jar"]
