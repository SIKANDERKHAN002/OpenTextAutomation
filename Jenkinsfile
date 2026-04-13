pipeline {
   agent any
   // ---------- Optional: Pipeline Triggers ----------
   /*
   triggers {
       Uncomment to schedule job every day at 7 AM
       cron('H 7 * * *')


       Uncomment to auto-trigger on every Git change (poll SCM every minute)
       pollSCM('* * * * *')
   }
   */
   // ---------- Parameters ----------
   parameters {
       choice(name: 'BROWSER', choices: ['firefox','chrome', 'edge'], description: 'Select the browser')
       choice(name: 'MARKER', choices: ['smoke', 'regression', 'sanity'], description: 'Select test group/marker')
   }
   // ---------- Environment Variables ----------
   environment {
       PROJECT_NAME   = "PytestAutomation"
       REPORT_DIR     = "reports"
       ALLURE_RESULTS = "${REPORT_DIR}\\allure-results"
       ALLURE_HTML    = "${REPORT_DIR}\\allure-html"
       PYTEST_HTML    = "${REPORT_DIR}\\pytest-report.html"
   }
   // ---------- Stages ----------
   stages {
       stage('Initialize') {
           steps {
               echo '🔧 Initializing pipeline...'
           }
       }
       stage('Checkout Code') {
           steps {
               echo 'Checking out code from GitHub...'
               git branch: 'main',git url: 'https://github.com/SIKANDERKHAN002/OpenTextAutomation.git'
           }
       }
       stage('Clean Old Reports') {
           steps {
               echo 'Cleaning up old reports...'
               bat "rmdir /s /q %ALLURE_RESULTS% || exit 0"
               bat "rmdir /s /q %ALLURE_HTML% || exit 0"
               bat "del %PYTEST_HTML% || exit 0"
           }
       }
       stage('Start Selenium Grid') {
           steps {
               echo 'Starting Selenium Grid via Docker...'
               bat 'docker-compose down || exit 0'
               bat 'docker-compose up -d'
           }
       }
       stage('Install Python Dependencies') {
           steps {
               echo 'Setting up virtual environment and installing dependencies...'
               bat 'python -m venv venv'
               bat 'call venv\\Scripts\\activate.bat && pip install -r requirements.txt'
           }
       }
       stage('Run Pytest Tests') {
           steps {
               script {
                   catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                       def command = """
                           call venv\\Scripts\\activate.bat && pytest -s -v -m "${params.MARKER}" ^
                           --reruns=2 --reruns-delay=2 ^
                           --alluredir=%ALLURE_RESULTS% ^
                           --html=%PYTEST_HTML% --self-contained-html ^
                           testCases\\ ^
                           --browser ${params.BROWSER}
                       """
                       echo "Running tests: ${command}"
                       bat "${command}"
                   }
               }
           }
       }
       stage('Generate Allure Report') {
           steps {
               echo 'Generating Allure HTML Report...'
               bat "allure generate %ALLURE_RESULTS% -o %ALLURE_HTML% --clean"
           }
       }
       // Optional: Enable to publish Pytest HTML report in Jenkins UI
       /*
       stage('Publish Pytest HTML Report') {
           steps {
               publishHTML(target: [
                   reportDir: 'reports',
                   reportFiles: 'pytest-report.html',
                   reportName: 'Pytest HTML Report',
                   keepAll: true,
                   alwaysLinkToLastBuild: true,
                   allowMissing: false
               ])
           }
       }
       */
       stage('Publish Allure Report in Jenkins UI') {
           steps {
               echo 'Allure Report will be visible via Jenkins Allure Plugin.'
           }
       }
       stage('Archive Reports') {
           steps {
               echo 'Archiving test reports...'
               archiveArtifacts artifacts: "${ALLURE_HTML}/**", fingerprint: true
               archiveArtifacts artifacts: "${PYTEST_HTML}", fingerprint: true
           }
       }
   }
   // ---------- Post Actions ----------
   post {
       always {
           echo 'Always publishing Allure results and stopping Docker Grid...'
           allure includeProperties: false,
                  jdk: '',
                  results: [[path: "${env.ALLURE_RESULTS}"]]
           echo "Stopping Selenium Grid..."
           bat 'docker-compose down || true'
       }
       success {
           emailext(
               to: 'sikander@gmail.com, jatin@gmail.com, sohan24@gmail.com',
               subject: "[${env.PROJECT_NAME}] Jenkins Job #${env.BUILD_NUMBER} - PASSED",
               mimeType: 'text/html',
               body: """
                   <h2 style="color:green;">Build Success - ${env.PROJECT_NAME}</h2>
                   <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
                       <tr><th>Project</th><td>${env.PROJECT_NAME}</td></tr>
                       <tr><th>Job Name</th><td>${env.JOB_NAME}</td></tr>
                       <tr><th>Build Number</th><td>#${env.BUILD_NUMBER}</td></tr>
                       <tr><th>Browser</th><td>${params.BROWSER}</td></tr>
                       <tr><th>Marker</th><td>${params.MARKER}</td></tr>
                       <tr><th>Threads</th><td>${params.PARALLEL}</td></tr>
                       <tr><th>Allure Report</th><td><a href="${env.BUILD_URL}allure">View Allure Report</a></td></tr>
                       <tr><th>Console Logs</th><td><a href="${env.BUILD_URL}console">View Console</a></td></tr>
                   </table>
                   <p style="margin-top:20px;">Great job! All tests passed for <strong>${env.PROJECT_NAME}</strong>.</p>
                   <p>Regards,<br><strong>Sikander</strong></p>
               """,
               from: "Sikander <sikander@gmail.com>"
           )
       }
       failure {
           emailext(
               to: 'sikander@gmail.com, dileepkumarpaidi@gmail.com, narayan24@gmail.com',
               subject: "[${env.PROJECT_NAME}] Jenkins Job #${env.BUILD_NUMBER} - FAILED",
               mimeType: 'text/html',
               body: """
                   <h2 style="color:red;">Build Failed - ${env.PROJECT_NAME}</h2>
                   <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
                       <tr><th>Project</th><td>${env.PROJECT_NAME}</td></tr>
                       <tr><th>Job Name</th><td>${env.JOB_NAME}</td></tr>
                       <tr><th>Build Number</th><td>#${env.BUILD_NUMBER}</td></tr>
                       <tr><th>Browser</th><td>${params.BROWSER}</td></tr>
                       <tr><th>Marker</th><td>${params.MARKER}</td></tr>
                       <tr><th>Threads</th><td>${params.PARALLEL}</td></tr>
                       <tr><th>Allure Report</th><td><a href="${env.BUILD_URL}allure">View Allure Report</a></td></tr>
                       <tr><th>Console Logs</th><td><a href="${env.BUILD_URL}console">View Console</a></td></tr>
                   </table>
                   <p style="margin-top:20px;">Please review the logs and fix the issues.</p>
                   <p>Regards,<br><strong>Sikander</strong></p>
               """,
               from: "sikander <sikander@gmail.com>"
           )
       }
   }
}