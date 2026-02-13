pipeline {
    agent any

    environment {
        REPO_URL    = "https://github.com/2022BCS0004-Ananya/Lab2.git"
        BRANCH_NAME = "main"
        IMAGE_NAME  = "ananyabcs4/lab6-wine-quality-2022bcs0004"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: "${BRANCH_NAME}",
                    credentialsId: 'git-creds',
                    url: "${REPO_URL}"
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                . venv/bin/activate
                python train.py
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    def metrics = readJSON file: 'app/artifacts/metrics.json'
                    def acc = metrics.r2

                    env.CURRENT_ACCURACY = acc.toString()
                    echo "Current Accuracy: ${env.CURRENT_ACCURACY}"
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'best-accuracy', variable: 'BEST_ACC')]) {

                        if (env.CURRENT_ACCURACY.toFloat() <= BEST_ACC.toFloat()) {
                            error("Model did NOT improve.")
                        } else {
                            echo "Model improved!"
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression {
                    return env.CURRENT_ACCURACY.toFloat() > 
                           withCredentials([string(credentialsId: 'best-accuracy', variable: 'BEST_ACC')]) {
                               return BEST_ACC.toFloat()
                           }
                }
            }
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-creds') {
                        sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                        sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
                    }
                }
            }
        }

        stage('Push Docker Image') {
            when {
                expression {
                    return env.CURRENT_ACCURACY.toFloat() > 
                           withCredentials([string(credentialsId: 'best-accuracy', variable: 'BEST_ACC')]) {
                               return BEST_ACC.toFloat()
                           }
                }
            }
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-creds') {
                        sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                        sh "docker push ${IMAGE_NAME}:latest"
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'app/artifacts/**', fingerprint: true
        }
    }
}
