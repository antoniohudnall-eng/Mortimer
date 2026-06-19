// Collections API Server - Node.js
// Serves data from SQLite database

const http = require('http');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const DB_PATH = '/root/.openclaw/workspace/datadepot/data/collections.db';
const PORT = 8085;

function getDb() {
    return new Promise((resolve, reject) => {
        const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READONLY, (err) => {
            if (err) {
                console.error('Database open error:', err);
                reject(err);
            } else {
                resolve(db);
            }
        });
    });
}

function queryDb(db, sql, params = []) {
    return new Promise((resolve, reject) => {
        db.all(sql, params, (err, rows) => {
            if (err) {
                reject(err);
            } else {
                resolve(rows);
            }
        });
    });
}

const server = http.createServer(async (req, res) => {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Content-Type', 'application/json');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    if (req.url === '/collections/api' || req.url === '/collections/api/') {
        try {
            const db = await getDb();
            const rows = await queryDb(db, `
                SELECT * FROM collections_accounts 
                WHERE status != 'paid' 
                ORDER BY days_overdue DESC, amount DESC
            `);
            
            db.close();

            const invoices = rows.map(row => ({
                date: row.invoice_date,
                customer: row.customer_name,
                email: row.email || '',
                invoice: row.invoice_number,
                amount: parseFloat(row.amount),
                status: row.status,
                days: parseInt(row.days_overdue || 0),
                viewed: !!row.viewed,
                note: row.notes || '',
                address: row.address || 'Address not on file - Click Edit to add',
                phone: row.phone || ''
            }));

            res.writeHead(200);
            res.end(JSON.stringify({
                success: true,
                count: invoices.length,
                invoices: invoices,
                lastUpdated: new Date().toISOString()
            }));

        } catch (err) {
            console.error('API Error:', err);
            res.writeHead(500);
            res.end(JSON.stringify({
                error: 'Database error: ' + err.message,
                fallback: true,
                invoices: []
            }));
        }
        return;
    }

    // 404 for other paths
    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Not found' }));
});

server.listen(PORT, () => {
    console.log(`Collections API running on port ${PORT}`);
    console.log(`Database: ${DB_PATH}`);
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received, shutting down');
    server.close(() => {
        process.exit(0);
    });
});
