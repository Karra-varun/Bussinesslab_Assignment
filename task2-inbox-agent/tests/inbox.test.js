"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * Automated Test Suite for Task 2: The Inbox Agent.
 */
const intentClassifier_1 = require("../src/agent/intentClassifier");
const learningEngine_1 = require("../src/agent/learningEngine");
const sampleEmails_1 = require("../src/data/sampleEmails");
function runTests() {
    console.log('Running Task 2 Inbox Agent Tests...\n');
    let passed = 0;
    let failed = 0;
    function assert(condition, desc) {
        if (condition) {
            console.log(`✅ PASS: ${desc}`);
            passed++;
        }
        else {
            console.error(`❌ FAIL: ${desc}`);
            failed++;
        }
    }
    // 1. Dataset size verification
    assert(sampleEmails_1.SAMPLE_EMAILS.length >= 50, `Sample emails dataset has ${sampleEmails_1.SAMPLE_EMAILS.length} >= 50 emails`);
    // 2. Intent Classifier verification
    const howToIntent = intentClassifier_1.intentClassifier.classify({
        subject: 'Where is the social media tab?',
        body: 'How do I add social media links in settings?'
    });
    assert(howToIntent.category === 'HOW_TO', 'Classifies HOW_TO questions correctly');
    const refundIntent = intentClassifier_1.intentClassifier.classify({
        subject: 'Refund request for accidental charge',
        body: 'Please refund our transaction TXN_1234.'
    });
    assert(refundIntent.category === 'REFUND_CANCELLATION', 'Classifies REFUND_CANCELLATION correctly');
    assert(refundIntent.entities.transactionId === 'TXN_1234', 'Extracts transaction ID from email');
    const outageIntent = intentClassifier_1.intentClassifier.classify({
        subject: 'URGENT: 500 error on checkout',
        body: 'The directory signup is down!'
    });
    assert(outageIntent.category === 'COMPLAINT_OUTAGE', 'Classifies COMPLAINT_OUTAGE correctly');
    assert(outageIntent.urgency === 'URGENT', 'Identifies urgent outage severity');
    // 3. Edit Distance & Similarity verification
    const simExact = learningEngine_1.learningEngine.calculateSimilarity('Hello world', 'Hello world');
    assert(simExact === 1.0, 'Exact match has similarity 1.0');
    const simSlight = learningEngine_1.learningEngine.calculateSimilarity('Hello world', 'Hello world!');
    assert(simSlight > 0.90, 'Slight punctuation edit maintains high similarity');
    // 4. Learning & Streak Increment verification
    const initialRules = learningEngine_1.learningEngine.getAutonomyStatus().find((r) => r.category === 'HOW_TO');
    const initialStreak = initialRules?.streakCount || 0;
    learningEngine_1.learningEngine.recordAction('TEST-1', 'HOW_TO', 'SEND_AS_IS', 'Standard draft reply', 'Standard draft reply');
    const afterSendRule = learningEngine_1.learningEngine.getAutonomyStatus().find((r) => r.category === 'HOW_TO');
    assert(afterSendRule?.streakCount === initialStreak + 1, 'Unchanged send increments autonomy streak');
    // 5. Human Edit Learning extraction
    const feedback = learningEngine_1.learningEngine.recordAction('TEST-2', 'REFUND_CANCELLATION', 'EDIT_AND_SEND', 'We will process your refund.', 'We will process your refund via Stripe in 3-5 business days.');
    assert(!feedback.isUnchanged, 'Substantive edit is marked as changed');
    assert(feedback.extractedLearning !== undefined, 'Extracts new policy learning rule from human edit');
    // 6. 20-in-a-row Autonomy Unlocking verification
    for (let i = 1; i <= 20; i++) {
        learningEngine_1.learningEngine.recordAction(`STREAK-${i}`, 'NEW_PROJECT', 'SEND_AS_IS', 'Thank you for reaching out.', 'Thank you for reaching out.');
    }
    const projectRule = learningEngine_1.learningEngine.getAutonomyStatus().find((r) => r.category === 'NEW_PROJECT');
    assert(projectRule?.isAutonomous === true, '20-in-a-row sends without edits unlocks isAutonomous = true');
    // 7. Circuit Breaker verification
    learningEngine_1.learningEngine.tripCircuitBreaker('NEW_PROJECT', 'Customer complaint received');
    const revokedRule = learningEngine_1.learningEngine.getAutonomyStatus().find((r) => r.category === 'NEW_PROJECT');
    assert(revokedRule?.isAutonomous === false, 'Circuit breaker trips and revokes autonomy');
    assert(revokedRule?.circuitBreakerTripped === true, 'Circuit breaker status is true');
    console.log(`\nTest Summary: ${passed} Passed, ${failed} Failed.`);
    if (failed > 0) {
        process.exit(1);
    }
}
runTests();
