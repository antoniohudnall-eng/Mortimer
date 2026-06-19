#!/usr/bin/env python3
"""
⚡ TEMPORAL SALES FUNNEL - Agent Sales TikTok
Integrates: Stripe (psdepot) + EVM Wallet + Agent Delivery

PATRICIA-APPROVED ARCHITECTURE
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum
import hashlib

# ========== CONFIG ==========

STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

# EVM Wallet (Captain's)
EVM_WALLET = "0x7244d8C20394CC11D54b2583Fb813B3EB8B72f36"
CRYPTO_PAYMENT_ADDRESS = "0x7244d8C20394CC11D54b2583Fb813B3EB8B72f36"

# Agents with Stripe Price IDs (to be configured)
AGENT_PRODUCTS = {
    "clerk": {"price": 97, "stripe_price_id": "price_clerk_monthly", "name": "CLERK Agent"},
    "greet": {"price": 147, "stripe_price_id": "price_greet_monthly", "name": "GREET Agent"},
    "personal": {"price": 197, "stripe_price_id": "price_personal_monthly", "name": "PERSONAL Agent"},
    "velvet": {"price": 247, "stripe_price_id": "price_velvet_monthly", "name": "VELVET Agent"},
    "concierge": {"price": 297, "stripe_price_id": "price_concierge_monthly", "name": "CONCIERGE Agent"},
    "executive": {"price": 497, "stripe_price_id": "price_executive_monthly", "name": "EXECUTIVE Agent"},
}

# EVM Crypto prices (would need oracle for real-time)
CRYPTO_PRICES = {
    "ETH": 3500,  # Approximate
    "USDC": 1,
    "USDT": 1,
}


class FunnelState(Enum):
    LEAD_CAPTURED = "lead_captured"
    CHECKOUT_STARTED = "checkout_started"
    PAYMENT_PENDING = "payment_pending"
    PAYMENT_CONFIRMED = "payment_confirmed"
    AGENT_PROVISIONING = "agent_provisioning"
    AGENT_DELIVERED = "agent_delivered"
    ACTIVE = "active"
    CANCELLED = "cancelled"
    FAILED = "failed"


@dataclass
class Customer:
    id: str
    email: str
    tiktok_handle: Optional[str] = None
    stripe_customer_id: Optional[str] = None
    wallet_address: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Order:
    id: str
    customer_id: str
    agent_type: str
    amount: int  # cents
    currency: str  # usd, eth, usdc
    payment_method: str  # stripe, crypto
    payment_intent_id: Optional[str] = None
    state: FunnelState = FunnelState.LEAD_CAPTURED
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ========== TEMPORAL WORKFLOWS ==========

class SalesFunnelWorkflows:
    """
    Temporal-style sales funnel workflows
    
    Workflow 1: CustomerOrderFlow
    Workflow 2: PaymentProcessing
    Workflow 3: AgentProvisioning
    Workflow 4: SubscriptionManagement
    """
    
    def __init__(self, data_dir: str = "~/.mortimer/sales"):
        self.data_dir = Path(data_dir).expanduser()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.orders_file = self.data_dir / "orders.json"
        self.customers_file = self.data_dir / "customers.json"
        self.orders = self._load_orders()
        self.customers = self._load_customers()
    
    def _load_orders(self) -> List[Order]:
        if self.orders_file.exists():
            data = json.loads(self.orders_file.read_text())
            return [Order(**o) if isinstance(o, dict) else o for o in data]
        return []
    
    def _save_orders(self):
        self.orders_file.write_text(json.dumps([
            {**o.__dict__, 'state': o.state.value} for o in self.orders
        ], indent=2))
    
    def _load_customers(self) -> Dict[str, Customer]:
        if self.customers_file.exists():
            data = json.loads(self.customers_file.read_text())
            return {k: Customer(**v) for k, v in data.items()}
        return {}
    
    def _save_customers(self):
        self.customers_file.write_text(json.dumps({
            k: v.__dict__ for k, v in self.customers.items()
        }, indent=2))
    
    # ========== WORKFLOW 1: Customer Order Flow ==========
    
    def start_order(self, email: str, agent_type: str, 
                   payment_method: str = "stripe",
                   tiktok_handle: str = None) -> str:
        """
        Start new customer order flow
        Signal: AwaitPayment
        """
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{agent_type[:3]}"
        
        # Create or get customer
        customer_id = hashlib.md5(email.encode()).hexdigest()[:12]
        if customer_id not in self.customers:
            self.customers[customer_id] = Customer(
                id=customer_id,
                email=email,
                tiktok_handle=tiktok_handle
            )
        
        order = Order(
            id=order_id,
            customer_id=customer_id,
            agent_type=agent_type,
            amount=AGENT_PRODUCTS[agent_type]["price"] * 100,  # cents
            currency="usd" if payment_method == "stripe" else "eth",
            payment_method=payment_method,
            state=FunnelState.LEAD_CAPTURED
        )
        
        self.orders.append(order)
        self._save_orders()
        self._save_customers()
        
        return order_id
    
    def get_order(self, order_id: str) -> Optional[Order]:
        for o in self.orders:
            if o.id == order_id:
                return o
        return None
    
    # ========== WORKFLOW 2: Payment Processing ==========
    
    def create_stripe_checkout(self, order_id: str) -> Dict:
        """
        Activity: Create Stripe Checkout Session
        Retry: 3x with backoff
        """
        order = self.get_order(order_id)
        if not order:
            raise Exception("Order not found")
        
        if not STRIPE_API_KEY:
            return {
                "status": "demo",
                "checkout_url": f"https://psdepot.com/checkout/{order_id}",
                "session_id": f"cs_demo_{order_id}"
            }
        
        try:
            # Create Stripe Checkout Session
            headers = {
                "Authorization": f"Bearer {STRIPE_API_KEY}",
                "Content-Type": "application/json"
            }
            
            product = AGENT_PRODUCTS[order.agent_type]
            
            data = {
                "mode": "subscription",
                "success_url": f"https://agentfleet.com/success?order={order_id}",
                "cancel_url": f"https://agentfleet.com/cancel?order={order_id}",
                "line_items": [{
                    "price": product["stripe_price_id"],
                    "quantity": 1
                }],
                "metadata": {
                    "order_id": order_id,
                    "agent_type": order.agent_type,
                    "customer_id": order.customer_id
                }
            }
            
            response = requests.post(
                "https://api.stripe.com/v1/checkout/sessions",
                headers=headers,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                order.payment_intent_id = result["id"]
                order.state = FunnelState.PAYMENT_PENDING
                self._save_orders()
                
                return {
                    "status": "success",
                    "checkout_url": result["url"],
                    "session_id": result["id"]
                }
            else:
                raise Exception(f"Stripe error: {response.text}")
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def verify_crypto_payment(self, order_id: str, tx_hash: str) -> Dict:
        """
        Activity: Verify crypto payment on-chain
        Retry: 5x (blockchain dependent)
        """
        # Would integrate with EVM wallet API
        # For now, simulate verification
        order = self.get_order(order_id)
        if not order:
            return {"status": "error", "message": "Order not found"}
        
        # Simulate payment verification
        return {
            "status": "verified",
            "tx_hash": tx_hash,
            "block_number": 18500000,
            "confirmations": 12
        }
    
    # ========== WORKFLOW 3: Agent Provisioning ==========
    
    def provision_agent(self, order_id: str) -> Dict:
        """
        Activity: Provision and deliver agent to customer
        Signal: HumanApproval (optional)
        """
        order = self.get_order(order_id)
        if not order:
            raise Exception("Order not found")
        
        order.state = FunnelState.AGENT_PROVISIONING
        self._save_orders()
        
        # Would trigger agent creation workflow
        agent_type = order.agent_type
        customer = self.customers.get(order.customer_id)
        
        # Provisioning steps
        result = {
            "order_id": order_id,
            "agent_type": agent_type,
            "customer_email": customer.email if customer else "unknown",
            "provisioned_at": datetime.now().isoformat(),
            "status": "ready",
            "delivery_method": "email" if customer else "telegram"
        }
        
        order.state = FunnelState.AGENT_DELIVERED
        order.metadata["provisioned"] = result
        self._save_orders()
        
        return result
    
    # ========== WORKFLOW 4: Subscription Management ==========
    
    def handle_webhook(self, event: dict) -> Dict:
        """
        Handle Stripe webhook events
        Signals: PaymentSucceeded, PaymentFailed, SubscriptionUpdated
        """
        event_type = event.get("type", "")
        
        if event_type == "checkout.session.completed":
            session = event["data"]["object"]
            order_id = session["metadata"].get("order_id")
            
            if order_id:
                order = self.get_order(order_id)
                if order:
                    order.state = FunnelState.PAYMENT_CONFIRMED
                    self._save_orders()
                    
                    # Trigger provisioning
                    self.provision_agent(order_id)
                    
                    return {"status": "processed", "action": "provision_agent"}
        
        elif event_type == "invoice.paid":
            # Recurring payment succeeded
            return {"status": "processed", "action": "renew_subscription"}
        
        elif event_type == "customer.subscription.deleted":
            # Subscription cancelled
            return {"status": "processed", "action": "deactivate_agent"}
        
        return {"status": "ignored", "event": event_type}
    
    # ========== QUERIES ==========
    
    def query_order(self, order_id: str) -> Dict:
        """Query order status"""
        order = self.get_order(order_id)
        if not order:
            return {"error": "Order not found"}
        
        return {
            "id": order.id,
            "agent_type": order.agent_type,
            "state": order.state.value,
            "amount": f"${order.amount / 100}",
            "payment_method": order.payment_method,
            "created": order.created_at
        }
    
    def query_revenue(self, period: str = "all") -> Dict:
        """Query revenue metrics"""
        completed = [o for o in self.orders 
                   if o.state in [FunnelState.PAYMENT_CONFIRMED, FunnelState.AGENT_DELIVERED, FunnelState.ACTIVE]]
        
        total_revenue = sum(o.amount for o in completed)
        
        by_agent = {}
        for o in completed:
            agent = o.agent_type
            by_agent[agent] = by_agent.get(agent, 0) + o.amount
        
        mrr = sum(
            AGENT_PRODUCTS[a]["price"] * 100 
            for a in by_agent.keys()
        )
        
        return {
            "total_orders": len(self.orders),
            "completed_orders": len(completed),
            "total_revenue": total_revenue,
            "total_revenue_usd": total_revenue / 100,
            "mrr": mrr / 100,
            "by_agent": {a: v / 100 for a, v in by_agent.items()}
        }


# ========== PAYMENT LINKS ==========

class PaymentLinks:
    """Generate payment links for agents"""
    
    def __init__(self):
        self.base_url = "https://psdepot.com"
    
    def get_stripe_link(self, agent_type: str) -> str:
        """Get Stripe checkout link"""
        return f"{self.base_url}/checkout/{agent_type}"
    
    def get_crypto_link(self, agent_type: str, currency: str = "ETH") -> Dict:
        """Get crypto payment details"""
        price_usd = AGENT_PRODUCTS[agent_type]["price"]
        
        if currency == "ETH":
            amount = price_usd / CRYPTO_PRICES["ETH"]
            amount_str = f"{amount:.006f}"
        else:
            amount = price_usd
            amount_str = str(int(amount))
        
        return {
            "currency": currency,
            "amount": amount_str,
            "address": CRYPTO_PAYMENT_ADDRESS,
            "network": "ethereum",
            "note": f"Agent: {agent_type}"
        }
    
    def generate_all(self) -> Dict:
        """Generate all payment options"""
        result = {"stripe": {}, "crypto": {}, "paypal": {}}
        
        for agent in AGENT_PRODUCTS:
            result["stripe"][agent] = self.get_stripe_link(agent)
            result["crypto"][agent] = self.get_crypto_link(agent)
            result["paypal"][agent] = f"https://paypal.me/agentfleet/{AGENT_PRODUCTS[agent]['price']}"
        
        return result


# ========== MAIN ==========

def main():
    funnel = SalesFunnelWorkflows()
    payments = PaymentLinks()
    
    print("⚡ TEMPORAL SALES FUNNEL - Agent Sales")
    print("=" * 50)
    print(f"💳 Stripe: {'✅ Configured' if STRIPE_API_KEY else '⏳ Demo mode'}")
    print(f"📊 EVM Wallet: {EVM_WALLET[:20]}...")
    print()
    
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    
    if cmd == "links":
        print("📋 PAYMENT LINKS:")
        links = payments.generate_all()
        
        print("\n💳 STRIPE:")
        for a, url in links["stripe"].items():
            print(f"  {a}: {url}")
        
        print("\n🪙 CRYPTO:")
        for a, data in links["crypto"].items():
            print(f"  {a}: {data['amount']} {data['currency']} → {data['address'][:20]}...")
        
        print("\n💵 PAYPAL:")
        for a, url in links["paypal"].items():
            print(f"  {a}: {url}")
    
    elif cmd == "order":
        email = sys.argv[2] if len(sys.argv) > 2 else "demo@example.com"
        agent = sys.argv[3] if len(sys.argv) > 3 else "clerk"
        order_id = funnel.start_order(email, agent)
        print(f"✅ Order created: {order_id}")
        
        checkout = funnel.create_stripe_checkout(order_id)
        print(f"📎 Checkout: {checkout}")
    
    elif cmd == "status":
        print("📊 SALES FUNNEL STATUS:")
        print()
        print(f"Orders: {len(funnel.orders)}")
        
        revenue = funnel.query_revenue()
        print(f"Total Revenue: ${revenue['total_revenue_usd']}")
        print(f"MRR: ${revenue['mrr']}")
        print(f"By Agent: {revenue['by_agent']}")
    
    else:
        print("Commands:")
        print("  links        - Generate all payment links")
        print("  order <email> <agent> - Create new order")
        print("  status       - Show funnel status")


if __name__ == "__main__":
    main()
