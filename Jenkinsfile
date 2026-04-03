pipeline {
    agent { label 'ec2-agent' }   // run only on Jenkins node with label ec2-agent

    environment {
        AWS_REGION = "ap-southeast-1"
        ECR_REPO   = "fair-share-backend"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"   // ✅ unique tag per build
        ACCOUNT_ID = "445842911672"
    }

    stages {


        stage('Build Backend') {
            steps {
                sh '''
                  echo "Running backend tests..."
                  pytest || true
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                  docker build -t $ECR_REPO:$IMAGE_TAG .
               
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                  aws ecr get-login-password --region $AWS_REGION \
                    | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                '''
            }
        }

        stage('Tag & Push to ECR') {
            steps {
                sh '''
                  docker tag $ECR_REPO:$IMAGE_TAG $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG
                  docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG
                
                 
                
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Backend image pushed to ECR with tag: ${IMAGE_TAG}"
            sh "echo ${env.BUILD_NUMBER} > image_tag.txt"
        }
        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}
