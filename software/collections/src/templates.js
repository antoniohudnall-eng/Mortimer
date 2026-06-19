/**
 * Collections Templates
 * Email, SMS, and letter templates for debt collection
 */

const templates = {
  // Early Stage (Friendly)
  friendly_reminder: {
    subject: "Friendly reminder: Invoice {{invoiceNumber}} due",
    email: `Hi {{debtorName}},

I hope you're doing well! I wanted to quickly follow up on invoice #{{invoiceNumber}} for ${{balance}} that was due {{dueDate}}.

We value your business and understand that things can get busy. If you've already sent payment, please disregard this message.

If you need any assistance or have questions about this invoice, I'm here to help.

Best regards,
Collections Team
Performance Supply Depot`,
    sms: `Hi {{debtorName}}, friendly reminder: Invoice {{invoiceNumber}} for ${{balance}} is overdue. Pay online: psdepot.com/pay or call 1-800-DEPOT-01`
  },
  
  follow_up: {
    subject: "Following up: Invoice {{invoiceNumber}} payment",
    email: `Hi {{debtorName}},

I'm following up on my previous email regarding invoice #{{invoiceNumber}} for ${{balance}} ({{daysDelinquent}} days overdue).

We'd love to keep this relationship smooth. Could you confirm when we can expect payment, or if there's anything we can help with?

If cash flow is tight right now, we can discuss a payment plan that works for you.

Thanks,
Collections Team
Performance Supply Depot`,
    sms: `Hi {{debtorName}}, following up on invoice {{invoiceNumber}} for ${{balance}}. Can we help? Call 1-800-DEPOT-01 or reply PAY to set up a payment plan.`
  },
  
  // Mid Stage (Firm)
  urgent_notice: {
    subject: "URGENT: Payment required - Account {{accountId}}",
    email: `Dear {{debtorName}},

This is an urgent notice regarding your outstanding balance of ${{balance}}, now {{daysDelinquent}} days overdue.

Invoice: {{invoiceNumber}}
Account: {{accountId}}
Amount Due: ${{balance}}
Days Overdue: {{daysDelinquent}}

Immediate payment is required to avoid further collection action. 

Pay now: https://psdepot.com/pay?account={{accountId}}

If you cannot pay in full, please contact us immediately to discuss payment options.

Sincerely,
Collections Department
Performance Supply Depot
1-800-DEPOT-01`,
    sms: `URGENT: Your account {{accountId}} is {{daysDelinquent}} days overdue with balance ${{balance}}. Pay now: psdepot.com/pay or call 1-800-DEPOT-01 immediately.`
  },
  
  demand_letter: {
    subject: "Final Demand for Payment - Account {{accountId}}",
    email: null, // Mail only
    letter: `DEMAND FOR PAYMENT

Date: {{currentDate}}
Account: {{accountId}}
Amount Due: ${{balance}}
Days Overdue: {{daysDelinquent}}

Dear {{debtorName}},

This letter serves as formal demand for immediate payment of ${{balance}} owed to Performance Supply Depot LLC for goods/services rendered.

If payment is not received within 10 days of this letter, we will be forced to:

1. Report this debt to credit bureaus
2. Forward to a collection agency
3. Pursue legal action to recover the debt plus applicable fees

PAYMENT OPTIONS:
- Online: psdepot.com/pay?account={{accountId}}
- Phone: 1-800-DEPOT-01
- Mail: Performance Supply Depot, Collections Dept, [Address]

If you dispute this debt or need to make payment arrangements, you must contact us within 10 days.

This is an attempt to collect a debt. Any information obtained will be used for that purpose.

Sincerely,
Collections Department
Performance Supply Depot LLC`,
    sms: null
  },
  
  // Late Stage (Serious)
  legal_notice: {
    subject: "LEGAL NOTICE - Account {{accountId}}",
    email: null, // Certified mail
    letter: `LEGAL NOTICE

Date: {{currentDate}}
Re: Account {{accountId}}
Outstanding Balance: ${{balance}}

Dear {{debtorName}},

Despite multiple attempts to resolve this matter amicably, your account remains unpaid with a balance of ${{balance}}, now {{daysDelinquent}} days overdue.

This is your FINAL NOTICE before we escalate this matter to our legal department and/or external collection agency.

ESCALATION TIMELINE:
- 10 days: Credit bureau reporting
- 15 days: Collection agency assignment
- 30 days: Legal proceedings initiated

To avoid these actions, you must:
1. Pay in full: ${{balance}}, OR
2. Enter into a binding payment agreement: Call 1-800-DEPOT-01

If we do not hear from you within 10 days, we will proceed with escalation without further notice.

Performance Supply Depot LLC
Collections Department`,
    sms: null
  },
  
  // Payment Plan
  plan_confirmation: {
    subject: "Payment Plan Confirmation - Account {{accountId}}",
    email: `Hi {{debtorName}},

Thank you for working with us to set up a payment plan for account {{accountId}}.

PAYMENT PLAN DETAILS:
Total Balance: ${{balance}}
Number of Payments: {{numPayments}}
Payment Amount: ${{paymentAmount}}
Frequency: {{frequency}}
First Payment Due: {{firstPaymentDate}}

Your payments will be automatically charged on the {{paymentDay}} of each month starting {{firstPaymentDate}}.

PAYMENT SCHEDULE:
{{paymentSchedule}}

If you need to modify this plan or have any questions, please contact us at 1-800-DEPOT-01.

Thank you for your commitment to resolving this.

Best regards,
Collections Team
Performance Supply Depot`,
    sms: `Payment plan confirmed for account {{accountId}}: {{numPayments}} payments of ${{paymentAmount}} starting {{firstPaymentDate}}. Questions? Call 1-800-DEPOT-01`
  },
  
  payment_due: {
    subject: "Payment Due Reminder - Account {{accountId}}",
    email: `Hi {{debtorName}},

This is a friendly reminder that your scheduled payment of ${{paymentAmount}} for account {{accountId}} is due tomorrow ({{dueDate}}).

The payment will be automatically processed using your saved payment method.

If you need to update your payment method or have questions, please call 1-800-DEPOT-01 before {{dueDate}}.

Thank you,
Collections Team`,
    sms: `Reminder: Your ${{paymentAmount}} payment for account {{accountId}} is due tomorrow {{dueDate}}. Will auto-charge. Questions? Call 1-800-DEPOT-01`
  },
  
  payment_missed: {
    subject: "Missed Payment - Account {{accountId}}",
    email: `Hi {{debtorName}},

We attempted to process your scheduled payment of ${{paymentAmount}} for account {{accountId}}, but the payment could not be completed.

This may be due to:
- Insufficient funds
- Expired payment method
- Bank declined transaction

Please update your payment information and submit payment as soon as possible:
https://psdepot.com/pay?account={{accountId}}

If you're experiencing financial difficulties, please contact us at 1-800-DEPOT-01 to discuss options.

Collections Team
Performance Supply Depot`,
    sms: `Payment of ${{paymentAmount}} for account {{accountId}} could not be processed. Please update payment info: psdepot.com/pay or call 1-800-DEPOT-01`
  },
  
  // Cold Outreach
  cold_outreach: {
    subject: "Struggling with unpaid invoices? We can help",
    email: `Hi {{prospectName}},

I noticed {{companyName}} may be dealing with outstanding receivables like many businesses in the {{industry}} space.

Quick question: How much time is your team spending chasing unpaid invoices?

The challenge most {{industry}} companies face:
- Manual follow-ups drain 10+ hours/week
- Delinquent accounts sit untouched for months
- No systematic approach to collections
- Cash flow suffers from slow recovery

**Our AI-powered collections service solves this.**

Performance Supply Depot Collections ($499-$3,999/month):
✓ Automated multi-channel outreach (email, SMS, voice)
✓ Smart prioritization by recovery probability
✓ Payment plan automation
✓ Real-time recovery dashboard
✓ Legal escalation when needed

**ROI:** Replace 20+ hours/week of manual work with automated recovery.

30-day trial available. No commitment, no setup fees.

Want to see how it works for {{companyName}}?

Best,
Miles
Sales Consultant, Performance Supply Depot
miles@psdepot.com | 1-800-DEPOT-01

P.S. We're offering a free collections audit for {{industry}} companies this month. Reply AUDIT to claim yours.`,
    sms: null
  }
};

/**
 * Get a template with variable substitution
 */
function getTemplate(name, variables = {}) {
  const template = templates[name];
  if (!template) {
    throw new Error(`Template '${name}' not found`);
  }
  
  // Substitute variables in all template fields
  const result = {};
  for (const [key, value] of Object.entries(template)) {
    if (value && typeof value === 'string') {
      result[key] = substituteVariables(value, variables);
    } else {
      result[key] = value;
    }
  }
  
  return result;
}

/**
 * Substitute {{variable}} placeholders with actual values
 */
function substituteVariables(template, variables) {
  let result = template;
  for (const [key, value] of Object.entries(variables)) {
    const regex = new RegExp(`{{${key}}}`, 'g');
    result = result.replace(regex, value || '');
  }
  // Clean up any remaining placeholders
  result = result.replace(/{{\w+}}/g, '');
  return result;
}

module.exports = {
  templates,
  getTemplate,
  substituteVariables
};
