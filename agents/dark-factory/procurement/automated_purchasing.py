#!/usr/bin/env python3
"""
Dark Factory Automated Purchasing System
Agent: Clerk (Inventory) + Ledger (Financial)
Purpose: API integrations for automated procurement
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import hashlib
import hmac

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AutoPurchasing")

class PurchaseStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    ORDERED = "ordered"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    INVOICED = "invoiced"
    PAID = "paid"
    CANCELLED = "cancelled"

class Priority(Enum):
    CRITICAL = 1  # Line-down risk
    HIGH = 2      # Safety stock breach
    MEDIUM = 3    # Planned replenishment
    LOW = 4       # Opportunistic buying

@dataclass
class PurchaseOrder:
    """Purchase order for equipment or consumables"""
    po_number: str
    supplier: str
    items: List[Dict]
    total_amount: float
    currency: str
    status: PurchaseStatus
    priority: Priority
    requested_by: str  # Agent name
    approved_by: Optional[str]
    created_at: str
    required_by: Optional[str]
    terms: str
    shipping_address: str
    api_response: Optional[Dict] = None

@dataclass
class SupplierIntegration:
    """Supplier API configuration"""
    name: str
    api_type: str  # "REST", "SOAP", "EDI", "OAUTH2"
    base_url: str
    auth_method: str  # "api_key", "oauth2", "bearer", "hmac"
    credentials: Dict
    endpoints: Dict[str, str]
    rate_limit: int  # requests per minute
    reliability_score: float

class AutomatedPurchasing:
    """
    Automated purchasing system for Dark Factory
    Integrates with supplier APIs, ERP systems, and payment gateways
    """
    
    def __init__(self, config_file: str = "purchasing_config.json"):
        self.config_file = config_file
        self.session: Optional[aiohttp.ClientSession] = None
        self.pending_orders: List[PurchaseOrder] = []
        self.completed_orders: List[PurchaseOrder] = []
        self.inventory_thresholds = self._load_thresholds()
        self.supplier_integrations = self._initialize_integrations()
        
    def _load_thresholds(self) -> Dict:
        """Load inventory reorder thresholds"""
        return {
            "spare_parts": {"min": 5, "optimal": 20},
            "consumables": {"min": 100, "optimal": 500},
            "safety_stock_days": 7,
            "max_lead_time_days": 30
        }
    
    def _initialize_integrations(self) -> Dict[str, SupplierIntegration]:
        """Initialize supplier API integrations"""
        integrations = {}
        
        # Siemens Industry Mall
        integrations["siemens"] = SupplierIntegration(
            name="Siemens Industry Mall",
            api_type="REST",
            base_url="https://mall.industry.siemens.com/api/v1",
            auth_method="oauth2",
            credentials={
                "client_id": os.getenv("SIEMENS_CLIENT_ID", ""),
                "client_secret": os.getenv("SIEMENS_CLIENT_SECRET", ""),
                "scope": "purchasing"
            },
            endpoints={
                "catalog": "/products",
                "pricing": "/pricing",
                "availability": "/stock",
                "order": "/orders",
                "tracking": "/shipments"
            },
            rate_limit=100,
            reliability_score=0.98
        )
        
        # Grainger
        integrations["grainger"] = SupplierIntegration(
            name="Grainger",
            api_type="REST",
            base_url="https://api.grainger.com/v1",
            auth_method="api_key",
            credentials={
                "api_key": os.getenv("GRAINGER_API_KEY", "")
            },
            endpoints={
                "search": "/products",
                "order": "/orders",
                "invoice": "/invoices"
            },
            rate_limit=200,
            reliability_score=0.95
        )
        
        # McMaster-Carr
        integrations["mcmaster"] = SupplierIntegration(
            name="McMaster-Carr",
            api_type="REST",
            base_url="https://api.mcmaster.com/v1",
            auth_method="api_key",
            credentials={
                "api_key": os.getenv("MCMASTER_API_KEY", "")
            },
            endpoints={
                "catalog": "/items",
                "order": "/orders",
                "tracking": "/shipments"
            },
            rate_limit=150,
            reliability_score=0.97
        )
        
        # Amazon Business
        integrations["amazon_business"] = SupplierIntegration(
            name="Amazon Business",
            api_type="REST",
            base_url="https://sellingpartnerapi-na.amazon.com",
            auth_method="oauth2",
            credentials={
                "client_id": os.getenv("AMAZON_CLIENT_ID", ""),
                "client_secret": os.getenv("AMAZON_CLIENT_SECRET", ""),
                "refresh_token": os.getenv("AMAZON_REFRESH_TOKEN", "")
            },
            endpoints={
                "catalog": "/catalog/2022-04-01/items",
                "orders": "/orders/v0/orders",
                "inventory": "/fba/inventory/v1/summaries"
            },
            rate_limit=60,
            reliability_score=0.93
        )
        
        # Digi-Key (for electronics/components)
        integrations["digikey"] = SupplierIntegration(
            name="Digi-Key",
            api_type="REST",
            base_url="https://api.digikey.com/products/v4",
            auth_method="oauth2",
            credentials={
                "client_id": os.getenv("DIGIKEY_CLIENT_ID", ""),
                "client_secret": os.getenv("DIGIKEY_CLIENT_SECRET", "")
            },
            endpoints={
                "search": "/search",
                "barcode": "/barcode",
                "order": "/order"
            },
            rate_limit=1000,
            reliability_score=0.99
        )
        
        return integrations
    
    async def __aenter__(self):
        """Async context manager"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup"""
        if self.session:
            await self.session.close()
    
    async def _make_api_request(
        self, 
        integration: SupplierIntegration, 
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict] = None
    ) -> Optional[Dict]:
        """Make authenticated API request to supplier"""
        url = f"{integration.base_url}{endpoint}"
        headers = {}
        
        # Authentication
        if integration.auth_method == "api_key":
            headers["X-API-Key"] = integration.credentials["api_key"]
        elif integration.auth_method == "bearer":
            headers["Authorization"] = f"Bearer {integration.credentials['token']}"
        elif integration.auth_method == "oauth2":
            token = await self._get_oauth_token(integration)
            headers["Authorization"] = f"Bearer {token}"
        
        headers["Content-Type"] = "application/json"
        
        try:
            if method == "GET":
                async with self.session.get(url, headers=headers) as resp:
                    if resp.status in [200, 201]:
                        return await resp.json()
                    else:
                        logger.error(f"API error {resp.status}: {await resp.text()}")
            elif method == "POST":
                async with self.session.post(url, headers=headers, json=data) as resp:
                    if resp.status in [200, 201]:
                        return await resp.json()
                    else:
                        logger.error(f"API error {resp.status}: {await resp.text()}")
        except Exception as e:
            logger.error(f"Request failed: {e}")
        
        return None
    
    async def _get_oauth_token(self, integration: SupplierIntegration) -> str:
        """Obtain OAuth2 token"""
        # Token caching would be implemented here
        token_url = f"{integration.base_url}/oauth/token"
        
        payload = {
            "grant_type": "client_credentials",
            "client_id": integration.credentials["client_id"],
            "client_secret": integration.credentials["client_secret"],
            "scope": integration.credentials.get("scope", "")
        }
        
        async with self.session.post(token_url, data=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("access_token", "")
        return ""
    
    async def check_inventory_availability(
        self, 
        supplier: str, 
        sku: str
    ) -> Dict:
        """Check real-time inventory availability"""
        integration = self.supplier_integrations.get(supplier)
        if not integration:
            return {"error": f"Unknown supplier: {supplier}"}
        
        endpoint = integration.endpoints.get("availability", "/stock")
        endpoint = f"{endpoint}?sku={sku}"
        
        result = await self._make_api_request(integration, endpoint)
        
        if result:
            return {
                "sku": sku,
                "available": result.get("quantity", 0),
                "warehouse": result.get("location", "Unknown"),
                "lead_time_days": result.get("lead_time", 7),
                "price": result.get("unit_price"),
                "currency": result.get("currency", "USD"),
                "timestamp": datetime.now().isoformat()
            }
        
        return {"error": "Failed to check availability"}
    
    async def compare_supplier_prices(
        self, 
        sku: str,
        suppliers: Optional[List[str]] = None
    ) -> List[Dict]:
        """Compare prices across multiple suppliers"""
        if not suppliers:
            suppliers = list(self.supplier_integrations.keys())
        
        tasks = [
            self.check_inventory_availability(sup, sku)
            for sup in suppliers
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_results = []
        for result in results:
            if isinstance(result, dict) and "error" not in result:
                valid_results.append(result)
        
        # Sort by price
        valid_results.sort(key=lambda x: x.get("price", float('inf')))
        
        return valid_results
    
    def generate_po_number(self, supplier: str) -> str:
        """Generate unique purchase order number"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        supplier_code = supplier[:3].upper()
        random_suffix = os.urandom(2).hex()
        return f"DF-{supplier_code}-{timestamp}-{random_suffix}"
    
    async def create_purchase_order(
        self,
        supplier: str,
        items: List[Dict],
        priority: Priority,
        requested_by: str,
        required_by: Optional[datetime] = None
    ) -> Optional[PurchaseOrder]:
        """
        Create and submit purchase order
        
        Args:
            supplier: Supplier name
            items: List of {"sku": str, "quantity": int, "unit_price": float}
            priority: Order priority
            requested_by: Agent requesting the order
            required_by: Date required
        """
        integration = self.supplier_integrations.get(supplier)
        if not integration:
            logger.error(f"Unknown supplier: {supplier}")
            return None
        
        # Calculate totals
        total = sum(item["quantity"] * item.get("unit_price", 0) for item in items)
        currency = items[0].get("currency", "USD") if items else "USD"
        
        # Create PO object
        po = PurchaseOrder(
            po_number=self.generate_po_number(supplier),
            supplier=supplier,
            items=items,
            total_amount=total,
            currency=currency,
            status=PurchaseStatus.PENDING,
            priority=priority,
            requested_by=requested_by,
            approved_by=None,
            created_at=datetime.now().isoformat(),
            required_by=required_by.isoformat() if required_by else None,
            terms="NET_30",
            shipping_address="Dark Factory - Zone 1 Receiving Dock",
            api_response=None
        )
        
        # Auto-approval for low-value orders
        approval_threshold = 5000  # USD
        if total < approval_threshold and priority.value >= Priority.MEDIUM.value:
            po.status = PurchaseStatus.APPROVED
            po.approved_by = "Ledger-Auto"
            logger.info(f"Auto-approved PO {po.po_number} (${total:,.2f})")
        else:
            logger.info(f"PO {po.po_number} pending approval (${total:,.2f})")
            self.pending_orders.append(po)
            return po
        
        # Submit to supplier API
        await self._submit_order_to_supplier(po, integration)
        
        return po
    
    async def _submit_order_to_supplier(
        self, 
        po: PurchaseOrder, 
        integration: SupplierIntegration
    ):
        """Submit order to supplier API"""
        endpoint = integration.endpoints.get("order", "/orders")
        
        order_data = {
            "po_number": po.po_number,
            "items": po.items,
            "shipping_address": po.shipping_address,
            "terms": po.terms,
            "priority": po.priority.name,
            "required_date": po.required_by
        }
        
        result = await self._make_api_request(
            integration, 
            endpoint, 
            method="POST", 
            data=order_data
        )
        
        if result:
            po.status = PurchaseStatus.ORDERED
            po.api_response = result
            self.completed_orders.append(po)
            logger.info(f"Order {po.po_number} submitted successfully")
            
            # Update inventory records
            await self._update_inventory_on_order(po)
        else:
            po.status = PurchaseStatus.CANCELLED
            logger.error(f"Failed to submit order {po.po_number}")
    
    async def _update_inventory_on_order(self, po: PurchaseOrder):
        """Update expected inventory records"""
        # Implementation would update internal inventory tracking
        for item in po.items:
            logger.info(f"Expected delivery: {item['sku']} x{item['quantity']} by {po.required_by}")
    
    async def track_shipment(self, supplier: str, tracking_number: str) -> Dict:
        """Track shipment status"""
        integration = self.supplier_integrations.get(supplier)
        if not integration:
            return {"error": "Unknown supplier"}
        
        endpoint = integration.endpoints.get("tracking", "/shipments")
        endpoint = f"{endpoint}/{tracking_number}"
        
        result = await self._make_api_request(integration, endpoint)
        
        if result:
            return {
                "tracking_number": tracking_number,
                "status": result.get("status"),
                "location": result.get("current_location"),
                "estimated_delivery": result.get("estimated_delivery"),
                "carrier": result.get("carrier"),
                "events": result.get("tracking_events", [])
            }
        
        return {"error": "Tracking information unavailable"}
    
    async def auto_replenish(
        self, 
        inventory_data: List[Dict],
        requested_by: str = "Clerk"
    ) -> List[PurchaseOrder]:
        """
        Automatically replenish inventory based on thresholds
        
        Args:
            inventory_data: List of {"sku": str, "current_qty": int, "reorder_point": int}
        """
        orders_created = []
        
        for item in inventory_data:
            current = item.get("current_qty", 0)
            reorder_point = item.get("reorder_point", 0)
            optimal = item.get("optimal_qty", reorder_point * 4)
            
            if current <= reorder_point:
                qty_to_order = optimal - current
                
                # Find best supplier
                sku = item["sku"]
                price_comparison = await self.compare_supplier_prices(sku)
                
                if price_comparison:
                    best_supplier = price_comparison[0]
                    supplier_name = best_supplier.get("supplier", "grainger")
                    
                    # Calculate urgency
                    days_until_stockout = current / item.get("daily_usage", 1) if item.get("daily_usage") else 30
                    priority = Priority.CRITICAL if days_until_stockout < 3 else Priority.HIGH
                    
                    # Create order
                    order_items = [{
                        "sku": sku,
                        "quantity": qty_to_order,
                        "unit_price": best_supplier.get("price", 0),
                        "currency": best_supplier.get("currency", "USD")
                    }]
                    
                    required_by = datetime.now() + timedelta(
                        days=best_supplier.get("lead_time_days", 7)
                    )
                    
                    po = await self.create_purchase_order(
                        supplier=supplier_name,
                        items=order_items,
                        priority=priority,
                        requested_by=requested_by,
                        required_by=required_by
                    )
                    
                    if po:
                        orders_created.append(po)
                        logger.info(f"Auto-replenishment order created: {po.po_number} for {sku}")
        
        return orders_created
    
    def get_procurement_report(self) -> Dict:
        """Generate procurement activity report"""
        return {
            "report_date": datetime.now().isoformat(),
            "pending_orders": len(self.pending_orders),
            "completed_orders": len(self.completed_orders),
            "total_spend": sum(po.total_amount for po in self.completed_orders),
            "pending_spend": sum(po.total_amount for po in self.pending_orders),
            "suppliers_used": list(set(po.supplier for po in self.completed_orders)),
            "critical_orders": len([po for po in self.pending_orders if po.priority == Priority.CRITICAL])
        }
    
    def export_orders_to_erp(self, filename: str = "erp_orders.json"):
        """Export orders to ERP-compatible format"""
        all_orders = self.pending_orders + self.completed_orders
        
        erp_data = {
            "export_date": datetime.now().isoformat(),
            "orders": [
                {
                    "po_number": po.po_number,
                    "supplier": po.supplier,
                    "total": po.total_amount,
                    "currency": po.currency,
                    "status": po.status.value,
                    "line_items": po.items
                }
                for po in all_orders
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(erp_data, f, indent=2)
        
        logger.info(f"Exported {len(all_orders)} orders to {filename}")


# Payment Gateway Integration
class PaymentGateway:
    """Handles automated payments for approved POs"""
    
    def __init__(self):
        self.supported_gateways = ["stripe", "dwolla", "plaid", "wise"]
    
    async def process_payment(
        self, 
        po: PurchaseOrder,
        gateway: str = "stripe"
    ) -> Dict:
        """Process payment for approved purchase order"""
        if gateway not in self.supported_gateways:
            return {"error": f"Unsupported gateway: {gateway}"}
        
        # Payment processing logic
        # This would integrate with actual payment APIs
        
        return {
            "po_number": po.po_number,
            "amount": po.total_amount,
            "currency": po.currency,
            "status": "processed",
            "transaction_id": f"TXN-{os.urandom(8).hex()}",
            "timestamp": datetime.now().isoformat()
        }


async def main():
    """Demo of automated purchasing system"""
    async with AutomatedPurchasing() as purchasing:
        # Simulate inventory data
        inventory = [
            {"sku": "SIEM-6ES7-321-1BL00-0AA0", "current_qty": 2, "reorder_point": 5, "optimal_qty": 20, "daily_usage": 0.5},
            {"sku": "GRA-5XRP1", "current_qty": 45, "reorder_point": 50, "optimal_qty": 200, "daily_usage": 10},
            {"sku": "MIS-MR-J4-10A", "current_qty": 1, "reorder_point": 3, "optimal_qty": 10, "daily_usage": 0.2},
        ]
        
        # Auto-replenish
        logger.info("=== Starting Auto-Replenishment ===")
        orders = await purchasing.auto_replenish(inventory)
        
        for order in orders:
            print(f"\nPO: {order.po_number}")
            print(f"  Supplier: {order.supplier}")
            print(f"  Amount: ${order.total_amount:,.2f}")
            print(f"  Status: {order.status.value}")
            print(f"  Priority: {order.priority.name}")
        
        # Generate report
        report = purchasing.get_procurement_report()
        print(f"\n=== Procurement Report ===")
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    asyncio.run(main())