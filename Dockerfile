# Step 1: 기본 이미지
FROM eclipse-temurin:17

# Step 2: 작업 디렉토리 생성
RUN mkdir /opt/app

# Step 3: 빌드된 파일 복사
COPY build/libs/carbot_back /opt/app/docker-app.jar

# Step 4: 애플리케이션 실행 명령어
CMD ["java", "-jar", "/opt/app/docker-app.jar"]
