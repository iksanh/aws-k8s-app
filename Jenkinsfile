pipeline {
       agent any

       environment {
           DOCKERHUB_USER = 'iksanhariji'                    // ← GANTI dengan username Docker Hub kamu
           IMAGE_NAME     = "${DOCKERHUB_USER}/aws-k8s-app"
           IMAGE_TAG      = "${BUILD_NUMBER}"
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
                   sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
                   sh "docker images ${IMAGE_NAME}"
               }
           }

           stage('Push Image') {
               steps {
                   echo '=== Pushing to Docker Hub ==='
                   withCredentials([usernamePassword(
                       credentialsId: 'dockerhub-creds',
                       usernameVariable: 'DH_USER',
                       passwordVariable: 'DH_PASS'
                   )]) {
                       sh 'echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin'
                       sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                       sh "docker push ${IMAGE_NAME}:latest"
                       sh 'docker logout'
                   }
               }
           }
       }

       post {
           always {
               echo 'Pipeline finished.'
               sh 'docker logout || true'
           }
           success {
               echo '✅ Build SUCCESS — all checks passed.'
           }
           failure {
               echo '❌ Build FAILED — please check the logs.'
           }
       }
   }