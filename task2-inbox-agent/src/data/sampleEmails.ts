/**
 * Dataset of 52 Realistic Customer Emails across all core business categories.
 * Each email represents a real-world scenario encountered by a SaaS/software tech consultancy.
 */
import { CustomerEmail } from '../types';

export const SAMPLE_EMAILS: CustomerEmail[] = [
  // 1-10: Technical HOW_TO
  {
    id: 'EM-101',
    fromEmail: 'sarah.miller@vetdirectory.org',
    fromName: 'Dr. Sarah Miller',
    subject: 'Where can I update the social media icons on our homepage footer?',
    body: 'Hi team, We just rebranded our X handle and launched an Instagram page. Where do we plug in these social links in the admin area so they show in our footer and header? Thanks, Sarah',
    receivedAt: '2026-10-18T09:15:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'HOW_TO',
      subcategory: 'Social Media Settings',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Social Media Tab' }
    }
  },
  {
    id: 'EM-102',
    fromEmail: 'kevin.b@legalpros.com',
    fromName: 'Kevin Barnes',
    subject: 'Connecting Stripe test mode vs live mode',
    body: 'We are ready to connect our Stripe gateway to bill lawyers monthly. Where do we insert the Stripe live secret keys, and can we test with 4242 cards first?',
    receivedAt: '2026-10-18T09:30:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'HOW_TO',
      subcategory: 'Payment Gateway Setup',
      sentiment: 'NEUTRAL',
      urgency: 'HIGH',
      entities: { featureOrSetting: 'Stripe Gateway' }
    }
  },
  {
    id: 'EM-103',
    fromEmail: 'alyssa.wong@culinaryconnect.net',
    fromName: 'Alyssa Wong',
    subject: 'Need to import 1,200 restaurant categories via CSV',
    body: 'Hello, We have a spreadsheet of 1,200 cuisine types broken down by Top Level and Sub Level categories. How do we format the columns and upload this via CSV without breaking existing listings?',
    receivedAt: '2026-10-18T10:05:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'HOW_TO',
      subcategory: 'Category CSV Import',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Member Categories CSV' }
    }
  },
  {
    id: 'EM-104',
    fromEmail: 'marcus.t@austincontractors.io',
    fromName: 'Marcus Turner',
    subject: 'How does lead auto-match radius work?',
    body: 'When a homeowner enters a zip code for roofing, how does the system calculate which contractors get the lead? Can we limit it to a 25-mile radius?',
    receivedAt: '2026-10-18T10:45:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'HOW_TO',
      subcategory: 'Lead Routing Radius',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Lead Settings Radius' }
    }
  },
  {
    id: 'EM-105',
    fromEmail: 'rachel.adams@yogafinder.co',
    fromName: 'Rachel Adams',
    subject: 'Mass newsletter sending rate limit question',
    body: 'We want to email 3,500 registered yoga instructors about our upcoming virtual expo. Does the built-in newsletter tool send all at once or is it throttled per hour?',
    receivedAt: '2026-10-18T11:10:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'HOW_TO',
      subcategory: 'Mass Email Newsletter',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Send Newsletter tool' }
    }
  },
  {
    id: 'EM-106',
    fromEmail: 'diego.s@medmatch.es',
    fromName: 'Diego Sanchez',
    subject: 'Adding Accepting New Patients badge on search results',
    body: 'Can we add a filter checkbox so visitors can filter doctors by "Accepting New Patients"? Do we need custom coding or is there a form manager setting for this?',
    receivedAt: '2026-10-18T11:40:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'HOW_TO',
      subcategory: 'Search Filters',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Search Results Filters' }
    }
  },
  {
    id: 'EM-107',
    fromEmail: 'linda.k@therapynetwork.com',
    fromName: 'Linda Kowalski',
    subject: 'Outgoing webhook to HubSpot on new member signup',
    body: 'Whenever a therapist registers on our directory, we want their details pushed to HubSpot CRM. Where do we enter the webhook URL in the Developer Hub?',
    receivedAt: '2026-10-18T12:05:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'HOW_TO',
      subcategory: 'Webhooks Integration',
      sentiment: 'NEUTRAL',
      urgency: 'HIGH',
      entities: { featureOrSetting: 'Developer Hub Webhooks' }
    }
  },
  {
    id: 'EM-108',
    fromEmail: 'brian.g@dentalhub.ca',
    fromName: 'Brian Green',
    subject: 'Where to set primary currency to CAD instead of USD',
    body: 'Our directory operates exclusively in Canada. How do we change the currency symbol to CAD and adjust date formatting to DD/MM/YYYY?',
    receivedAt: '2026-10-18T12:30:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'HOW_TO',
      subcategory: 'Localization Settings',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'General Settings Localization' }
    }
  },
  {
    id: 'EM-109',
    fromEmail: 'fiona.m@weddingspotlight.co.uk',
    fromName: 'Fiona MacLeod',
    subject: 'SPF and DKIM records for custom email domain',
    body: 'Our welcome emails are landing in Gmail Spam. What SPF TXT record should we add to our DNS to verify Brilliant Directories mail servers?',
    receivedAt: '2026-10-18T13:00:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'HOW_TO',
      subcategory: 'DNS and Email Deliverability',
      sentiment: 'FRUSTRATED',
      urgency: 'HIGH',
      entities: { featureOrSetting: 'SPF DKIM Records' }
    }
  },
  {
    id: 'EM-110',
    fromEmail: 'tariq.a@dubairealestate.ae',
    fromName: 'Tariq Al-Mansoor',
    subject: 'Allowing members to cancel subscription from their dashboard',
    body: 'Is there a setting in membership plans to allow members to cancel their own recurring payments, or must an admin do it manually every time?',
    receivedAt: '2026-10-18T13:25:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'HOW_TO',
      subcategory: 'Member Cancellation Self-Service',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Membership Plan Cancellation Tab' }
    }
  },

  // 11-20: REFUND_CANCELLATION
  {
    id: 'EM-201',
    fromEmail: 'david.clark@apexfitness.com',
    fromName: 'David Clark',
    subject: 'Refund request: Charged annual fee accidentally',
    body: 'Hi, I signed up 4 days ago for the monthly plan but was charged $499 for the annual tier instead. I have not claimed any leads or added listings yet. Can I please get a full refund back to my card? Transaction ID: TXN_98124',
    receivedAt: '2026-10-18T13:50:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'REFUND_CANCELLATION',
      subcategory: 'Accidental Charge Refund',
      sentiment: 'FRUSTRATED',
      urgency: 'HIGH',
      entities: { transactionId: 'TXN_98124', urgencyReason: '4 days ago / within 30 days policy' }
    }
  },
  {
    id: 'EM-202',
    fromEmail: 'elizabeth.holt@holthealth.org',
    fromName: 'Elizabeth Holt',
    subject: 'Cancel our premium directory membership and refund current month',
    body: 'We are closing down our clinic location. Please cancel our recurring membership immediately and refund the $79 charged yesterday. Account email: elizabeth@holthealth.org.',
    receivedAt: '2026-10-18T14:15:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'REFUND_CANCELLATION',
      subcategory: 'Cancellation and Refund',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { membershipPlan: 'Premium Clinic Plan' }
    }
  },
  {
    id: 'EM-203',
    fromEmail: 'jason.reid@reidplumbing.com',
    fromName: 'Jason Reid',
    subject: 'Bogus lead charge - refund requested',
    body: 'I was charged $35 for an emergency plumbing lead yesterday, but the phone number provided is disconnected and the email bounced. Please refund this lead purchase.',
    receivedAt: '2026-10-18T14:40:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'REFUND_CANCELLATION',
      subcategory: 'Invalid Lead Refund',
      sentiment: 'FRUSTRATED',
      urgency: 'HIGH',
      entities: { transactionId: 'LEAD_CHARGE_441' }
    }
  },
  {
    id: 'EM-204',
    fromEmail: 'clara.b@petgroomers.com',
    fromName: 'Clara Bennett',
    subject: 'Cancel renewal notice',
    body: 'Hello, Our annual directory listing is set to renew in 2 weeks on Nov 1st. Please confirm our auto-renewal is turned off. We do not wish to be billed $299 again.',
    receivedAt: '2026-10-18T15:00:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'REFUND_CANCELLATION',
      subcategory: 'Auto-Renewal Opt-Out',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { membershipPlan: 'Annual Listing' }
    }
  },
  {
    id: 'EM-205',
    fromEmail: 'richard.v@techfoundry.io',
    fromName: 'Richard Vance',
    subject: 'Refund under 30-day guarantee',
    body: 'We tested the directory platform for 12 days and realized it does not fit our complex internal workflow. We are requesting a refund under your 30-day money-back guarantee.',
    receivedAt: '2026-10-18T15:20:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'REFUND_CANCELLATION',
      subcategory: '30-Day Money Back Guarantee',
      sentiment: 'NEUTRAL',
      urgency: 'HIGH',
      entities: { urgencyReason: '12 days in / eligible for 30-day guarantee' }
    }
  },
  {
    id: 'EM-206',
    fromEmail: 'samuel.w@buildright.co',
    fromName: 'Samuel Wright',
    subject: 'Double billed this morning',
    body: 'I noticed two charges of $99 on my credit card statement today for BuildRight Co. Can you please check Stripe and refund the duplicate charge?',
    receivedAt: '2026-10-18T15:45:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'REFUND_CANCELLATION',
      subcategory: 'Duplicate Billing',
      sentiment: 'FRUSTRATED',
      urgency: 'URGENT',
      entities: { urgencyReason: 'Duplicate transaction on credit card' }
    }
  },
  {
    id: 'EM-207',
    fromEmail: 'anna.schmidt@berlintours.de',
    fromName: 'Anna Schmidt',
    subject: 'Cancellation confirmation request',
    body: 'I pressed cancel in my dashboard yesterday. Could someone confirm that my Stripe subscription has actually been terminated and no further invoices will generate?',
    receivedAt: '2026-10-18T16:10:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'REFUND_CANCELLATION',
      subcategory: 'Cancellation Verification',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { membershipPlan: 'Pro Member' }
    }
  },
  {
    id: 'EM-208',
    fromEmail: 'greg.m@islandtours.org',
    fromName: 'Greg Mitchell',
    subject: 'Refund for annual renewal billed yesterday without notice',
    body: 'Our card was charged $590 for year 2 renewal yesterday. We hadn’t used the site in 4 months. As this was billed within the last 24 hours, can you please refund and cancel?',
    receivedAt: '2026-10-18T16:35:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'REFUND_CANCELLATION',
      subcategory: 'Annual Renewal Refund Request',
      sentiment: 'FRUSTRATED',
      urgency: 'HIGH',
      entities: { budget: '$590', urgencyReason: 'Billed 24 hours ago, eligible under 7-day annual policy' }
    }
  },
  {
    id: 'EM-209',
    fromEmail: 'patricia.k@cleaningservices.com',
    fromName: 'Patricia King',
    subject: 'Downgrade from Premium to Free tier instead of full cancel',
    body: 'Can you downgrade our account from the $49/mo Gold tier to the Free Community listing tier? Please refund the prorated difference for this month if possible.',
    receivedAt: '2026-10-18T17:00:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'REFUND_CANCELLATION',
      subcategory: 'Downgrade Plan',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { membershipPlan: 'Gold Tier -> Free Community' }
    }
  },
  {
    id: 'EM-210',
    fromEmail: 'ethan.p@mechanicfinder.net',
    fromName: 'Ethan Powell',
    subject: 'Chargeback dispute inquiry',
    body: 'Our accounting department noticed an unrecognized $120 charge from your company descriptor. Before we file a bank dispute, could you clarify what account this is attached to?',
    receivedAt: '2026-10-18T17:25:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'REFUND_CANCELLATION',
      subcategory: 'Chargeback Prevention',
      sentiment: 'NEGATIVE',
      urgency: 'URGENT',
      entities: { budget: '$120' }
    }
  },

  // 21-30: NEW_PROJECT
  {
    id: 'EM-301',
    fromEmail: 'dr.elena.vance@healthmatch.org',
    fromName: 'Dr. Elena Vance',
    subject: 'New Project: Medical Directory Platform with Telehealth Booking',
    body: 'Hello, We are launching HealthMatch, a directory of 5,000 certified pediatricians and therapists. We need doctor profiles, specialty search, clinic tiers, and telehealth scheduling links. Looking for a partner to build and configure this.',
    receivedAt: '2026-10-18T17:50:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'NEW_PROJECT',
      subcategory: 'Healthcare Directory Build',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Healthcare Directory + Telehealth', budget: '$5,000 - $10,000' }
    }
  },
  {
    id: 'EM-302',
    fromEmail: 'carlos.m@b2bwholesalers.com',
    fromName: 'Carlos Morales',
    subject: 'Request for Proposal: B2B Industrial Suppliers Marketplace',
    body: 'We want to migrate our existing static supplier list to an interactive B2B portal where suppliers can list product catalogs and receive direct quote inquiries. What is your process and timeline?',
    receivedAt: '2026-10-18T18:15:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'NEW_PROJECT',
      subcategory: 'B2B Marketplace Portal',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Product Catalogs and RFQ' }
    }
  },
  {
    id: 'EM-303',
    fromEmail: 'victoria.cross@luxurystays.travel',
    fromName: 'Victoria Cross',
    subject: 'Custom luxury boutique hotel booking directory',
    body: 'We are seeking an agency to build a high-end directory of boutique villas in the Mediterranean with video header, Instagram sync, and custom inquiry forms. Looking to launch by Q1.',
    receivedAt: '2026-10-18T18:40:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'NEW_PROJECT',
      subcategory: 'Travel Directory',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Boutique Directory + Video' }
    }
  },
  {
    id: 'EM-304',
    fromEmail: 'arjun.patel@evchargingnetwork.io',
    fromName: 'Arjun Patel',
    subject: 'Electric Vehicle Charger Station Locator App',
    body: 'We need a public directory of EV charging stations with interactive map clustering, filter by plug type (CCS, NACS), and user check-in reviews. Can Brilliant Directories handle this natively?',
    receivedAt: '2026-10-18T19:00:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'NEW_PROJECT',
      subcategory: 'EV Locator Directory',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Map Clustering + Plug Filters' }
    }
  },
  {
    id: 'EM-305',
    fromEmail: 'monica.lewis@nonprofitnetwork.org',
    fromName: 'Monica Lewis',
    subject: 'Community grant directory for local NGOs',
    body: 'We are a philanthropic foundation looking to create a centralized database where non-profits can search for grants and community sponsors. Need custom application submission forms.',
    receivedAt: '2026-10-18T19:25:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'NEW_PROJECT',
      subcategory: 'Nonprofit Grant Portal',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Grant Database + Forms' }
    }
  },
  {
    id: 'EM-306',
    fromEmail: 'simon.b@weddingphotographers.co',
    fromName: 'Simon Bell',
    subject: 'Photographer portfolio marketplace with lead routing',
    body: 'We need to set up a platform where wedding photographers can showcase photo albums and brides can request availability. We want pay-per-lead functionality enabled.',
    receivedAt: '2026-10-18T19:50:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'NEW_PROJECT',
      subcategory: 'Portfolio Directory',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Photo Galleries + Pay-Per-Lead' }
    }
  },
  {
    id: 'EM-307',
    fromEmail: 'yuki.tanaka@tokyocowork.jp',
    fromName: 'Yuki Tanaka',
    subject: 'Coworking space locator across Asia Pacific',
    body: 'We are expanding our coworking directory across Japan, Singapore, and Australia. Multi-currency and multi-language support are essential. What is your roadmap for such a project?',
    receivedAt: '2026-10-18T20:10:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'NEW_PROJECT',
      subcategory: 'International Directory',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Multi-Currency + Localization' }
    }
  },
  {
    id: 'EM-308',
    fromEmail: 'hannah.schmidt@craftbrewfinder.com',
    fromName: 'Hannah Schmidt',
    subject: 'Craft brewery directory with upcoming events and tours',
    body: 'Looking to launch CraftBrewFinder. Breweries should be able to post upcoming beer releases, taproom hours, and live music events on their profiles.',
    receivedAt: '2026-10-18T20:30:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'NEW_PROJECT',
      subcategory: 'Events & Listings Portal',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Events Post Type' }
    }
  },
  {
    id: 'EM-309',
    fromEmail: 'omar.farooq@halalrestaurants.co',
    fromName: 'Omar Farooq',
    subject: 'Certified halal dining guide with member reviews',
    body: 'We need a specialized directory for certified halal restaurants in North America with Google Maps integration, review moderation, and claiming listings.',
    receivedAt: '2026-10-18T20:55:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'NEW_PROJECT',
      subcategory: 'Claim Listings Directory',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Claim Listings + Google Maps' }
    }
  },
  {
    id: 'EM-310',
    fromEmail: 'brad.nelson@boatrentals.club',
    fromName: 'Brad Nelson',
    subject: 'Charter boat rental marketplace',
    body: 'Hi, We want to build a platform connecting yacht captains with charter customers. Can we manage security deposits and recurring captain dues on this system?',
    receivedAt: '2026-10-18T21:15:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'NEW_PROJECT',
      subcategory: 'Charter Marketplace',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Membership dues + Stripe' }
    }
  },

  // 31-40: QUOTE_REQUEST
  {
    id: 'EM-401',
    fromEmail: 'lucas.meyer@autoinspect.de',
    fromName: 'Lucas Meyer',
    subject: 'Quote: Custom API sync between Brilliant Directories and SAP',
    body: 'Could you provide an estimate for building a two-way sync between Brilliant Directories member database and our SAP ERP system using webhooks?',
    receivedAt: '2026-10-18T21:40:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'QUOTE_REQUEST',
      subcategory: 'Custom API Integration',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'SAP ERP Two-Way Sync', budget: 'Quote needed' }
    }
  },
  {
    id: 'EM-402',
    fromEmail: 'karen.w@chicagorealtors.org',
    fromName: 'Karen White',
    subject: 'Cost to add interactive radius search slider on homepage',
    body: 'We want a prominent radius distance slider (5 to 50 miles) right on our homepage hero banner. What would the developer cost and timeline be to implement this?',
    receivedAt: '2026-10-18T22:00:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'QUOTE_REQUEST',
      subcategory: 'UI Widget Customization',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Hero Radius Slider' }
    }
  },
  {
    id: 'EM-403',
    fromEmail: 'steve.j@cleantechfirms.com',
    fromName: 'Steve Jenkins',
    subject: 'Quote request: Turnkey directory setup and CSV formatting',
    body: 'We have 3,000 clean tech company listings in Excel. How much do you charge to configure our branding, set up 4 membership plans, and import the clean data?',
    receivedAt: '2026-10-18T22:20:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'QUOTE_REQUEST',
      subcategory: 'Turnkey Setup & Data Import',
      sentiment: 'NEUTRAL',
      urgency: 'HIGH',
      entities: { budget: 'Full setup quote' }
    }
  },
  {
    id: 'EM-404',
    fromEmail: 'valerie.t@weddingvendors.ca',
    fromName: 'Valerie Tremblay',
    subject: 'Estimate for custom mobile app wrapper',
    body: 'Does your team build React Native or iOS wrappers for Brilliant Directories? We want our members to receive push notifications on new leads. Please provide a rough price range.',
    receivedAt: '2026-10-18T22:45:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'QUOTE_REQUEST',
      subcategory: 'Mobile App Wrapper',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Push Notifications + Mobile App' }
    }
  },
  {
    id: 'EM-405',
    fromEmail: 'marcus.h@tradepros.com.au',
    fromName: 'Marcus Hughes',
    subject: 'Hourly development rate for custom PHP/JS widgets',
    body: 'We need periodic ad-hoc modifications to our directory theme (custom member card layouts, badge icons). What is your hourly consulting rate and minimum commitment?',
    receivedAt: '2026-10-18T23:05:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'QUOTE_REQUEST',
      subcategory: 'Hourly Consulting Rates',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Custom Widget Dev' }
    }
  },
  {
    id: 'EM-406',
    fromEmail: 'olivia.p@psychiatrynetwork.org',
    fromName: 'Olivia Perez',
    subject: 'HIPAA compliance audit and consultation quote',
    body: 'We are storing intake notes for patients contacting mental health specialists. Can you quote an architecture review to ensure we handle data in compliance with HIPAA guidelines?',
    receivedAt: '2026-10-18T23:30:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'QUOTE_REQUEST',
      subcategory: 'Compliance Audit',
      sentiment: 'NEUTRAL',
      urgency: 'HIGH',
      entities: { featureOrSetting: 'HIPAA Compliance' }
    }
  },
  {
    id: 'EM-407',
    fromEmail: 'tom.bradley@veteranowned.biz',
    fromName: 'Tom Bradley',
    subject: 'Quote for custom verification badge verification workflow',
    body: 'We need to verify veteran-owned business licenses before granting a gold badge. How much would it cost to build a custom document upload and admin approval tab?',
    receivedAt: '2026-10-18T23:55:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'QUOTE_REQUEST',
      subcategory: 'Custom Verification Workflow',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Document Upload + Badge' }
    }
  },
  {
    id: 'EM-408',
    fromEmail: 'natalie.r@greenenergyinstallers.com',
    fromName: 'Natalie Ross',
    subject: 'Cost to integrate Google Tag Manager and GA4 e-commerce',
    body: 'Can you provide a price to hook up GA4 e-commerce tracking on our membership checkout pages and lead purchase buttons?',
    receivedAt: '2026-10-19T00:20:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'QUOTE_REQUEST',
      subcategory: 'Analytics Integration',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'GA4 eCommerce Tracking' }
    }
  },
  {
    id: 'EM-409',
    fromEmail: 'charlie.d@foodtruckfinder.org',
    fromName: 'Charlie Davis',
    subject: 'Quote for live GPS location tracking for food trucks',
    body: 'Food trucks move every day. Can we quote building a mobile check-in feature where truck owners press a button on their phone to update their map pin instantly?',
    receivedAt: '2026-10-19T00:45:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'QUOTE_REQUEST',
      subcategory: 'Live GPS Pin Update',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'GPS Geolocation Pin' }
    }
  },
  {
    id: 'EM-410',
    fromEmail: 'laura.k@daycaresdirectory.net',
    fromName: 'Laura Kim',
    subject: 'Pricing for speed optimization and Core Web Vitals audit',
    body: 'Our homepage Largest Contentful Paint is 4.8 seconds on mobile. How much would it cost to optimize images, defer scripts, and get us to a 90+ PageSpeed score?',
    receivedAt: '2026-10-19T01:10:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'QUOTE_REQUEST',
      subcategory: 'Performance Optimization',
      sentiment: 'NEUTRAL',
      urgency: 'HIGH',
      entities: { featureOrSetting: 'PageSpeed LCP Optimization' }
    }
  },

  // 41-46: COMPLAINT_OUTAGE
  {
    id: 'EM-501',
    fromEmail: 'mark.stevens@dentistsnearme.com',
    fromName: 'Mark Stevens',
    subject: 'URGENT: Sign up page throwing 500 error on checkout',
    body: 'Our paid membership signup page has been throwing a 500 internal server error for the last 2 hours. Prospective dentists cannot complete payment. Please investigate immediately!',
    receivedAt: '2026-10-19T01:30:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'COMPLAINT_OUTAGE',
      subcategory: 'Checkout 500 Error',
      sentiment: 'FRUSTRATED',
      urgency: 'URGENT',
      entities: { urgencyReason: 'Signup page down, loss of revenue' }
    }
  },
  {
    id: 'EM-502',
    fromEmail: 'sandra.c@homeinspectors.org',
    fromName: 'Sandra Collins',
    subject: 'Google Maps showing "For Development Purposes Only" watermark',
    body: 'All the maps on our member profile pages have dark gray tiles with a watermarked error saying Google Maps is in development mode. Our members are complaining. How do we fix this?',
    receivedAt: '2026-10-19T01:50:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'COMPLAINT_OUTAGE',
      subcategory: 'Google Maps API Error',
      sentiment: 'FRUSTRATED',
      urgency: 'HIGH',
      entities: { featureOrSetting: 'Google Maps API Key' }
    }
  },
  {
    id: 'EM-503',
    fromEmail: 'gary.b@autotowing247.com',
    fromName: 'Gary Brooks',
    subject: 'Lead notification emails delayed by 4 hours',
    body: 'Emergency towing leads sent by customers at 8 AM were delivered to our drivers at noon. This lag is completely unacceptable for an on-demand towing business. What is going on?',
    receivedAt: '2026-10-19T02:15:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'COMPLAINT_OUTAGE',
      subcategory: 'Email Notification Delay',
      sentiment: 'NEGATIVE',
      urgency: 'URGENT',
      entities: { urgencyReason: '4 hour email delay for emergency leads' }
    }
  },
  {
    id: 'EM-504',
    fromEmail: 'jessica.m@coachesregistry.org',
    fromName: 'Jessica Murphy',
    subject: 'Member profile pictures showing broken image icons',
    body: 'Several of our life coaches reported that their profile avatar shows a broken image box after they uploaded JPEGs yesterday. Is there an issue with the media uploads folder?',
    receivedAt: '2026-10-19T02:40:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'COMPLAINT_OUTAGE',
      subcategory: 'Media Upload Issue',
      sentiment: 'FRUSTRATED',
      urgency: 'HIGH',
      entities: { featureOrSetting: 'Profile Photo Upload' }
    }
  },
  {
    id: 'EM-505',
    fromEmail: 'tony.ramirez@hvacspecialists.net',
    fromName: 'Tony Ramirez',
    subject: 'Search results page infinite loading spinner',
    body: 'When users search for zip codes in Florida, the page spins indefinitely and never displays matching contractors. Mobile users cannot use the site at all.',
    receivedAt: '2026-10-19T03:00:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'COMPLAINT_OUTAGE',
      subcategory: 'Search Page Infinite Spinner',
      sentiment: 'NEGATIVE',
      urgency: 'URGENT',
      entities: { urgencyReason: 'Search broken for zip codes' }
    }
  },
  {
    id: 'EM-506',
    fromEmail: 'melissa.w@tutorsclub.edu',
    fromName: 'Melissa Watson',
    subject: 'SSL Certificate expired warning for visitors',
    body: 'Chrome is blocking our site with an "Your connection is not private" warning because our SSL expired at midnight. Please renew the certificate right now!',
    receivedAt: '2026-10-19T03:20:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'COMPLAINT_OUTAGE',
      subcategory: 'SSL Expiration Outage',
      sentiment: 'NEGATIVE',
      urgency: 'URGENT',
      entities: { urgencyReason: 'SSL Certificate Expired' }
    }
  },

  // 47-52: FOLLOW_UP
  {
    id: 'EM-601',
    fromEmail: 'arthur.pendleton@antiqueconnoisseur.com',
    fromName: 'Arthur Pendleton',
    subject: 'Status of custom search filter update (Ticket #4092)',
    body: 'Hi, Just checking in on ticket #4092 from last Thursday regarding the antique era dropdown filter. Was the staging site updated for us to test?',
    receivedAt: '2026-10-19T03:40:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'FOLLOW_UP',
      subcategory: 'Ticket Status Check',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Ticket #4092 Staging Update' }
    }
  },
  {
    id: 'EM-602',
    fromEmail: 'miranda.frost@arcticadventures.is',
    fromName: 'Miranda Frost',
    subject: 'Following up on invoice #INV-2041 payment',
    body: 'We sent wire payment for milestone 2 of the Arctic Adventures directory project on Monday. Could you please confirm receipt and let us know when sprint 2 begins?',
    receivedAt: '2026-10-19T04:00:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'FOLLOW_UP',
      subcategory: 'Payment & Milestone Confirmation',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { transactionId: 'INV-2041' }
    }
  },
  {
    id: 'EM-603',
    fromEmail: 'derek.stone@rockymountainhomes.com',
    fromName: 'Derek Stone',
    subject: 'Review of staging homepage color palette',
    body: 'We looked at the staging site preview. The navy blue header looks fantastic! We just want to make the phone number in the top right slightly bolder. Ready to push live once that is done.',
    receivedAt: '2026-10-19T04:20:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'FOLLOW_UP',
      subcategory: 'Staging Review Approval',
      sentiment: 'POSITIVE',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Staging Approval' }
    }
  },
  {
    id: 'EM-604',
    fromEmail: 'chloe.dupont@parisparfums.fr',
    fromName: 'Chloe Dupont',
    subject: 'DNS nameservers propagation update',
    body: 'We switched our nameservers to Brilliant Directories 18 hours ago as requested. Has the domain resolved on your end so we can link the live SSL certificate?',
    receivedAt: '2026-10-19T04:40:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'FOLLOW_UP',
      subcategory: 'DNS Nameservers Propagation',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Nameservers & SSL' }
    }
  },
  {
    id: 'EM-605',
    fromEmail: 'brandon.cole@floridapoolpros.com',
    fromName: 'Brandon Cole',
    subject: 'Checking on our Stripe webhook test verification',
    body: 'Did the test customer subscription webhook ping succeed on your staging dashboard yesterday? Let us know if we need to resend the payload from Stripe.',
    receivedAt: '2026-10-19T05:00:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'FOLLOW_UP',
      subcategory: 'Webhook Test Verification',
      sentiment: 'NEUTRAL',
      urgency: 'NORMAL',
      entities: { featureOrSetting: 'Stripe Webhook Ping' }
    }
  },
  {
    id: 'EM-606',
    fromEmail: 'nadia.petrova@wellnessguides.org',
    fromName: 'Nadia Petrova',
    subject: 'Final sign-off on Q3 directory maintenance',
    body: 'All reported bugs from Q3 seem resolved. Thank you for the quick turnaround this week. Please send through the final monthly timesheet for our records.',
    receivedAt: '2026-10-19T05:20:00Z',
    status: 'PENDING_REVIEW',
    intent: {
      category: 'FOLLOW_UP',
      subcategory: 'Sign-off & Monthly Timesheet',
      sentiment: 'POSITIVE',
      urgency: 'LOW',
      entities: { featureOrSetting: 'Monthly Timesheet' }
    }
  }
];
