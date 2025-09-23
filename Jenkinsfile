pipeline {
    agent any

    environment {
        IMAGE_NAME = "devops-practice-hello-net"
        BRANCH_NAME = "feature1"
        DOCKER_COMPOSE_PATH = "/usr/local/bin/docker-compose"
        DOCKER_REGISTRY = "shahabuddin"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Checking out ${BRANCH_NAME} branch..."
                git branch: "${BRANCH_NAME}", url: 'https://github.com/Shahabuddin280/devops-practice.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }

        stage('Run Docker-Compose') {
            steps {
                echo "Deploying containers with docker-compose..."
                sh "${DOCKER_COMPOSE_PATH} down || true"
                sh "${DOCKER_COMPOSE_PATH} up -d --build"
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                echo "Logging in to DockerHub and pushing image..."
                withCredentials([usernamePassword(
                    credentialsId: 'shahab12345', 
                    usernameVariable: 'DOCKER_USER', 
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}"
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline execution completed."
            cleanWs() // Clean workspace after build
        }
        success {
            echo "Pipeline completed successfully! 🎉"
        }
        failure {
            echo "Pipeline failed. Check logs! ❌"
        }
    }
}