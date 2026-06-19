/**
 * Collections Module - Core Service
 * Performance Supply Depot LLC
 * 
 * AI-powered debt collection and recovery system
 * @version 1.0.0
 */

const { EventEmitter } = require('events');
const crypto = require('crypto');

class CollectionsService extends EventEmitter {
  constructor(config = {}) {
    super();
    this.config = {
      tier: config.tier || 'starter',
      maxAccounts: config.maxAccounts || 500,
      responseSLA: config.responseSLA || 72, // hours
      channels: config.channels || ['email', 'sms'],
      ...config
    };
    
    this.accounts = new Map();
    this.workflows = new Map();
    this.metrics = {
      totalAccounts: 0,
      activeCampaigns: 0,
      recoveryRate: 0,
      avgRecoveryTime: 0,
      revenueRecovered: 0
    };
    
    this.tiers = {
      starter: {
        maxAccounts: 500,
        channels: ['email', 'sms'],
        paymentPlans: { maxDuration: 3, minPayment: 25 },
        sla: 72,
        reporting: 'monthly'
      },
      professional: {
        maxAccounts: 2000,
        channels: ['email', 'sms', 'voice'],
        paymentPlans: { maxDuration: 6, minPayment: 25 },
        sla: 48,
        reporting: 'weekly',
        features: ['dispute_management']
      },
      corporate: {
        maxAccounts: Infinity,
        channels: ['email', 'sms', 'voice', 'mail'],
        paymentPlans: { maxDuration: 12, minPayment: 10 },
        sla: 24,
        reporting: 'realtime',
        features: ['dispute_management', 'legal_prep', 'certified_mail', 'dedicated_manager']
      },
      enterprise: {
        maxAccounts: Infinity,
        channels: ['email', 'sms', 'voice', 'mail', 'api'],
        paymentPlans: { custom: true },
        sla: 12,
        reporting: 'realtime',
        features: ['dispute_management', 'legal_prep', 'certified_mail', 'dedicated_manager', 'white_label', 'compliance_mgmt', 'multi_entity']
      }
    };
    
    this.initialized = false;
  }
  
  /**
   * Initialize the collections service
   */
  async init() {
    console.log(`[Collections] Initializing ${this.config.tier} tier...`);
    
    const tier = this.tiers[this.config.tier];
    if (!tier) {
      throw new Error(`Invalid tier: ${this.config.tier}`);
    }
    
    // Load default workflows
    await this.loadWorkflows();
    
    this.initialized = true;
    this.emit('ready');
    console.log(`[Collections] Ready - ${this.config.tier.toUpperCase()} tier active`);
    
    return this;
  }
  
  /**
   * Load default collection workflows
   */
  async loadWorkflows() {
    const workflows = [
      {
        id: 'early_stage',
        name: 'Early Stage (0-30 days)',
        stages: [
          { day: 0, action: 'friendly_reminder', channel: 'email' },
          { day: 3, action: 'follow_up', channel: 'email' },
          { day: 7, action: 'sms_reminder', channel: 'sms' },
          { day: 14, action: 'phone_call', channel: 'voice' }
        ],
        tone: 'friendly'
      },
      {
        id: 'mid_stage',
        name: 'Mid Stage (31-60 days)',
        stages: [
          { day: 31, action: 'urgent_notice', channel: 'email' },
          { day: 35, action: 'phone_call', channel: 'voice' },
          { day: 45, action: 'demand_letter', channel: 'mail' },
          { day: 60, action: 'final_notice', channel: 'email' }
        ],
        tone: 'firm'
      },
      {
        id: 'late_stage',
        name: 'Late Stage (60+ days)',
        stages: [
          { day: 61, action: 'legal_notice', channel: 'mail' },
          { day: 75, action: 'collection_agency', channel: 'external' },
          { day: 90, action: 'litigation_prep', channel: 'legal' }
        ],
        tone: 'serious'
      },
      {
        id: 'payment_plan',
        name: 'Payment Plan Workflow',
        stages: [
          { day: 0, action: 'plan_confirmation', channel: 'email' },
          { day: 3, action: 'first_reminder', channel: 'sms', beforePayment: true },
          { day: -1, action: 'payment_due', channel: 'sms' },
          { day: 1, action: 'payment_missed', channel: 'email' },
          { day: 3, action: 'follow_up_call', channel: 'voice' }
        ],
        tone: 'supportive'
      }
    ];
    
    workflows.forEach(wf => this.workflows.set(wf.id, wf));
    console.log(`[Collections] Loaded ${workflows.length} workflows`);
  }
  
  /**
   * Add a new account to collections
   */
  async addAccount(accountData) {
    const { accountId, debtorInfo, balance, daysDelinquent, invoiceRefs } = accountData;
    
    if (this.accounts.size >= this.config.maxAccounts) {
      throw new Error('Account limit reached for current tier');
    }
    
    const account = {
      id: accountId || crypto.randomUUID(),
      debtor: debtorInfo,
      balance: parseFloat(balance),
      daysDelinquent: parseInt(daysDelinquent),
      invoiceRefs: invoiceRefs || [],
      status: 'active',
      priority: this.calculatePriority(balance, daysDelinquent),
      workflow: this.assignWorkflow(daysDelinquent),
      createdAt: new Date(),
      lastActivity: new Date(),
      paymentPlan: null,
      notes: [],
      communications: []
    };
    
    this.accounts.set(account.id, account);
    this.metrics.totalAccounts++;
    
    this.emit('account:added', account);
    console.log(`[Collections] Account ${account.id} added (${account.priority} priority)`);
    
    return account;
  }
  
  /**
   * Calculate account priority based on balance and delinquency
   */
  calculatePriority(balance, days) {
    const score = (balance * 0.6) + (days * 10);
    
    if (score >= 5000) return 'critical';
    if (score >= 2000) return 'high';
    if (score >= 500) return 'medium';
    return 'low';
  }
  
  /**
   * Assign appropriate workflow based on delinquency
   */
  assignWorkflow(days) {
    if (days >= 60) return 'late_stage';
    if (days >= 30) return 'mid_stage';
    return 'early_stage';
  }
  
  /**
   * Process the next action for an account
   */
  async processAccount(accountId) {
    const account = this.accounts.get(accountId);
    if (!account) throw new Error('Account not found');
    
    const workflow = this.workflows.get(account.workflow);
    if (!workflow) throw new Error('Workflow not found');
    
    // Find next pending stage
    const nextStage = workflow.stages.find(s => !s.completed);
    if (!nextStage) {
      console.log(`[Collections] Account ${accountId} workflow complete`);
      return { status: 'complete' };
    }
    
    // Execute action
    const result = await this.executeAction(account, nextStage);
    
    // Update account
    account.lastActivity = new Date();
    account.communications.push({
      action: nextStage.action,
      channel: nextStage.channel,
      timestamp: new Date(),
      result: result.status
    });
    
    nextStage.completed = true;
    nextStage.completedAt = new Date();
    
    this.emit('action:completed', { accountId, action: nextStage.action, result });
    
    return result;
  }
  
  /**
   * Execute a collection action
   */
  async executeAction(account, stage) {
    const { action, channel } = stage;
    
    console.log(`[Collections] Executing ${action} via ${channel} for ${account.id}`);
    
    // Simulate action execution
    const templates = {
      friendly_reminder: this.getTemplate('friendly_reminder', account),
      urgent_notice: this.getTemplate('urgent_notice', account),
      demand_letter: this.getTemplate('demand_letter', account),
      legal_notice: this.getTemplate('legal_notice', account)
    };
    
    // In production, this would integrate with email/SMS/voice APIs
    return {
      status: 'sent',
      channel,
      action,
      template: templates[action],
      timestamp: new Date()
    };
  }
  
  /**
   * Get template for action
   */
  getTemplate(templateName, account) {
    const templates = require('./templates');
    return templates.get(templateName, {
      debtorName: account.debtor.name,
      balance: account.balance.toFixed(2),
      daysDelinquent: account.daysDelinquent,
      accountId: account.id
    });
  }
  
  /**
   * Set up a payment plan
   */
  async createPaymentPlan(accountId, planData) {
    const account = this.accounts.get(accountId);
    if (!account) throw new Error('Account not found');
    
    const tier = this.tiers[this.config.tier];
    
    const plan = {
      id: crypto.randomUUID(),
      accountId,
      totalAmount: account.balance,
      numPayments: planData.numPayments || 3,
      paymentAmount: account.balance / (planData.numPayments || 3),
      frequency: planData.frequency || 'monthly',
      startDate: planData.startDate || new Date(),
      payments: [],
      status: 'active'
    };
    
    // Validate against tier limits
    if (plan.numPayments > tier.paymentPlans.maxDuration) {
      throw new Error(`Max ${tier.paymentPlans.maxDuration} payments allowed on ${this.config.tier} tier`);
    }
    
    account.paymentPlan = plan;
    account.workflow = 'payment_plan';
    
    this.emit('paymentplan:created', plan);
    console.log(`[Collections] Payment plan created for ${accountId}: ${plan.numPayments} x $${plan.paymentAmount.toFixed(2)}`);
    
    return plan;
  }
  
  /**
   * Process a payment
   */
  async processPayment(accountId, amount) {
    const account = this.accounts.get(accountId);
    if (!account) throw new Error('Account not found');
    
    const payment = {
      id: crypto.randomUUID(),
      accountId,
      amount: parseFloat(amount),
      timestamp: new Date(),
      method: 'manual' // Could be 'auto', 'check', etc.
    };
    
    account.balance -= payment.amount;
    this.metrics.revenueRecovered += payment.amount;
    
    if (account.paymentPlan) {
      account.paymentPlan.payments.push(payment);
      
      // Check if plan complete
      const totalPaid = account.paymentPlan.payments.reduce((sum, p) => sum + p.amount, 0);
      if (totalPaid >= account.paymentPlan.totalAmount) {
        account.paymentPlan.status = 'completed';
        account.status = 'paid';
        this.emit('account:paid', account);
      }
    }
    
    if (account.balance <= 0) {
      account.status = 'paid';
      account.balance = 0;
      this.emit('account:paid', account);
    }
    
    this.emit('payment:received', payment);
    console.log(`[Collections] Payment received: $${payment.amount.toFixed(2)} for ${accountId}`);
    
    return payment;
  }
  
  /**
   * Get current metrics
   */
  getMetrics() {
    const accounts = Array.from(this.accounts.values());
    const paidAccounts = accounts.filter(a => a.status === 'paid');
    const activeAccounts = accounts.filter(a => a.status === 'active');
    
    return {
      ...this.metrics,
      totalAccounts: accounts.length,
      activeAccounts: activeAccounts.length,
      paidAccounts: paidAccounts.length,
      recoveryRate: accounts.length > 0 ? (paidAccounts.length / accounts.length * 100).toFixed(2) : 0,
      avgRecoveryTime: this.calculateAvgRecoveryTime(paidAccounts),
      byPriority: {
        critical: accounts.filter(a => a.priority === 'critical').length,
        high: accounts.filter(a => a.priority === 'high').length,
        medium: accounts.filter(a => a.priority === 'medium').length,
        low: accounts.filter(a => a.priority === 'low').length
      }
    };
  }
  
  calculateAvgRecoveryTime(paidAccounts) {
    if (paidAccounts.length === 0) return 0;
    
    const totalDays = paidAccounts.reduce((sum, a) => {
      const days = Math.floor((a.lastActivity - a.createdAt) / (1000 * 60 * 60 * 24));
      return sum + days;
    }, 0);
    
    return Math.round(totalDays / paidAccounts.length);
  }
  
  /**
   * Get accounts by filter
   */
  getAccounts(filter = {}) {
    let accounts = Array.from(this.accounts.values());
    
    if (filter.status) {
      accounts = accounts.filter(a => a.status === filter.status);
    }
    if (filter.priority) {
      accounts = accounts.filter(a => a.priority === filter.priority);
    }
    if (filter.workflow) {
      accounts = accounts.filter(a => a.workflow === filter.workflow);
    }
    if (filter.minBalance) {
      accounts = accounts.filter(a => a.balance >= filter.minBalance);
    }
    
    return accounts;
  }
  
  /**
   * Export account data
   */
  export(format = 'json') {
    const data = {
      exportDate: new Date().toISOString(),
      tier: this.config.tier,
      metrics: this.getMetrics(),
      accounts: Array.from(this.accounts.values())
    };
    
    if (format === 'csv') {
      return this.toCsv(data.accounts);
    }
    
    return JSON.stringify(data, null, 2);
  }
  
  toCsv(accounts) {
    const headers = ['ID', 'Name', 'Email', 'Phone', 'Balance', 'Days Delinquent', 'Priority', 'Status', 'Created'];
    const rows = accounts.map(a => [
      a.id,
      a.debtor.name,
      a.debtor.email,
      a.debtor.phone,
      a.balance,
      a.daysDelinquent,
      a.priority,
      a.status,
      a.createdAt.toISOString()
    ]);
    
    return [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  }
}

module.exports = CollectionsService;
