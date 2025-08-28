/**
 * full-scan-production-score.js
 * Run: node full-scan-production-score.js
 */

const { exec } = require("child_process");
const fs = require("fs");
const path = require("path");

const reportFile = "scan-report.txt";
fs.writeFileSync(reportFile, "=== laundr-me-2 Full Production-Ready Scan + Scoring ===\n\n");

function logToReport(title, output) {
  fs.appendFileSync(reportFile, `\n--- ${title} ---\n`);
  fs.appendFileSync(reportFile, output + "\n");
}

// Score counters
let safetyIssues = 0;
let maintainabilityIssues = 0;
let securityIssues = 0;

// ------------------------ UTILITIES ------------------------

function scanPrompts(dir) {
  if (!fs.existsSync(dir)) return;
  const files = fs.readdirSync(dir);
  files.forEach(file => {
    const fullPath = path.join(dir, file);
    if (fs.statSync(fullPath).isDirectory()) {
      scanPrompts(fullPath);
    } else if (file.endsWith(".txt") || file.endsWith(".json")) {
      const content = fs.readFileSync(fullPath, "utf8");
      const secretPattern = /(API_KEY|SECRET|PASSWORD)/i;
      if (secretPattern.test(content)) {
        const msg = `Found potential secret in ${fullPath}`;
        logToReport("AI Prompt Security Warning", msg);
        safetyIssues += 2;
        securityIssues += 2;
      }
    }
  });
}

function scanOrchestration(dir) {
  if (!fs.existsSync(dir)) return;
  const files = fs.readdirSync(dir);
  files.forEach(file => {
    const fullPath = path.join(dir, file);
    if (fs.statSync(fullPath).isDirectory()) {
      scanOrchestration(fullPath);
    } else if (file.endsWith(".js") || file.endsWith(".ts")) {
      const content = fs.readFileSync(fullPath, "utf8");
      const issues = [];

      if (/while\s*\(\s*true\s*\)/.test(content)) { issues.push("Infinite loop (while true)"); safetyIssues += 5; }
      if (/for\s*\(.*;.*;.*\)\s*{/.test(content) && content.length > 1000) { issues.push("Large for-loop"); safetyIssues += 3; }
      if (/async function.*\{[^}]*[^try]/s.test(content)) { issues.push("Async missing try/catch"); safetyIssues += 2; }
      if (/function\s+\w+\(.*\)\s*{[^}]*\1\(/.test(content)) { issues.push("Recursive call"); safetyIssues += 2; }
      if (/(forEach|map|filter|reduce|for\s*\(.*;.*;.*\))/g.test(content)) { issues.push("Large data operation"); safetyIssues += 2; }
      if (/(for|while).*{\s*(fetch|axios|XMLHttpRequest)/g.test(content)) { issues.push("Network call inside loop"); safetyIssues += 3; }
      if (/async\s+function\s+\w+\(.*\)\s*{[^}]*[^await]\.then\(/g.test(content)) { issues.push("Async call without await"); safetyIssues += 2; }

      if (issues.length) logToReport("Orchestration Risk: " + fullPath, issues.join("\n"));
    }
  });
}

// ------------------------ RUN SCANS ------------------------

console.log("Running ESLint...");
exec("npx eslint . --ext .js,.jsx,.ts,.tsx", (err, stdout, stderr) => {
  const eslintOutput = stdout || stderr || "No JS/TS issues found";
  logToReport("ESLint Results", eslintOutput);

  const eslintErrors = (stdout.match(/error/g) || []).length;
  maintainabilityIssues += eslintErrors;

  console.log("Running Prettier check...");
  exec("npx prettier --check .", (err2, stdout2, stderr2) => {
    const prettierOutput = stdout2 || stderr2 || "All files formatted correctly";
    logToReport("Prettier Check", prettierOutput);

    if (!/All files formatted correctly/.test(prettierOutput)) maintainabilityIssues += 1;

    console.log("Running npm audit...");
    exec("npm audit --json", (err3, stdout3, stderr3) => {
      let auditCount = 0;
      try {
        const auditResults = JSON.parse(stdout3);
        auditCount = Object.keys(auditResults.vulnerabilities || {}).length;
        logToReport("npm Audit Results", JSON.stringify(auditResults, null, 2));
      } catch {
        logToReport("npm Audit Results", stdout3 || stderr3 || "No vulnerabilities found");
      }
      securityIssues += auditCount;

      console.log("Running Python checks...");
      exec("flake8 .", (err4, stdout4, stderr4) => {
        const flakeOutput = stdout4 || stderr4 || "No Python lint issues found";
        logToReport("Python flake8 Results", flakeOutput);

        const flakeCount = (stdout4.match(/\n/g) || []).length;
        maintainabilityIssues += flakeCount;

        exec("bandit -r . -q -f json", (err5, stdout5, stderr5) => {
          try {
            const banditResults = JSON.parse(stdout5);
            const banditCount = banditResults.results ? banditResults.results.length : 0;
            logToReport("Python Bandit Security Scan", JSON.stringify(banditResults, null, 2));
            securityIssues += banditCount;
          } catch {
            logToReport("Python Bandit Scan", stdout5 || stderr5 || "No Bandit issues found");
          }

          console.log("Scanning AI/agent prompts...");
          scanPrompts("./agents");
          scanPrompts("./prompts");

          console.log("Scanning orchestration logic...");
          scanOrchestration("./orchestration");

          // ------------------------ SCORING ------------------------
          const safetyScore = Math.max(0, 100 - safetyIssues*2);
          const maintainScore = Math.max(0, 100 - maintainabilityIssues*2);
          const securityScore = Math.max(0, 100 - securityIssues*5);

          logToReport("SCORES", 
            `Safety Score: ${safetyScore}/100\n` +
            `Maintainability Score: ${maintainScore}/100\n` +
            `Security Score: ${securityScore}/100\n`
          );

          console.log(`Full scan + scoring completed! See ${reportFile}`);
        });
      });
    });
  });
});