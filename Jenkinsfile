pipeline {
    agent any

    triger {
        pollSCM('H/2 * * * *') // Polls the SCM every 5 minutes
    }
    stages {
        stage('Setup Python') {
            steps {
                echo '=== Python version ==='
                sh 'python3 --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '=== Creating fresh virtual environment ==='
                sh 'rm -rf venv'
                sh 'python3 -m venv venv'

                echo '=== Installing dependencies ==='
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Lint') {
            steps {
                echo '=== Running ruff ==='
                sh '. venv/bin/activate && ruff check .'
            }
        }

        stage('Test') {
            steps {
                echo '=== Running pytest ==='
                sh '. venv/bin/activate && pytest -v'
            }
        }

        stage('Build Image') {
            steps {
                echo '=== Building Docker image ==='
                sh 'docker build -t aws-k8s-app:${BUILD_NUMBER} -t aws-k8s-app:latest .'
                sh 'docker images aws-k8s-app'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo '✅ Build SUCCESS — all checks passed.'
        }
        failure {
            echo '❌ Build FAILED — please check the logs.'
        }
    }
}