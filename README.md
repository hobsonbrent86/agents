# Local agent proofs

Sixty-eight small tools. Each one reads a fixture file and prints a result.
They run on your machine. They do not call a live account.

```bash
python3 run_all.py
```


## Inbound

- [Contact company linker](inbound/01-contact-company-linker): Associates a contact to a company by email domain, then by company name.
- [Phone enrichment](inbound/02-phone-enrichment): Fills a missing phone from the company record, then from a local lookup table.
- [Firm list builder](inbound/03-firm-list-builder): Filters a local directory of investment firms by state and firm type.
- [Attribution validator](inbound/04-attribution-validator): Flags conversions that have no matching click, and totals the spend sitting on those campaigns.
- [Forwarding rule builder](inbound/05-forwarding-rule-builder): Turns plain routing notes into Gmail filter objects. It does not call Google.
- [CRM command bridge](inbound/06-crm-command-bridge): Searches and updates a local CRM fixture from a short command list.
- [Lead scorer](inbound/07-lead-scorer): Ranks new contacts from title, company size, and early page views.
- [Visitor matcher](inbound/08-visitor-matcher): Ties anonymous visits to known contacts by email, then by company domain.
- [Reply intent classifier](inbound/09-reply-intent): Tags a reply as interested, objection, referral, out of office, or unclear.

## Outbound

- [CRM sequence sync](outbound/01-crm-sequence-sync): Merges sequence step, warmth, and task completion between two local copies. The newer timestamp wins.
- [Pipeline digest](outbound/02-pipeline-digest): Formats a daily pipeline note from local sequence stats. It prints the note instead of posting it.
- [Domain provision check](outbound/03-domain-provision-check): Checks a local DNS snapshot and mailbox flags for the records a sending domain needs.
- [Tracking subdomain check](outbound/04-tracking-subdomain-check): Checks that a tracking hostname points at the expected target and is tied to a mailbox.
- [Sequence factory](outbound/05-sequence-factory): Builds an email, social, and phone sequence from a playbook. A second pass patches the subject on step 1.
- [Cohort enrollment](outbound/06-cohort-enrollment): Builds lists from title rules and enrolls people who are not already in a sequence.
- [Send balancer](outbound/07-send-balancer): Assigns queued mail to inboxes without crossing a daily cap.
- [Sequence auditor](outbound/08-sequence-auditor): Finds paused sequences, stale next steps, and broken step numbers.
- [Task repair](outbound/09-task-repair): Reassigns a task to the contact owner and flags tasks that are not linked to a contact.
- [Stage lists](outbound/10-stage-lists): Builds static follow-up lists from sequence stage.
- [Sequence best practices](outbound/11-sequence-best-practices): Applies a short audit: subject length, an opt-out line, a send window, and a step cap.
- [Sequence exporter](outbound/12-sequence-exporter): Writes active sequence copy to markdown and JSON for review.
- [Sequence command bridge](outbound/13-sequence-command-bridge): Runs search and pause commands against a local sequence store.
- [Sync health check](outbound/14-sync-health-check): Compares two contact copies and reports missing ids and field drift.
- [Reply router](outbound/15-reply-router): Pauses a cold sequence when the reply is interested or a referral. Objections stay paused too.
- [Touch queue](outbound/16-touch-queue): Sorts the day's social touches by warmth and fit.
- [Deliverability watch](outbound/17-deliverability-watch): Alerts when bounce rate or spam complaints cross a safe line.

## Lifecycle

- [Directory snapshot](lifecycle/01-directory-snapshot): Flattens users, groups, and MFA status into rows you can save as CSV.
- [Group provisioner](lifecycle/02-group-provisioner): Creates mailing lists that are in the config and missing from the directory.
- [Group member manager](lifecycle/03-group-member-manager): Adds people to a group and skips anyone already on the list.
- [Restricted mailbox](lifecycle/04-restricted-mailbox): Moves a user to a restricted org unit and adds them to the advisor group.
- [Group settings](lifecycle/05-group-settings): Applies reply-to, posting, and moderation changes on a local group record.
- [Advisor group defaults](lifecycle/06-advisor-group-defaults): Sets an advisor-style group to invite only, list replies, and moderated posts.
- [Group reporter](lifecycle/07-group-reporter): Writes a markdown inventory of groups and who can reach them.
- [App install diagnostics](lifecycle/08-app-install-diagnostics): Lists devices whose app install failed, with the error code.
- [Directory questions](lifecycle/09-directory-questions): Answers plain questions about MFA and conditional access from a local snapshot.
- [Task sheet sync](lifecycle/10-task-sheet-sync): Checks checkbox values and writes a clean done flag.
- [Request bot](lifecycle/11-request-bot): Works a local request queue. Summaries, reminders, and lists stay on disk.
- [SSO rollout plan](lifecycle/12-sso-rollout-plan): Checks a rollout list against the evidence files you already have.
- [Onboarding checklist](lifecycle/13-onboarding-checklist): Tracks new-hire steps across mail, devices, and apps.
- [Churn risk](lifecycle/14-churn-risk): Flags accounts whose latest week of use fell well below the prior week.
- [Account health digest](lifecycle/15-account-health-digest): Writes a weekly usage line for each account.

## Operations

- [Transaction categorizer](operations/01-transaction-categorizer): Classifies bank lines from merchant rules. Unknown merchants stay uncategorized.
- [Ledger sync](operations/02-ledger-sync): Maps categorized bank lines to ledger accounts and skips anything still uncategorized.
- [Monthly true-up](operations/03-monthly-true-up): Matches bank lines to ledger lines on date and amount, then lists what is left.
- [Payment export converter](operations/04-payment-export-converter): Turns a payment export into ledger import rows.
- [Payroll inspector](operations/05-payroll-inspector): Reads a payroll export and totals gross pay, headcount, and the pay date.
- [Bank rule builder](operations/06-bank-rule-builder): Proposes a bank rule when the same merchant shows up at least three times.
- [Expense category sync](operations/07-expense-category-sync): Copies expense categories from a sheet into a table and updates rows that changed.
- [Card statement parser](operations/08-card-statement-parser): Parses statement lines into dated expenses and assigns a category.
- [Campaign dashboard](operations/09-campaign-dashboard): Builds a one-page local dashboard for spend, revenue, and conversions that do not match a click.
- [Mail routing audit](operations/10-mail-routing-audit): Says which outbound routing settings a mail API can set, and which ones it cannot.
- [List delivery normalizer](operations/11-list-delivery-normalizer): Sets every group member to receive all list mail.
- [Directory lab checklist](operations/12-directory-lab-checklist): Tracks a lab checklist for a fake directory forest. Host names stay on .example.
- [Invoice reminders](operations/13-invoice-reminders): Stages overdue invoices into a friendly note, a firm note, or a final note.
- [Spend anomaly detector](operations/14-spend-anomaly): Flags a charge that is more than double the usual amount for that vendor.
- [Job health](operations/15-job-health): Flags scheduled jobs whose last success is older than their interval.

## Brand

- [Site architecture classifier](brand/01-site-architecture): Splits sitemap URLs into core product pages and secondary marketing pages.
- [Sitemap compare](brand/02-sitemap-compare): Puts three competitor URL lists next to each other.
- [Page copy extract](brand/03-page-copy-extract): Pulls the title and first heading out of saved HTML.
- [Page pattern library](brand/04-page-pattern-library): Counts how peers structure product, solution, and trust pages.
- [Content blueprint](brand/05-content-blueprint): Recommends pages we are missing when two or more peers already have them.
- [Headline digest](brand/06-headline-digest): Clusters headlines that share a topic and keeps the outlet leaning next to each one.
- [Messaging playbook](brand/07-messaging-playbook): Assembles a short note for each audience from pain, proof, and a call to action.
- [Operations case study](brand/08-operations-case-study): Turns before and after operating numbers into a short case note.
- [Positioning gap](brand/09-positioning-gap): Diffs our page claims against a competitor, line by line.
- [Comparison page](brand/10-comparison-page): Drafts a short comparison from the claims each product makes.
- [Proof collector](brand/11-proof-collector): Collects approved quotes and logos into a list you can hand to a page.
- [Deck metric refresh](brand/12-deck-metric-refresh): Replaces slide placeholders with numbers from a local metrics file.
