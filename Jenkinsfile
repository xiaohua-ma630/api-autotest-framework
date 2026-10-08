pipeline {
    agent any
    parameters { string(name: 'TEST_ENV', defaultValue: 'test', description: '测试环境') }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Install') {
            steps { bat 'pip install -r requirements.txt -q' }
        }
        stage('Run Tests') {
            steps {
                bat 'pytest'
            }
            post {
                always {
                    allure includeProperties: false, jdk: '', results: [[path: 'report/allure-results']]
                }
            }
        }
    }
    post {
        failure { emailext subject: "接口自动化失败: ${JOB_NAME} #${BUILD_NUMBER}", to: "qa-team@example.com", body: "请查看 Allure 报告: ${BUILD_URL}allure" }
    }
}
