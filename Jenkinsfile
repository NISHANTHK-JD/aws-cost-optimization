pipeline {
    agent any

    environment {
        APP_NAME     = "sample-app"
        DOCKER_IMAGE = "${APP_NAME}:${env.BUILD_NUMBER}"
        SONAR_TOKEN  = credentials('sonar-token')
    }

    triggers {
        githubPush()
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo "Building application..."
                sh 'chmod +x scripts/build.sh && ./scripts/build.sh'
            }
        }

        stage('Unit Test') {
            steps {
                echo "Running unit tests..."
                sh 'chmod +x scripts/test.sh && ./scripts/test.sh'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results/**/*.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo "Running static code analysis..."
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=${APP_NAME} \
                          -Dsonar.sources=app/ \
                          -Dsonar.login=${SONAR_TOKEN}
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo "Waiting for SonarQube quality gate result..."
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo "Building Docker image: ${DOCKER_IMAGE}"
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Docker Push') {
            steps {
                echo "Pushing Docker image to registry..."
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE}
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying application..."
                sh 'chmod +x scripts/deploy.sh && ./scripts/deploy.sh'
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded for build #${env.BUILD_NUMBER}"
            slackSend(
                color  : 'good',
                message: "SUCCESS: ${APP_NAME} build #${env.BUILD_NUMBER} deployed. ${env.BUILD_URL}"
            )
        }
        failure {
            echo "Pipeline FAILED for build #${env.BUILD_NUMBER}"
            slackSend(
                color  : 'danger',
                message: "FAILED: ${APP_NAME} build #${env.BUILD_NUMBER}. Check: ${env.BUILD_URL}"
            )
        }
        always {
            cleanWs()
        }
    }
}
