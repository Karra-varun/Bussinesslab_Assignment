/**
 * Express Server for Task 2: The Inbox Agent.
 * Runs on Port 8002.
 */
import express, { Request, Response } from 'express';
import cors from 'cors';
import path from 'path';
import dotenv from 'dotenv';

import { CustomerEmail, HumanActionType, EmailCategory } from './types';
import { SAMPLE_EMAILS } from './data/sampleEmails';
import { intentClassifier } from './agent/intentClassifier';
import { emailDrafter } from './agent/drafter';
import { learningEngine } from './agent/learningEngine';

dotenv.config();

const app = express();
const PORT = process.env.INBOX_PORT || 8002;

app.use(cors());
app.use(express.json());

// In-memory operational store for emails initialized from the 52 samples
const emailStore: Map<string, CustomerEmail> = new Map();

for (const email of SAMPLE_EMAILS) {
  // Re-classify intent dynamically
  const classifiedIntent = intentClassifier.classify(email);
  emailStore.set(email.id, {
    ...email,
    intent: classifiedIntent
  });
}

// Serve public static dashboard files
const publicDir = path.resolve(__dirname, '../public');
app.use(express.static(publicDir));

// API Routes

/**
 * Health check endpoint
 */
app.get('/api/health', (_req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    service: 'Inbox Agent (TypeScript)',
    totalEmails: emailStore.size,
    autonomyStatus: learningEngine.getAutonomyStatus()
  });
});

/**
 * List all emails with optional category and status filters
 */
app.get('/api/emails', (req: Request, res: Response) => {
  const { category, status } = req.query;
  let list = Array.from(emailStore.values());

  if (category) {
    list = list.filter((e) => e.intent.category === category);
  }
  if (status) {
    list = list.filter((e) => e.status === status);
  }

  res.json(list);
});

/**
 * Get individual email details
 */
app.get('/api/emails/:id', (req: Request, res: Response): void => {
  const emailId = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
  const email = emailStore.get(emailId);
  if (!email) {
    res.status(404).json({ error: 'Email not found' });
    return;
  }
  res.json(email);
});

/**
 * Generate or retrieve grounded draft for an email
 */
app.post('/api/emails/:id/draft', async (req: Request, res: Response): Promise<void> => {
  const emailId = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
  const email = emailStore.get(emailId);
  if (!email) {
    res.status(404).json({ error: 'Email not found' });
    return;
  }

  const draft = await emailDrafter.generateDraft(email);
  email.assignedDraft = draft;
  emailStore.set(email.id, email);

  res.json(draft);
});

/**
 * Record human action (SEND_AS_IS, EDIT_AND_SEND, WRITE_OWN)
 */
app.post('/api/emails/:id/action', (req: Request, res: Response): void => {
  const emailId = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
  const email = emailStore.get(emailId);
  if (!email) {
    res.status(404).json({ error: 'Email not found' });
    return;
  }

  const { action, finalSentText } = req.body as {
    action: HumanActionType;
    finalSentText?: string;
  };

  const originalDraft = email.assignedDraft?.body || '';
  const sentText = finalSentText || originalDraft;

  // Record feedback into learning engine & update streak
  const feedback = learningEngine.recordAction(
    email.id,
    email.intent.category,
    action,
    originalDraft,
    sentText
  );

  // Update email status
  if (action === 'SEND_AS_IS') {
    email.status = 'SENT_BY_HUMAN';
  } else if (action === 'EDIT_AND_SEND') {
    email.status = 'EDITED_AND_SENT';
  } else {
    email.status = 'REPLACED_BY_HUMAN';
  }

  emailStore.set(email.id, email);

  res.json({
    success: true,
    email,
    feedback,
    autonomyStatus: learningEngine.getAutonomyStatus().find((r) => r.category === email.intent.category)
  });
});

/**
 * Retrieve Autonomy rules and streak status
 */
app.get('/api/autonomy/status', (_req: Request, res: Response) => {
  res.json(learningEngine.getAutonomyStatus());
});

/**
 * Retrieve learned rules and feedback history
 */
app.get('/api/learnings', (_req: Request, res: Response) => {
  res.json({
    rules: learningEngine.getLearnedRules(),
    feedbacks: learningEngine.getFeedbackHistory()
  });
});

/**
 * Trip circuit breaker
 */
app.post('/api/autonomy/trip-circuit', (req: Request, res: Response) => {
  const { category, reason } = req.body as { category: EmailCategory; reason: string };
  const updatedRule = learningEngine.tripCircuitBreaker(category, reason || 'Manual circuit breaker triggered');
  res.json(updatedRule);
});

/**
 * Simulate 20 consecutive unedited sends to demonstrate autonomy unlocking
 */
app.post('/api/inbox/simulate-streak', (req: Request, res: Response) => {
  const { category } = req.body as { category: EmailCategory };
  const targetCategory: EmailCategory = category || 'HOW_TO';

  for (let i = 1; i <= 20; i++) {
    learningEngine.recordAction(
      `SIM-${i}`,
      targetCategory,
      'SEND_AS_IS',
      'Thank you for reaching out. Here is the verified setting: Go to Dashboard > Settings.',
      'Thank you for reaching out. Here is the verified setting: Go to Dashboard > Settings.'
    );
  }

  res.json({
    message: `Simulated 20 consecutive unedited sends for ${targetCategory}. Autonomy unlocked!`,
    rule: learningEngine.getAutonomyStatus().find((r) => r.category === targetCategory)
  });
});

// Serve frontend for all unmatched routes (Express 5 compliant)
app.use((_req: Request, res: Response) => {
  res.sendFile(path.join(publicDir, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`[Task 2 Inbox Agent] Server running on http://localhost:${PORT}`);
});
