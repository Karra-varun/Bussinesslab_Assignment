/**
 * Strict TypeScript Type Definitions for Task 2: The Inbox Agent.
 */

export type EmailCategory =
  | 'HOW_TO'
  | 'REFUND_CANCELLATION'
  | 'NEW_PROJECT'
  | 'QUOTE_REQUEST'
  | 'COMPLAINT_OUTAGE'
  | 'FOLLOW_UP';

export type EmailUrgency = 'LOW' | 'NORMAL' | 'HIGH' | 'URGENT';

export type EmailStatus =
  | 'PENDING_REVIEW'
  | 'SENT_BY_HUMAN'
  | 'EDITED_AND_SENT'
  | 'REPLACED_BY_HUMAN'
  | 'AUTONOMOUSLY_SENT';

export interface EmailIntent {
  category: EmailCategory;
  subcategory: string;
  sentiment: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE' | 'FRUSTRATED';
  urgency: EmailUrgency;
  entities: {
    featureOrSetting?: string;
    membershipPlan?: string;
    transactionId?: string;
    budget?: string;
    urgencyReason?: string;
  };
}

export interface CustomerEmail {
  id: string;
  fromEmail: string;
  fromName: string;
  subject: string;
  body: string;
  receivedAt: string;
  status: EmailStatus;
  intent: EmailIntent;
  assignedDraft?: DraftReply;
}

export interface KBCitation {
  article_id: string;
  title: string;
  url: string;
  category: string;
  folder: string;
  snippet: string;
  screenshot_url?: string;
  screenshot_caption?: string;
  relevance_score: number;
}

export interface KBQueryResponse {
  query: string;
  answer: string;
  citations: KBCitation[];
  confidence: number;
  is_fallback: boolean;
  fallback_reason?: string;
  human_ticket_id?: string;
  latency_ms: number;
  model_used: string;
}

export interface DraftReply {
  emailId: string;
  subject: string;
  body: string;
  citations: KBCitation[];
  reasoning: string;
  confidenceScore: number;
  appliedLearnedRules: string[];
  generatedAt: string;
  canAutoSend: boolean;
}

export type HumanActionType = 'SEND_AS_IS' | 'EDIT_AND_SEND' | 'WRITE_OWN';

export interface HumanFeedback {
  emailId: string;
  category: EmailCategory;
  action: HumanActionType;
  originalDraft: string;
  finalSentText: string;
  similarityRatio: number;
  isUnchanged: boolean;
  extractedLearning?: string;
  timestamp: string;
}

export interface AutonomyRule {
  category: EmailCategory;
  streakCount: number;
  threshold: number; // 20
  isAutonomous: boolean;
  circuitBreakerTripped: boolean;
  tripReason?: string;
  totalSentAutonomously: number;
  lastUpdated: string;
}

export interface LearningRule {
  id: string;
  category: EmailCategory;
  ruleText: string;
  sourceEmailId: string;
  createdAt: string;
  weight: number;
}
