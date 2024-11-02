FROM eclipse-temurin:17
RUN mkdir /opt/app
COPY build/libs/carbot_back docker-app.jar
CMD ["java","-jar", "docker-app.jar"]
EXPOSE 8001
