/**
 * Intent Classifier and Triage Engine for Customer Emails.
 * Classifies categories, urgency, sentiment, and extracts operational entities.
 */
import { CustomerEmail, EmailIntent, EmailCategory, EmailUrgency } from '../types';

export class IntentClassifier {
  /**
   * Classifies email intent and operational priorities.
   */
  classify(email: Partial<CustomerEmail>): EmailIntent {
    const text = `${email.subject || ''} ${email.body || ''}`.toLowerCase();

    let category: EmailCategory = 'HOW_TO';
    let subcategory = 'General Inquiries';
    let urgency: EmailUrgency = 'NORMAL';
    let sentiment: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE' | 'FRUSTRATED' = 'NEUTRAL';

    // 1. Complaint / Outage detection
    if (
      text.includes('500') ||
      text.includes('error') ||
      text.includes('broken') ||
      text.includes('expired') ||
      text.includes('urgent') ||
      text.includes('down') ||
      text.includes('infinite loading') ||
      text.includes('not private')
    ) {
      category = 'COMPLAINT_OUTAGE';
      subcategory = 'System Issue';
      urgency = 'URGENT';
      sentiment = 'FRUSTRATED';
    }
    // 2. Refund / Cancellation
    else if (
      text.includes('refund') ||
      text.includes('cancel') ||
      text.includes('cancellation') ||
      text.includes('chargeback') ||
      text.includes('double billed') ||
      text.includes('dispute')
    ) {
      category = 'REFUND_CANCELLATION';
      subcategory = 'Billing Policy & Refunds';
      urgency = text.includes('chargeback') || text.includes('double') ? 'URGENT' : 'HIGH';
      sentiment = text.includes('dispute') ? 'NEGATIVE' : 'NEUTRAL';
    }
    // 3. New Project Request
    else if (
      text.includes('new project') ||
      text.includes('request for proposal') ||
      text.includes('rfp') ||
      text.includes('launching') ||
      text.includes('seeking an agency') ||
      text.includes('build a platform') ||
      text.includes('marketplace')
    ) {
      category = 'NEW_PROJECT';
      subcategory = 'New Directory Build';
      urgency = 'NORMAL';
      sentiment = 'POSITIVE';
    }
    // 4. Quote Request
    else if (
      text.includes('quote') ||
      text.includes('estimate') ||
      text.includes('how much do you charge') ||
      text.includes('hourly rate') ||
      text.includes('pricing') ||
      text.includes('cost to')
    ) {
      category = 'QUOTE_REQUEST';
      subcategory = 'Development Estimate';
      urgency = 'NORMAL';
      sentiment = 'POSITIVE';
    }
    // 5. Follow Up
    else if (
      text.includes('following up') ||
      text.includes('checking in') ||
      text.includes('ticket #') ||
      text.includes('status of') ||
      text.includes('staging site') ||
      text.includes('nameservers') ||
      text.includes('timesheet')
    ) {
      category = 'FOLLOW_UP';
      subcategory = 'Status & Milestones';
      urgency = 'NORMAL';
      sentiment = 'POSITIVE';
    }
    // 6. How To
    else {
      category = 'HOW_TO';
      subcategory = 'Settings & Documentation';
      urgency = 'NORMAL';
      sentiment = 'NEUTRAL';
    }

    // Extract basic entities
    const txnMatch = text.match(/\b(txn_[0-9]+|inv-[0-9]+|lead_charge_[0-9]+|ticket\s*#[0-9]+)\b/i);
    const budgetMatch = text.match(/\$[0-9]+(,[0-9]+)?/);

    return {
      category,
      subcategory,
      sentiment,
      urgency,
      entities: {
        transactionId: txnMatch ? txnMatch[0].toUpperCase() : undefined,
        budget: budgetMatch ? budgetMatch[0] : undefined
      }
    };
  }
}

export const intentClassifier = new IntentClassifier();
