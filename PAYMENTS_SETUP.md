# Payment portal setup

The static `payments.html` page requires no Stripe SDK or API keys. The consultation button is intentionally disabled until the owner supplies a verified live Payment Link. No payment processing, subscription creation, or payment confirmation is implemented on the site itself.

## Stripe configuration still required

1. Complete the business account activation and payout setup for DivineGuard IT Services LLC in Stripe. Confirm the support email is AaronFrazier@DGITServices.onmicrosoft.com.
2. Use **Payment Links**, not Terminal (Terminal is for in-person payments). Create a one-time USD 75.00 product named **30-Minute IT/Cyber Consultation**, with quantity fixed at one. Confirm applicable tax settings and the customer-facing total, receipt, refund/cancellation information, and scheduling instructions.
3. Enable cards and, if eligible, ACH Direct Debit in Stripe's payment-method settings. Confirm which methods actually appear on the consultation link, invoices, and subscriptions. ACH confirmation can be delayed; do not treat checkout navigation as proof of settlement.
4. Test the consultation flow in Stripe's sandbox/test mode, then obtain the owner-approved live link. Never place a sandbox link on the production page.
5. In `payments.html`, replace only the disabled button under `STRIPE PAYMENT LINK PLACEHOLDER` with an anchor using the supplied HTTPS Stripe-hosted Payment Link and the existing `btn btn-primary` classes. Use the label **Pay $75 Consultation**. Remove or revise `consultation-payment-status` and the setup-in-progress paragraph only when the corresponding options have been verified. Do not invent a URL or include API keys.
6. For hourly, assessment, and website work, approve scope and amount first; issue a client-specific Stripe invoice or payment link. The public Pay Existing Invoice section tells clients to use the link they were sent or request a resend. Never publish private client invoice links or add a customer-entered arbitrary amount checkout.
7. For managed services, create a monthly recurring price for the client's approved scope and amount, confirm service/cancellation terms, and obtain payment authorization through Stripe before starting billing. Listed monthly prices are starting prices, not automatic subscriptions. Configure receipts, failed-payment handling, and subscription support in Stripe.
8. Verify successful, declined, and canceled test payments plus any ACH pending/verification behavior in Stripe. No live charge or subscription was created during this website implementation.

## Local preview and verification

Run `python3 -m http.server 8000` from the repository and open `http://localhost:8000/payments.html`. The Netlify contact form requires deployment for actual submission handling; local preview verifies navigation and service selection only.

Check navigation at desktop and mobile widths, the disabled consultation button, each Request a Quote link and its selected contact service, and invoice-support links. Review the existing Netlify form settings after deployment. Do not merge until the owner approves the website update.

## Official references

- [Create a Payment Link](https://docs.stripe.com/payment-links/create)
- [ACH Direct Debit](https://docs.stripe.com/payments/ach-direct-debit)
- [Recurring payments](https://docs.stripe.com/recurring-payments)
- [Stripe Terminal: in-person payments](https://docs.stripe.com/terminal)
