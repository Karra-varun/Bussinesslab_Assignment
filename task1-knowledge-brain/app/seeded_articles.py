"""
Seeded high-fidelity knowledge base articles from the Brilliant Directories Solution Center.
Covers real categories: General Settings, Finance & Payments, Members & Listings,
Leads System, Design & Theme, Email System, Developer Webhooks, and Business Policies.
Includes multimodal screenshot metadata and UI navigation breadcrumbs.
"""
from typing import List
from app.models import Article, ImageMetadata

SEEDED_ARTICLES: List[Article] = [
    Article(
        id="5000558389",
        url="https://support.brilliantdirectories.com/support/solutions/articles/5000558389-settings-general-settings-social-media-tab",
        title="Settings: General Settings - Social Media Tab",
        category="Settings",
        folder="General Settings",
        breadcrumbs=["Solutions", "Settings", "General Settings", "Social Media Tab"],
        content_text="""The Social Media tab in General Settings allows directory administrators to link their social media profiles and configure social sharing defaults.
To navigate here: Log in to the Admin Dashboard > Go to Settings > General Settings > Click the 'Social Media' tab.
Configurable fields include:
1. Facebook Page URL and Facebook App ID (for OAuth login and social feed embedding).
2. X / Twitter Profile URL and Twitter Card default image.
3. LinkedIn Company URL.
4. Instagram Profile URL.
5. YouTube Channel URL.
6. Open Graph Meta Image: Upload a default 1200x630px image that displays when links to your directory are shared on messaging apps and social media.
Tip: Enabling Social Login (Facebook/Google) requires adding API keys in Settings > General Settings > Integrations tab, not the Social Media tab.""",
        screenshots=[
            ImageMetadata(
                url="https://support.brilliantdirectories.com/images/general-settings-social-media.png",
                alt="Brilliant Directories General Settings Social Media Tab Screenshot",
                caption="General Settings interface displaying social media profile URLs and Open Graph default image upload box.",
                ocr_text="Admin > Settings > General Settings > Social Media | Facebook URL | Twitter/X URL | LinkedIn URL | Default Share Image",
                ui_context="Settings > General Settings > Social Media tab",
                article_id="5000558389"
            )
        ],
        last_modified="2026-10-18T08:00:54+00:00",
        content_hash="hash_5000558389"
    ),
    Article(
        id="5000558357",
        url="https://support.brilliantdirectories.com/support/solutions/articles/5000558357-can-i-send-a-mass-email-campaign-using-brilliant-directories-",
        title="Can I Send a Mass Email Campaign Using Brilliant Directories?",
        category="Emails",
        folder="Email Marketing",
        breadcrumbs=["Solutions", "Emails", "Email Marketing", "Mass Email Campaigns"],
        content_text="""Yes, Brilliant Directories includes a built-in Email Marketing Newsletter tool to broadcast emails to members and newsletter subscribers.
Navigation: Dashboard > Emails > Send Newsletter.
Key Features and Limits:
1. Recipient Filtering: Filter by Membership Plan, Member Status (Active, Pending, Cancelled), or Newsletter Subscriber list.
2. Email Templates: Select pre-designed responsive newsletter templates or build custom HTML templates in Emails > Email Templates.
3. Sending Limits: Default server sending rate is throttled to 250 emails/hour to maintain high domain sender reputation and prevent IP blacklisting.
4. Third-Party SMTP: For sending high volumes (>5,000 emails/month), connecting an external SMTP provider like SendGrid, Mailgun, or Amazon SES is recommended under Settings > General Settings > Integrations.
Unsubscribe Handling: Every email sent automatically appends an RFC-compliant unsubscribe link linked to the member profile preferences.""",
        screenshots=[
            ImageMetadata(
                url="https://support.brilliantdirectories.com/images/send-newsletter-tool.png",
                alt="Send Newsletter interface showing recipient filter dropdown and template picker",
                caption="Email Marketing dashboard with recipient segmentation filters and scheduling options.",
                ocr_text="Emails > Send Newsletter | Step 1: Select Recipients | Step 2: Choose Template | Step 3: Review & Schedule",
                ui_context="Emails > Send Newsletter wizard",
                article_id="5000558357"
            )
        ],
        last_modified="2026-10-18T08:00:54+00:00",
        content_hash="hash_5000558357"
    ),
    Article(
        id="5000558363",
        url="https://support.brilliantdirectories.com/support/solutions/articles/5000558363-emails-email-accounts",
        title="Emails: Setting Up Email Accounts and MX Records",
        category="Emails",
        folder="Email Configuration",
        breadcrumbs=["Solutions", "Emails", "Email Accounts", "Configuration"],
        content_text="""Configuring branded custom email accounts (e.g., info@yourdirectory.com, support@yourdirectory.com).
Navigation: Dashboard > Emails > Email Accounts.
Options:
1. Native CPanel Webmail: Create mailboxes directly on the server with POP3/IMAP credentials.
2. Google Workspace / Microsoft 365: Recommended for professional deliverability. To route mail externally, update MX Records under Developer Hub > DNS Records.
3. SPF and DKIM Records: Always verify SPF TXT records (`v=spf1 include:brilliantdirectories.com ~all`) to prevent emails from ending in client spam folders.""",
        screenshots=[
            ImageMetadata(
                url="https://support.brilliantdirectories.com/images/email-accounts-dns.png",
                alt="Email Accounts configuration panel",
                caption="DNS MX record and SPF configuration screen.",
                ocr_text="Emails > Email Accounts | Add Mailbox | DNS Status: Verified",
                ui_context="Emails > Email Accounts",
                article_id="5000558363"
            )
        ],
        last_modified="2026-10-18T08:00:54+00:00",
        content_hash="hash_5000558363"
    ),
    Article(
        id="5000558401",
        url="https://support.brilliantdirectories.com/support/solutions/articles/5000558401-how-to-import-categories-via-csv-file",
        title="How to Import Member Categories via CSV File",
        category="Members",
        folder="Categories & Classifications",
        breadcrumbs=["Solutions", "Members", "Categories", "CSV Import"],
        content_text="""To bulk import Top-Level, Sub-Level, and Sub-Sub Categories into your directory:
Navigation: Dashboard > My Members > Member Categories > Click 'Import Categories' button.
CSV Formatting Rules:
- Column A: Top Category Name
- Column B: Sub Category Name (Parent must match Column A)
- Column C: Sub-Sub Category Name (Parent must match Column B)
- Column D: Clean URL Slug (Optional, auto-generated if left blank)
Max File Size: 10MB CSV UTF-8 formatted.
Important: Always perform a database backup under Developer Hub > Backups prior to large category imports to enable instant restoration if hierarchy columns are misaligned.""",
        screenshots=[
            ImageMetadata(
                url="https://support.brilliantdirectories.com/images/import-categories-csv.png",
                alt="Member categories import dialog with file upload and sample template link",
                caption="Import Categories modal with CSV mapping and duplicate detection switches.",
                ocr_text="My Members > Member Categories > Import | Upload CSV | Match Columns | Overwrite Existing: NO",
                ui_context="My Members > Member Categories > Import modal",
                article_id="5000558401"
            )
        ],
        last_modified="2026-10-18T08:00:54+00:00",
        content_hash="hash_5000558401"
    ),
    Article(
        id="5000558415",
        url="https://support.brilliantdirectories.com/support/solutions/articles/5000558415-connecting-stripe-payment-gateway",
        title="Connecting Stripe Payment Gateway for Subscriptions & One-Time Payments",
        category="Finance",
        folder="Payment Gateways",
        breadcrumbs=["Solutions", "Finance", "Payment Gateways", "Stripe Setup"],
        content_text="""Brilliant Directories integrates natively with Stripe for automated credit card billing, recurring subscription plans, and paid lead purchases.
Navigation: Dashboard > Finance > Payment Gateways > Select 'Stripe'.
Setup Steps:
1. Click 'Connect with Stripe' to authenticate via Stripe OAuth or enter your Stripe Publishable Key and Secret Key manually.
2. Webhook Configuration: Copy the Brilliant Directories Webhook Endpoint URL into your Stripe Dashboard (Developers > Webhooks). Listen for events: `customer.subscription.deleted`, `invoice.payment_succeeded`, `invoice.payment_failed`.
3. Supported Currencies: Set your primary currency in Settings > General Settings > Localization. Stripe will bill transactions in this designated currency.
3D Secure (SCA): Natively supported for European and international credit cards.
Test Mode: Toggle 'Enable Test Mode' to simulate signups using 4242 test cards before launching live.""",
        screenshots=[
            ImageMetadata(
                url="https://support.brilliantdirectories.com/images/stripe-gateway-settings.png",
                alt="Payment Gateway settings screen showing Stripe Connect button and webhook status",
                caption="Finance Payment Gateways page with Stripe live/test toggles and webhook signing secret input.",
                ocr_text="Finance > Payment Gateways > Stripe | Status: Active | Live Secret Key: sk_live_*** | Test Mode: OFF",
                ui_context="Finance > Payment Gateways > Stripe tab",
                article_id="5000558415"
            )
        ],
        last_modified="2026-10-18T08:00:54+00:00",
        content_hash="hash_5000558415"
    ),
    Article(
        id="5000558422",
        url="https://support.brilliantdirectories.com/support/solutions/articles/5000558422-how-to-process-refunds-and-handle-cancellations",
        title="How to Process Refunds and Handle Member Cancellations",
        category="Finance",
        folder="Billing & Policy",
        breadcrumbs=["Solutions", "Finance", "Billing", "Refunds & Cancellations"],
        content_text="""Refund Processing Workflow:
Refunds for member subscriptions or lead purchases must be initiated directly within your connected Payment Gateway (Stripe or PayPal account).
Steps to issue refund:
1. Log into your Stripe account > Search for the member's transaction > Click 'Refund'.
2. Inside Brilliant Directories: Go to Finance > Transaction History > Find the transaction > Click 'Mark as Refunded' to update directory reporting logs. Note: The directory does not deduct funds directly from your bank; gateway handles funds transfer.

Member Cancellation Settings:
Navigation: Dashboard > Finance > Membership Plans > Select Plan > 'Sign Up Page' / 'Cancellation' tab.
Admin controls:
- Allow Members to Cancel from Dashboard: YES / NO toggle.
- When Cancelled: Immediately change member status to 'Cancelled' or allow access until end of current billing cycle.
- Retention Offer / Exit Survey: Present a discount offer or cancellation survey prompt before final account deactivation.

Standard Company Policy:
Refund requests within 30 days of initial signup are honored with full refund upon request if no leads were claimed. Annual renewals require request within 7 business days of billing date.""",
        screenshots=[
            ImageMetadata(
                url="https://support.brilliantdirectories.com/images/membership-plan-cancellation.png",
                alt="Membership plan cancellation settings screen",
                caption="Cancellation settings tab under Membership Plans showing member self-service cancel toggle.",
                ocr_text="Finance > Membership Plans > Edit Plan > Cancellation Tab | Allow Member Cancellation: YES | Grace Period: 3 Days",
                ui_context="Finance > Membership Plans > Cancellation Settings",
                article_id="5000558422"
            )
        ],
        last_modified="2026-10-18T08:00:54+00:00",
        content_hash="hash_5000558422"
    ),
    Article(
        id="5000558430",
        url="https://support.brilliantdirectories.com/support/solutions/articles/5000558430-lead-system-auto-matching-and-lead-pricing",
        title="Lead System: Auto-Matching, Lead Routing, and Lead Pricing",
        category="Leads",
        folder="Lead Management",
        breadcrumbs=["Solutions", "Leads", "Lead Settings", "Auto-Matching"],
        content_text="""The Lead Generation system routes visitor inquiries to relevant professionals based on location and specialty.
Navigation: Dashboard > Leads > Lead Settings.
Matching Logic:
1. Auto-Match vs Manual Review:
   - Auto-Match (Instant): As soon as a visitor submits the 'Get a Quote' or 'Book Appointment' form, the system automatically emails matched members.
   - Manual Review: Holds leads in 'Pending Admin Review' queue (Leads > Manage Leads) before admin approves and dispatches.
2. Radius Matching: Set default search radius (e.g. 25 miles / 50 km) from visitor zip/postal code.
3. Pricing Models:
   - Free for Premium Members: Membership plans can include free lead access (Finance > Membership Plans > Edit Plan > Leads tab).
   - Pay-Per-Lead: Charge members $10-$50 to accept and view visitor contact information (requires Stripe gateway).
4. Direct Inquiries vs General Leads: Direct inquiries submitted on a doctor or business profile page can be set to route exclusively to that member or additionally match competing local members.""",
        screenshots=[
            ImageMetadata(
                url="https://support.brilliantdirectories.com/images/lead-settings-automatch.png",
                alt="Lead auto-match settings panel",
                caption="Lead Settings control panel showing auto-dispatch toggles and radius match slider.",
                ocr_text="Leads > Lead Settings | Auto-Match Leads: ENABLED | Match Radius: 25 Miles | Max Member Matches: 3",
                ui_context="Leads > Lead Settings tab",
                article_id="5000558430"
            )
        ],
        last_modified="2026-10-18T08:00:54+00:00",
        content_hash="hash_5000558430"
    ),
    Article(
        id="5000558445",
        url="https://support.brilliantdirectories.com/support/solutions/articles/5000558445-member-search-results-and-radius-search-settings",
        title="Member Search Results: Radius Filtering, Sorting, and Map Pins",
        category="Settings",
        folder="Search Settings",
        breadcrumbs=["Solutions", "Settings", "General Settings", "Search Settings"],
        content_text="""Configuring how visitors search for and discover directory listings.
Navigation: Dashboard > Settings > General Settings > Search Settings.
Key Configurations:
1. Default Sort Order: Top-tier membership plans first, followed by alphabetical or distance.
2. Radius Distance Unit: Miles or Kilometers (Settings > General Settings > Localization).
3. Google Maps API Integration: Paste your Google Maps JavaScript and Geocoding API keys under Settings > General Settings > Integrations.
4. Custom Search Filters: Display specialty dropdowns, accepting new patients checkboxes, language spoken, and price ranges.
Notice: Adding a new custom search filter (e.g. 'Accepting New Patients') does NOT require custom coding; it is configured via the Form Manager under Toolbox > Form Manager > Listing - Search Results form.""",
        screenshots=[
            ImageMetadata(
                url="https://support.brilliantdirectories.com/images/search-results-settings.png",
                alt="Search results configuration page with sorting dropdowns",
                caption="Search Settings panel showing default sort order, map pin cluster toggles, and radius bounds.",
                ocr_text="Settings > General Settings > Search Settings | Default Sort: Highest Tier First | Radius Search: Enabled | Google Map Clustering: ON",
                ui_context="Settings > General Settings > Search Settings",
                article_id="5000558445"
            )
        ],
        last_modified="2026-10-18T08:00:54+00:00",
        content_hash="hash_5000558445"
    ),
    Article(
        id="5000558460",
        url="https://support.brilliantdirectories.com/support/solutions/articles/5000558460-webhooks-and-api-integrations",
        title="Developer Hub: Webhooks, REST API, and Zapier Integration",
        category="Developer",
        folder="API & Webhooks",
        breadcrumbs=["Solutions", "Developer Hub", "API", "Webhooks"],
        content_text="""Integrate Brilliant Directories with external CRM systems (HubSpot, Salesforce, HighLevel) or automate workflows via Webhooks.
Navigation: Dashboard > Developer Hub > Webhooks / API.
Available Webhook Events:
1. `member.signup`: Fires when a new user registers or pays for a plan.
2. `member.updated`: Fires when profile details or status changes.
3. `member.cancelled`: Fires on cancellation.
4. `lead.created`: Fires when visitor submits an inquiry.
Payload Structure: Standard JSON containing member ID, email, name, membership plan ID, and custom form field data.
API Authentication: Generate Bearer API Keys under Developer Hub > API Keys. Standard rate limit is 60 requests/minute per key.""",
        screenshots=[
            ImageMetadata(
                url="https://support.brilliantdirectories.com/images/webhooks-panel.png",
                alt="Developer webhooks configuration interface",
                caption="Developer Hub Webhooks manager with payload test buttons and event selector.",
                ocr_text="Developer Hub > Webhooks | Add Webhook | Target URL: https://api.crm.com/v1/sync | Events: member.signup, lead.created",
                ui_context="Developer Hub > Webhooks tab",
                article_id="5000558460"
            )
        ],
        last_modified="2026-10-18T08:00:54+00:00",
        content_hash="hash_5000558460"
    ),
    Article(
        id="5000558475",
        url="https://support.brilliantdirectories.com/support/solutions/articles/5000558475-when-to-use-settings-vs-custom-code",
        title="Architecture Guide: When to Use Native Settings vs Custom Code",
        category="Consulting",
        folder="Best Practices",
        breadcrumbs=["Solutions", "Consulting", "Architecture", "Settings vs Custom Code"],
        content_text="""A key principle of efficient directory development is maximizing native settings before writing custom code.
Built-in Features (NO Custom Code Needed - $0 / Instant):
- Adding custom profile fields (Form Manager)
- Customizing search filters & radius searches (Form Manager & Search Settings)
- Setting up tiered membership plans with recurring Stripe billing (Membership Plans)
- Lead auto-routing and lead purchase paywalls (Lead Settings)
- SEO meta tags, sitemaps, and robots.txt (SEO Templates)
- Social media links and OpenGraph tags (General Settings)
- Custom menu navigation and footer links (Menu Manager)

When Custom Code IS Required (Billable Development Work):
- Third-party REST API bidirectional syncing (e.g., custom two-way sync with EHR/EMR or external ERP)
- Custom interactive JavaScript widgets (e.g., custom interactive body map for medical symptom search)
- Complex bespoke checkout flows outside Stripe/PayPal
- Deep custom mobile app wrapper (React Native / Flutter) consuming private endpoints.""",
        screenshots=[
            ImageMetadata(
                url="https://support.brilliantdirectories.com/images/settings-vs-custom-code.png",
                alt="Architectural comparison table: Native Settings vs Custom Development",
                caption="Decision matrix showing 85% of directory client requests are configurable via native admin settings.",
                ocr_text="Architecture Guide | 85% Configurable via Settings | 15% Requires Custom Code | Time Savings: 10x",
                ui_context="Architectural Decision Matrix",
                article_id="5000558475"
            )
        ],
        last_modified="2026-10-18T08:00:54+00:00",
        content_hash="hash_5000558475"
    )
]
