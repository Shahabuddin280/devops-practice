pipeline {
    agent any

    environment {
        IMAGE_NAME = "devops-practice-hello-net"   // Docker image name
        BRANCH_NAME = "feature1"
        DOCKER_COMPOSE_PATH = "/usr/local/bin/docker-compose" // full path to docker-compose
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "Checking out feature1 branch..."
                git branch: "${BRANCH_NAME}", url: 'https://github.com/Shahabuddin280/devops-practice.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh "docker build -t shahabuddin/$IMAGE_NAME:$BUILD_NUMBER ."
            }
        }

        stage('Run Docker-Compose') {
            steps {
                echo "Deploying containers with docker-compose..."
                // Stop old containers if running
                sh "${DOCKER_COMPOSE_PATH} down || true"
                // Start new containers
                sh "${DOCKER_COMPOSE_PATH} up -d --build"
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                echo "Logging in to DockerHub and pushing image..."
                withCredentials([usernamePassword(credentialsId: 'shahab12345', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh "docker tag shahabuddin/$IMAGE_NAME:$BUILD_NUMBER $DOCKER_USER/$IMAGE_NAME:$BUILD_NUMBER"
                    sh "docker push $DOCKER_USER/$IMAGE_NAME:$BUILD_NUMBER"
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully! 🎉"
        }
        failure {
            echo "Pipeline failed. Check logs! ❌"
        }
    }
}
