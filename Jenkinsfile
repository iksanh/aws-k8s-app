pipeline {
    agent any

    environment {
        // Docker Hub config
        DOCKERHUB_USER  = 'iksanhariji'
        IMAGE_NAME      = "${DOCKERHUB_USER}/aws-k8s-app"
        IMAGE_TAG       = "${BUILD_NUMBER}"

        // Manifest repo config — GANTI sesuai punyamu
        MANIFEST_REPO   = 'https://github.com/iksanh/aws-k8s-manifests.git'
        MANIFEST_BRANCH = 'main'
        MANIFEST_FILE   = 'apps/fastapi/deployment.yaml'

        // Git identity untuk commit dari Jenkins
        GIT_USER_EMAIL  = 'iksanhariji@gmail.com'
        GIT_USER_NAME   = 'iksanh'
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

        stage('Update Manifest Repo') {
            steps {
                echo '=== Updating image tag in manifest repo ==='
                withCredentials([usernamePassword(
                    credentialsId: 'github-manifest-pat',
                    usernameVariable: 'GH_USER',
                    passwordVariable: 'GH_TOKEN'
                )]) {
                    sh '''
                        set -e

                        # Clean clone dari awal, jangan reuse folder lama
                        rm -rf manifest-repo
                        git clone https://${GH_USER}:${GH_TOKEN}@${MANIFEST_REPO} manifest-repo
                        cd manifest-repo

                        # Set identity untuk commit ini
                        git config user.email "${GIT_USER_EMAIL}"
                        git config user.name "${GIT_USER_NAME}"

                        # Ganti tag image. Format yang dicari: "image: iksanhariji/aws-k8s-app:<apapun>"
                        # Pakai delimiter | di sed karena image name ada karakter /
                        sed -i "s|image: ${IMAGE_NAME}:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|g" ${MANIFEST_FILE}

                        echo "=== Diff after sed ==="
                        git diff ${MANIFEST_FILE}

                        # Commit & push hanya kalau ada perubahan
                        if git diff --quiet ${MANIFEST_FILE}; then
                            echo "ℹ️  No changes — tag sudah sama, skip commit"
                        else
                            git add ${MANIFEST_FILE}
                            git commit -m "ci: update image tag to ${IMAGE_TAG} [skip ci]"
                            git push origin ${MANIFEST_BRANCH}
                            echo "✅ Manifest updated to ${IMAGE_NAME}:${IMAGE_TAG}"
                        fi
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
            sh 'docker logout || true'
            sh 'rm -rf manifest-repo || true'
        }
        success {
            echo '✅ Build SUCCESS — all checks passed.'
        }
        failure {
            echo '❌ Build FAILED — please check the logs.'
        }
    }
}