/**
 * Learning Engine and Autonomy Manager for Task 2: The Inbox Agent.
 * Features:
 * - Levenshtein edit distance and character similarity computation.
 * - Learning extraction from human edits and custom replies.
 * - Dynamic feedback persistence into feedback_db.json.
 * - 20-in-a-row Autonomy Tracker per category.
 * - Circuit breakers to revoke autonomy on quality drops.
 */
import * as fs from 'fs';
import * as path from 'path';
import {
  EmailCategory,
  HumanActionType,
  HumanFeedback,
  AutonomyRule,
  LearningRule
} from '../types';

export class LearningEngine {
  private feedbackDbPath: string;
  private feedbacks: HumanFeedback[] = [];
  private learnedRules: LearningRule[] = [];
  private autonomyRules: Map<EmailCategory, AutonomyRule> = new Map();

  constructor() {
    const dataDir = path.resolve(__dirname, '../../data');
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true });
    }
    this.feedbackDbPath = path.join(dataDir, 'feedback_db.json');
    this.initAutonomyRules();
    this.loadState();
  }

  private initAutonomyRules() {
    const categories: EmailCategory[] = [
      'HOW_TO',
      'REFUND_CANCELLATION',
      'NEW_PROJECT',
      'QUOTE_REQUEST',
      'COMPLAINT_OUTAGE',
      'FOLLOW_UP'
    ];

    for (const cat of categories) {
      this.autonomyRules.set(cat, {
        category: cat,
        streakCount: 0,
        threshold: 20,
        isAutonomous: false,
        circuitBreakerTripped: false,
        totalSentAutonomously: 0,
        lastUpdated: new Date().toISOString()
      });
    }
  }

  private loadState() {
    if (fs.existsSync(this.feedbackDbPath)) {
      try {
        const raw = fs.readFileSync(this.feedbackDbPath, 'utf-8');
        const data = JSON.parse(raw);
        this.feedbacks = data.feedbacks || [];
        this.learnedRules = data.learnedRules || [];
        if (data.autonomyRules) {
          for (const rule of data.autonomyRules) {
            this.autonomyRules.set(rule.category, rule);
          }
        }
      } catch (err) {
        console.warn('[LearningEngine] Could not parse feedback_db.json:', err);
      }
    }
  }

  private saveState() {
    try {
      const data = {
        feedbacks: this.feedbacks,
        learnedRules: this.learnedRules,
        autonomyRules: Array.from(this.autonomyRules.values())
      };
      fs.writeFileSync(this.feedbackDbPath, JSON.stringify(data, null, 2), 'utf-8');
    } catch (err) {
      console.error('[LearningEngine] Error saving state:', err);
    }
  }

  /**
   * Computes Levenshtein distance between two strings.
   */
  calculateEditDistance(a: string, b: string): number {
    const s1 = a.trim();
    const s2 = b.trim();
    const dp: number[][] = Array(s1.length + 1)
      .fill(null)
      .map(() => Array(s2.length + 1).fill(0));

    for (let i = 0; i <= s1.length; i++) dp[i][0] = i;
    for (let j = 0; j <= s2.length; j++) dp[0][j] = j;

    for (let i = 1; i <= s1.length; i++) {
      for (let j = 1; j <= s2.length; j++) {
        const cost = s1[i - 1] === s2[j - 1] ? 0 : 1;
        dp[i][j] = Math.min(
          dp[i - 1][j] + 1, // deletion
          dp[i][j - 1] + 1, // insertion
          dp[i - 1][j - 1] + cost // substitution
        );
      }
    }

    return dp[s1.length][s2.length];
  }

  calculateSimilarity(original: string, final: string): number {
    const maxLen = Math.max(original.length, final.length);
    if (maxLen === 0) return 1.0;
    const distance = this.calculateEditDistance(original, final);
    return Math.max(0, 1.0 - distance / maxLen);
  }

  /**
   * Records human action on an email draft and updates the autonomy streak.
   */
  recordAction(
    emailId: string,
    category: EmailCategory,
    action: HumanActionType,
    originalDraft: string,
    finalSentText: string
  ): HumanFeedback {
    const similarityRatio = action === 'SEND_AS_IS' ? 1.0 : this.calculateSimilarity(originalDraft, finalSentText);
    const isUnchanged = action === 'SEND_AS_IS' || similarityRatio >= 0.95;

    let extractedLearning: string | undefined = undefined;

    const rule = this.autonomyRules.get(category)!;

    if (isUnchanged) {
      // Increment autonomy streak towards 20
      rule.streakCount += 1;
      if (rule.streakCount >= rule.threshold) {
        rule.isAutonomous = true;
        rule.circuitBreakerTripped = false;
      }
    } else {
      // Extract what the human changed or added
      extractedLearning = this.extractLearningPattern(category, originalDraft, finalSentText);
      const newRule: LearningRule = {
        id: `LR-${Date.now().toString(36).toUpperCase()}`,
        category,
        ruleText: extractedLearning,
        sourceEmailId: emailId,
        createdAt: new Date().toISOString(),
        weight: 1.0
      };
      this.learnedRules.unshift(newRule);

      // Reset streak or trip circuit breaker if it was previously autonomous
      if (rule.isAutonomous) {
        rule.isAutonomous = false;
        rule.circuitBreakerTripped = true;
        rule.tripReason = `Human operator intervened and made significant modifications (Similarity: ${Math.round(similarityRatio * 100)}%). Autonomy revoked for safety.`;
      }
      rule.streakCount = 0;
    }

    rule.lastUpdated = new Date().toISOString();

    const feedback: HumanFeedback = {
      emailId,
      category,
      action,
      originalDraft,
      finalSentText,
      similarityRatio: Math.round(similarityRatio * 100) / 100,
      isUnchanged,
      extractedLearning,
      timestamp: new Date().toISOString()
    };

    this.feedbacks.unshift(feedback);
    this.saveState();
    return feedback;
  }

  private extractLearningPattern(category: EmailCategory, _original: string, final: string): string {
    const finalLower = final.toLowerCase();
    if (category === 'REFUND_CANCELLATION') {
      if (finalLower.includes('3-5 business days') || finalLower.includes('stripe')) {
        return 'Clarify that refunds reflect in 3-5 business days via Stripe and transaction logs are updated.';
      }
      if (finalLower.includes('discount') || finalLower.includes('retain')) {
        return 'Offer a 15% plan discount retention option prior to confirming final cancellation.';
      }
      return 'State standard 30-day refund guarantee window and request transaction confirmation ID.';
    }

    if (category === 'HOW_TO') {
      if (finalLower.includes('dashboard >') || finalLower.includes('step 1')) {
        return 'Format step-by-step UI dashboard navigation paths with explicit bold bullet points.';
      }
      return 'Ensure screenshots or documentation URLs are explicitly hyperlinked in the closing paragraph.';
    }

    if (category === 'NEW_PROJECT' || category === 'QUOTE_REQUEST') {
      return 'Emphasize that 85% of directory features can be achieved via native settings ($0 custom code).';
    }

    return 'Refine tone to be concise, polite, and directly address the user query first.';
  }

  /**
   * Retrieves all learned rules for a given category to inject into future prompts.
   */
  getRulesForCategory(category: EmailCategory): string[] {
    return this.learnedRules
      .filter((r) => r.category === category)
      .slice(0, 5)
      .map((r) => r.ruleText);
  }

  getAutonomyStatus(): AutonomyRule[] {
    return Array.from(this.autonomyRules.values());
  }

  getLearnedRules(): LearningRule[] {
    return this.learnedRules;
  }

  getFeedbackHistory(): HumanFeedback[] {
    return this.feedbacks;
  }

  /**
   * Manually trips the circuit breaker on quality drop or user request.
   */
  tripCircuitBreaker(category: EmailCategory, reason: string): AutonomyRule {
    const rule = this.autonomyRules.get(category)!;
    rule.isAutonomous = false;
    rule.circuitBreakerTripped = true;
    rule.tripReason = reason;
    rule.streakCount = 0;
    rule.lastUpdated = new Date().toISOString();
    this.saveState();
    return rule;
  }
}

export const learningEngine = new LearningEngine();
