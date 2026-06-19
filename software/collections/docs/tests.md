# Collections Module Tests

## Test Structure

```
tests/
├── unit/
│   ├── CollectionsService.test.js
│   ├── templates.test.js
│   └── priorityEngine.test.js
├── integration/
│   ├── api.test.js
│   ├── workflows.test.js
│   └── payments.test.js
└── e2e/
    └── fullCollectionCycle.test.js
```

## Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific file
npm test -- tests/unit/CollectionsService.test.js

# Run in watch mode
npm test -- --watch
```

## Sample Test Cases

### CollectionsService Unit Tests

```javascript
const CollectionsService = require('../src/CollectionsService');

describe('CollectionsService', () => {
  let service;
  
  beforeEach(async () => {
    service = new CollectionsService({ tier: 'professional' });
    await service.init();
  });
  
  describe('Account Management', () => {
    test('should add a new account', async () => {
      const account = await service.addAccount({
        debtorInfo: {
          name: 'Test Company',
          email: 'test@test.com',
          phone: '555-1234'
        },
        balance: 1000,
        daysDelinquent: 30
      });
      
      expect(account).toHaveProperty('id');
      expect(account.balance).toBe(1000);
      expect(account.status).toBe('active');
    });
    
    test('should calculate priority correctly', () => {
      expect(service.calculatePriority(10000, 90)).toBe('critical');
      expect(service.calculatePriority(5000, 45)).toBe('high');
      expect(service.calculatePriority(1000, 30)).toBe('medium');
      expect(service.calculatePriority(100, 15)).toBe('low');
    });
    
    test('should enforce tier limits', async () => {
      service.config.maxAccounts = 2;
      
      await service.addAccount({ debtorInfo: { name: 'A' }, balance: 100, daysDelinquent: 30 });
      await service.addAccount({ debtorInfo: { name: 'B' }, balance: 100, daysDelinquent: 30 });
      
      await expect(
        service.addAccount({ debtorInfo: { name: 'C' }, balance: 100, daysDelinquent: 30 })
      ).rejects.toThrow('Account limit reached');
    });
  });
  
  describe('Payment Processing', () => {
    test('should process payment and reduce balance', async () => {
      const account = await service.addAccount({
        debtorInfo: { name: 'Test', email: 'test@test.com' },
        balance: 1000,
        daysDelinquent: 30
      });
      
      const payment = await service.processPayment(account.id, 500);
      
      expect(payment.amount).toBe(500);
      expect(service.accounts.get(account.id).balance).toBe(500);
    });
    
    test('should mark account as paid when balance zero', async () => {
      const account = await service.addAccount({
        debtorInfo: { name: 'Test', email: 'test@test.com' },
        balance: 100,
        daysDelinquent: 30
      });
      
      await service.processPayment(account.id, 100);
      
      expect(service.accounts.get(account.id).status).toBe('paid');
    });
  });
  
  describe('Payment Plans', () => {
    test('should create payment plan', async () => {
      const account = await service.addAccount({
        debtorInfo: { name: 'Test', email: 'test@test.com' },
        balance: 600,
        daysDelinquent: 45
      });
      
      const plan = await service.createPaymentPlan(account.id, {
        numPayments: 3
      });
      
      expect(plan.numPayments).toBe(3);
      expect(plan.paymentAmount).toBe(200);
      expect(account.paymentPlan).toEqual(plan);
    });
    
    test('should enforce max payments per tier', async () => {
      service.config.tier = 'starter';
      
      const account = await service.addAccount({
        debtorInfo: { name: 'Test', email: 'test@test.com' },
        balance: 1000,
        daysDelinquent: 45
      });
      
      await expect(
        service.createPaymentPlan(account.id, { numPayments: 6 })
      ).rejects.toThrow('Max 3 payments allowed');
    });
  });
  
  describe('Metrics', () => {
    test('should calculate recovery rate', async () => {
      // Add 4 accounts, mark 2 as paid
      for (let i = 0; i < 4; i++) {
        const acc = await service.addAccount({
          debtorInfo: { name: `Test${i}`, email: `test${i}@test.com` },
          balance: 100,
          daysDelinquent: 30
        });
        if (i < 2) {
          await service.processPayment(acc.id, 100);
        }
      }
      
      const metrics = service.getMetrics();
      expect(metrics.recoveryRate).toBe('50.00');
    });
  });
});
```

### Template Tests

```javascript
const { getTemplate, substituteVariables } = require('../src/templates');

describe('Templates', () => {
  test('should substitute variables in template', () => {
    const template = 'Hello {{name}}, your balance is ${{balance}}';
    const result = substituteVariables(template, {
      name: 'John',
      balance: '100.00'
    });
    
    expect(result).toBe('Hello John, your balance is $100.00');
  });
  
  test('should load email template', () => {
    const template = getTemplate('friendly_reminder', {
      debtorName: 'Acme Corp',
      balance: '500.00',
      invoiceNumber: 'INV-001'
    });
    
    expect(template.email).toContain('Acme Corp');
    expect(template.email).toContain('$500.00');
    expect(template.subject).toContain('INV-001');
  });
  
  test('should throw error for missing template', () => {
    expect(() => {
      getTemplate('nonexistent');
    }).toThrow("Template 'nonexistent' not found");
  });
});
```

### API Integration Tests

```javascript
const request = require('supertest');
const app = require('../src/app');

describe('Collections API', () => {
  describe('POST /api/v1/accounts', () => {
    test('should create account', async () => {
      const response = await request(app)
        .post('/api/v1/accounts')
        .send({
          debtor: {
            name: 'Test Company',
            email: 'test@test.com',
            phone: '555-1234'
          },
          balance: 1000,
          daysDelinquent: 30
        });
      
      expect(response.status).toBe(201);
      expect(response.body).toHaveProperty('id');
    });
    
    test('should validate required fields', async () => {
      const response = await request(app)
        .post('/api/v1/accounts')
        .send({
          balance: 1000
          // Missing debtor
        });
      
      expect(response.status).toBe(400);
    });
  });
  
  describe('GET /api/v1/accounts', () => {
    test('should list accounts', async () => {
      const response = await request(app)
        .get('/api/v1/accounts')
        .query({ status: 'active' });
      
      expect(response.status).toBe(200);
      expect(Array.isArray(response.body)).toBe(true);
    });
  });
  
  describe('POST /api/v1/accounts/:id/payments', () => {
    test('should process payment', async () => {
      // Create account first
      const accountRes = await request(app)
        .post('/api/v1/accounts')
        .send({
          debtor: { name: 'Test', email: 'test@test.com' },
          balance: 1000,
          daysDelinquent: 30
        });
      
      const accountId = accountRes.body.id;
      
      const paymentRes = await request(app)
        .post(`/api/v1/accounts/${accountId}/payments`)
        .send({ amount: 500 });
      
      expect(paymentRes.status).toBe(201);
      expect(paymentRes.body.amount).toBe(500);
    });
  });
});
```

## Mock Services

```javascript
// tests/mocks/sendgrid.js
module.exports = {
  send: jest.fn().mockResolvedValue({ id: 'mock-message-id' })
};

// tests/mocks/twilio.js
module.exports = {
  messages: {
    create: jest.fn().mockResolvedValue({ sid: 'mock-sid' })
  },
  calls: {
    create: jest.fn().mockResolvedValue({ sid: 'mock-call-sid' })
  }
};

// tests/mocks/stripe.js
module.exports = {
  charges: {
    create: jest.fn().mockResolvedValue({
      id: 'ch_mock',
      amount: 50000,
      status: 'succeeded'
    })
  }
};
```

## Test Configuration

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/index.js'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  testMatch: [
    '**/tests/**/*.test.js'
  ],
  setupFilesAfterEnv: ['<rootDir>/tests/setup.js']
};
```

## CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run migrations
        run: npm run migrate
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/collections_test
      
      - name: Run tests
        run: npm run test:coverage
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/collections_test
          REDIS_URL: redis://localhost:6379
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

*Last Updated: 2026-06-12*
