/**
 * Grounded Email Reply Drafter for Task 2: The Inbox Agent.
 * Features:
 * - Queries Task 1 Knowledge Brain API for ground truth facts.
 * - Writes in Company Voice (helpful, professional, concise, structured).
 * - Dynamically incorporates past learned rules from human edits.
 * - Evaluates Autonomy Eligibility (streak >= 20 without edits).
 */
import { CustomerEmail, DraftReply, KBQueryResponse } from '../types';
import { kbClient } from '../client/knowledgeBrainClient';
import { learningEngine } from './learningEngine';

export class EmailDrafter {
  /**
   * Generates a grounded, learned draft reply for a customer email.
   */
  async generateDraft(email: CustomerEmail): Promise<DraftReply> {
    const category = email.intent.category;
    const learnedRules = learningEngine.getRulesForCategory(category);
    const autonomyRules = learningEngine.getAutonomyStatus().find((r) => r.category === category);

    // Step 1: Query Knowledge Brain API (Task 1)
    const kbQueryText = `${email.subject}. ${email.body}`;
    const kbResponse: KBQueryResponse = await kbClient.queryKnowledge(kbQueryText, 3);

    // Step 2: Build Company Voice Reply
    const draftText = this.synthesizeReply(email, kbResponse, learnedRules);

    const confidenceScore = kbResponse.confidence;
    const isAutonomous = autonomyRules?.isAutonomous || false;
    const canAutoSend = isAutonomous && confidenceScore >= 0.85;

    return {
      emailId: email.id,
      subject: `Re: ${email.subject}`,
      body: draftText,
      citations: kbResponse.citations || [],
      reasoning: `Categorized as ${category} (${email.intent.subcategory}). Retrieved ${kbResponse.citations.length} solution citations with confidence ${confidenceScore}. Injected ${learnedRules.length} learned team preferences.`,
      confidenceScore,
      appliedLearnedRules: learnedRules,
      generatedAt: new Date().toISOString(),
      canAutoSend
    };
  }

  private synthesizeReply(
    email: CustomerEmail,
    kb: KBQueryResponse,
    learnedRules: string[]
  ): string {
    const firstName = email.fromName.split(' ')[0] || 'there';
    const category = email.intent.category;

    const sections: string[] = [];

    // Greeting
    sections.push(`Hi ${firstName},`);

    // Opening & Empathy
    if (category === 'COMPLAINT_OUTAGE') {
      sections.push(
        `Thank you for alerting us right away. I completely understand how critical this is for your operations, and our technical team is actively prioritizing it.`
      );
    } else if (category === 'REFUND_CANCELLATION') {
      sections.push(
        `Thank you for reaching out regarding your account and billing. We are happy to assist you with this directly.`
      );
    } else if (category === 'NEW_PROJECT' || category === 'QUOTE_REQUEST') {
      sections.push(
        `Thank you for considering us for your directory platform! Your project sounds exciting and aligns closely with what our consultancy delivers.`
      );
    } else {
      sections.push(`Thank you for reaching out. Here is the exact information you need regarding your inquiry.`);
    }

    // Ground Truth from Knowledge Brain
    if (kb.citations && kb.citations.length > 0) {
      const topCitation = kb.citations[0];
      sections.push(
        `Based on our verified product documentation for **${topCitation.title}**:\n` +
        `• ${topCitation.snippet.replace(/\n/g, ' ')}`
      );

      if (topCitation.screenshot_url) {
        sections.push(
          `🖼️ **Visual Guide**: We also have a helpful screenshot illustrating this layout in your admin panel: [View Screenshot](${topCitation.screenshot_url})`
        );
      }
    } else {
      sections.push(`• ${kb.answer}`);
    }

    // Injected Learned Policy Rules
    if (learnedRules.length > 0) {
      const ruleExcerpts = learnedRules.map((r) => `• ${r}`).join('\n');
      sections.push(`**Key Notes & Policy:**\n${ruleExcerpts}`);
    } else {
      if (category === 'REFUND_CANCELLATION') {
        sections.push(
          `**Billing Policy Note**: In accordance with our standard policy, refunds are processed back to your original payment method via Stripe within 3-5 business days.`
        );
      } else if (category === 'NEW_PROJECT' || category === 'QUOTE_REQUEST') {
        sections.push(
          `**Pro Tip**: Over 85% of standard directory workflows can be configured via native admin settings with $0 custom development costs.`
        );
      }
    }

    // Next Steps & Closing
    if (category === 'NEW_PROJECT' || category === 'QUOTE_REQUEST') {
      sections.push(
        `Would you be available for a brief 20-minute discovery call this week to finalize your feature requirements and proposal?`
      );
    } else {
      sections.push(
        `Please let us know if you have any follow-up questions or if you'd like us to guide you through any part of the setup!`
      );
    }

    sections.push(`Best regards,\nAI Tech Consultant Team\nsupport@businesslabs.ai`);

    return sections.join('\n\n');
  }
}

export const emailDrafter = new EmailDrafter();
