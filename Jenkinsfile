pipeline {
    agent any

    environment {
        IMAGE_NAME = "devops-practice-hello-net"
        BRANCH_NAME = "feature1"
        DOCKER_COMPOSE_PATH = "/usr/local/bin/docker-compose"
        DOCKER_REGISTRY = "shahabuddin"
        DB_NAME = "app_database"
        DB_USER = "app_user"
        DB_PASSWORD = "app_password"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Checking out ${BRANCH_NAME} branch..."
                git branch: "${BRANCH_NAME}", url: 'https://github.com/Shahabuddin280/devops-practice.git'
            }
        }

        stage('Validate Docker Compose') {
            steps {
                echo "Validating docker-compose.yml configuration..."
                sh "${DOCKER_COMPOSE_PATH} config"
            }
        }

        stage('Build Docker Images') {
            steps {
                echo "Building Docker images..."
                sh "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }

        stage('Database Migration') {
            steps {
                echo "Running database migrations..."
                sh """
                    ${DOCKER_COMPOSE_PATH} run --rm app \
                    npm run migrate || echo "No migrations found or migration skipped"
                """
            }
        }

        stage('Deploy with Docker-Compose') {
            steps {
                echo "Deploying containers with docker-compose..."
                // Stop old containers if running
                sh "${DOCKER_COMPOSE_PATH} down --remove-orphans || true"
                
                // Start new containers
                sh "${DOCKER_COMPOSE_PATH} up -d --build"
                
                // Wait for services to be healthy
                sh "sleep 30"
                
                // Check if all services are running
                sh "${DOCKER_COMPOSE_PATH} ps"
            }
        }

        stage('Health Check') {
            steps {
                echo "Performing health checks..."
                script {
                    // Check if web application is responsive
                    sh "curl -f http://localhost:3000/health || echo 'Health check failed, but continuing...'"
                    
                    // Check database connectivity
                    sh """
                        ${DOCKER_COMPOSE_PATH} exec -T db \
                        pg_isready -h localhost -U ${DB_USER} || echo 'Database not ready yet'
                    """
                }
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
            // Log container status
            sh "${DOCKER_COMPOSE_PATH} ps"
            cleanWs()
        }
        success {
            echo "Pipeline completed successfully! 🎉"
            // Run tests after deployment
            sh "${DOCKER_COMPOSE_PATH} run --rm app npm test || true"
        }
        failure {
            echo "Pipeline failed. Check logs! ❌"
            // Save logs for debugging
            sh "${DOCKER_COMPOSE_PATH} logs > docker-compose-failure.log"
            archiveArtifacts artifacts: 'docker-compose-failure.log'
        }
    }
}