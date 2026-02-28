pipeline {
    agent any

    environment {
        IMAGE_NAME = "arjundockerhublab/lab6-model:latest"
        CONTAINER_NAME = "lab7_inference_test"
        API_PORT = "8030"
    }

    stages {

        stage('Pull Image') {
            steps {
                echo "Pulling Docker image..."
                sh "docker pull ${IMAGE_NAME}"
            }
        }

        stage('Run Container') {
            steps {
                echo "Starting container..."
                sh """
                    docker run -d -p ${API_PORT}:8030 --name ${CONTAINER_NAME} ${IMAGE_NAME}
                """
            }
        }

        stage('Wait for Service Readiness') {
            steps {
                echo "Waiting for API to become ready..."

                script {
                    timeout(time: 60, unit: 'SECONDS') {
                        waitUntil {
                            def status = sh(
                                script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:${API_PORT}/ || true",
                                returnStdout: true
                            ).trim()

                            echo "Current status: ${status}"
                            return (status == "200")
                        }
                    }
                    echo "✅ Service is ready."
                }
            }
        }

        stage('Send Valid Inference Request') {
            steps {
                echo "Sending valid inference request..."

                script {

                    def response = sh(
                        script: """
                        curl -s -X POST http://localhost:${API_PORT}/predict \
                        -H "Content-Type: application/json" \
                        -d '{
                            "features": [7.4, 0.7, 0.0, 1.9, 0.076, 11.0, 34.0, 0.9978, 3.51, 0.56, 9.4]
                        }'
                        """,
                        returnStdout: true
                    ).trim()

                    echo "API Response: ${response}"

                    if (!response.contains("prediction")) {
                        error("❌ Prediction field missing in response.")
                    }

                    def parsed = readJSON text: response

                    if (!(parsed.prediction instanceof Number)) {
                        error("❌ Prediction is not numeric.")
                    }

                    echo "✅ Valid inference test passed."
                }
            }
        }

        stage('Send Invalid Request') {
            steps {
                echo "Sending invalid inference request..."

                script {

                    def status = sh(
                        script: """
                        curl -s -o response.txt -w '%{http_code}' -X POST \
                        http://localhost:${API_PORT}/predict \
                        -H "Content-Type: application/json" \
                        -d '{"wrong_input": [1,2,3]}'
                        """,
                        returnStdout: true
                    ).trim()

                    def body = readFile('response.txt')
                    echo "Error Response: ${body}"
                    echo "Status Code: ${status}"

                    if (status == "200") {
                        error("❌ Invalid input did not fail as expected.")
                    }

                    if (!body.toLowerCase().contains("error") &&
                        !body.toLowerCase().contains("detail")) {
                        error("❌ Error message not meaningful.")
                    }

                    echo "✅ Invalid input test passed."
                }
            }
        }

        stage('Stop Container') {
            steps {
                echo "Stopping container..."
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                """
            }
        }
    }

    post {
        always {
            echo "Cleaning up..."
            sh """
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
            """
        }

        success {
            echo "🎉 All inference validation tests passed!"
        }

        failure {
            echo "🚨 Pipeline failed due to validation error."
        }
    }
}
