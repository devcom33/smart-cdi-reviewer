FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

COPY backend/target/*.jar smartcdi-image.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "smartcdi-image.jar"]