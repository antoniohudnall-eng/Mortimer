/**
 * N'og nog Crew Communications v1.0
 * Email and Telegram integration for crew updates
 */

const nodemailer = require('nodemailer');
const EventEmitter = require('events');

class CrewComms extends EventEmitter {
    constructor(config = {}) {
        super();
        this.config = {
            email: {
                enabled: config.email?.enabled ?? true,
                smtp: {
                    host: config.email?.smtp?.host || process.env.SMTP_HOST,
                    port: config.email?.smtp?.port || 587,
                    secure: config.email?.smtp?.secure || false,
                    auth: {
                        user: config.email?.smtp?.user || process.env.SMTP_USER,
                        pass: config.email?.smtp?.pass || process.env.SMTP_PASS
                    }
                },
                from: config.email?.from || 'nog-crew@agi.company',
                captainEmail: config.email?.captain || process.env.CAPTAIN_EMAIL
            },
            telegram: {
                enabled: config.telegram?.enabled ?? true,
                botToken: config.telegram?.token || process.env.TELEGRAM_BOT_TOKEN,
                chatId: config.telegram?.chatId || process.env.TELEGRAM_CHAT_ID
            }
        };
        
        this.emailTransporter = null;
        this.telegramQueue = [];
        this.messageHistory = [];
    }
    
    async init() {
        console.log('[CrewComms] Initializing...');
        
        if (this.config.email.enabled && this.config.email.smtp.host) {
            await this.initEmail();
        }
        
        if (this.config.telegram.enabled && this.config.telegram.botToken) {
            await this.initTelegram();
        }
        
        console.log('[CrewComms] Ready');
    }
    
    async initEmail() {
        this.emailTransporter = nodemailer.createTransporter(this.config.email.smtp);
        
        try {
            await this.emailTransporter.verify();
            console.log('[CrewComms] Email transporter verified');
        } catch (err) {
            console.error('[CrewComms] Email verification failed:', err);
            this.config.email.enabled = false;
        }
    }
    
    async initTelegram() {
        // Setup Telegram bot polling
        this.telegramEnabled = true;
        console.log('[CrewComms] Telegram bot initialized');
        
        // Start polling for messages
        this.pollTelegram();
    }
    
    async pollTelegram() {
        if (!this.telegramEnabled) return;
        
        const url = `https://api.telegram.org/bot${this.config.telegram.botToken}/getUpdates`;
        
        try {
            const response = await fetch(url + (this.telegramOffset ? `?offset=${this.telegramOffset}` : ''));
            const data = await response.json();
            
            if (data.ok && data.result.length > 0) {
                for (const update of data.result) {
                    this.telegramOffset = update.update_id + 1;
                    await this.handleTelegramMessage(update);
                }
            }
        } catch (err) {
            console.error('[CrewComms] Telegram poll error:', err);
        }
        
        // Poll every 5 seconds
        setTimeout(() => this.pollTelegram(), 5000);
    }
    
    async handleTelegramMessage(update) {
        const message = update.message;
        if (!message) return;
        
        const text = message.text || message.caption || '';
        const chatId = message.chat.id;
        const from = message.from.username || message.from.first_name;
        
        // Store in history
        this.messageHistory.push({
            source: 'telegram',
            from,
            text,
            timestamp: Date.now(),
            hasPhoto: message.photo ? true : false
        });
        
        this.emit('telegram:message', {
            from,
            text,
            chatId,
            messageId: message.message_id,
            photo: message.photo
        });
        
        // Handle photos (crew sending pictures)
        if (message.photo && message.photo.length > 0) {
            const photo = message.photo[message.photo.length - 1]; // Largest size
            this.emit('telegram:photo', {
                from,
                photo,
                caption: text
            });
            
            // Download and save photo
            await this.downloadTelegramPhoto(photo.file_id, from);
        }
    }
    
    async downloadTelegramPhoto(fileId, from) {
        try {
            // Get file path
            const url = `https://api.telegram.org/bot${this.config.telegram.botToken}/getFile?file_id=${fileId}`;
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.ok) {
                const fileUrl = `https://api.telegram.org/file/bot${this.config.telegram.botToken}/${data.result.file_path}`;
                
                // Save to expeditions folder
                const fs = require('fs').promises;
                const path = require('path');
                const filename = `crew_${from}_${Date.now()}.jpg`;
                const filepath = path.join('/root/.openclaw/workspace/expeditions', filename);
                
                const imgResponse = await fetch(fileUrl);
                const buffer = await imgResponse.arrayBuffer();
                await fs.writeFile(filepath, Buffer.from(buffer));
                
                console.log(`[CrewComms] Saved photo from ${from}: ${filename}`);
                this.emit('photo:saved', { from, filename, path: filepath });
            }
        } catch (err) {
            console.error('[CrewComms] Photo download failed:', err);
        }
    }
    
    // Send email to captain
    async sendEmail(subject, html, priority = 'normal') {
        if (!this.config.email.enabled || !this.config.email.captainEmail) {
            console.log('[CrewComms] Email disabled or no captain email configured');
            return false;
        }
        
        const mailOptions = {
            from: this.config.email.from,
            to: this.config.email.captainEmail,
            subject: `[N'og nog Crew] ${subject}`,
            html,
            priority: priority === 'high' ? 'high' : 'normal'
        };
        
        try {
            const info = await this.emailTransporter.sendMail(mailOptions);
            console.log(`[CrewComms] Email sent: ${info.messageId}`);
            return true;
        } catch (err) {
            console.error('[CrewComms] Email send failed:', err);
            return false;
        }
    }
    
    // Send Telegram message
    async sendTelegram(text, options = {}) {
        if (!this.telegramEnabled || !this.config.telegram.chatId) {
            console.log('[CrewComms] Telegram disabled or no chat ID');
            return false;
        }
        
        const url = `https://api.telegram.org/bot${this.config.telegram.botToken}/sendMessage`;
        
        const body = {
            chat_id: this.config.telegram.chatId,
            text,
            parse_mode: 'HTML',
            ...options
        };
        
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            
            const data = await response.json();
            if (data.ok) {
                console.log('[CrewComms] Telegram sent');
                return true;
            }
        } catch (err) {
            console.error('[CrewComms] Telegram send failed:', err);
        }
        return false;
    }
    
    // Send crew report to captain
    async sendCrewReport(report, format = 'both') {
        const html = this.formatReportHtml(report);
        const text = this.formatReportText(report);
        
        const subject = `Crew Status Report - ${new Date().toLocaleDateString()}`;
        
        if (format === 'email' || format === 'both') {
            await this.sendEmail(subject, html);
        }
        
        if (format === 'telegram' || format === 'both') {
            await this.sendTelegram(text);
        }
    }
    
    formatReportHtml(report) {
        const timestamp = new Date(report.timestamp).toLocaleString();
        
        let html = `
            <h2>N'og nog Crew Report</h2>
            <p><strong>Time:</strong> ${timestamp}</p>
            
            <h3>Crew Summary</h3>
            <ul>
                <li>Total Crew: ${report.crewSummary.total}</li>
                <li>Active: ${report.crewSummary.active}</li>
                <li>Injured: ${report.crewSummary.injured}</li>
                <li>Resting: ${report.crewSummary.resting}</li>
                <li>By Role: ${JSON.stringify(report.crewSummary.byRole)}</li>
            </ul>
            
            <h3>Active Crew</h3>
            <table border="1" cellpadding="5">
                <tr>
                    <th>Name</th>
                    <th>Role</th>
                    <th>Level</th>
                    <th>Health</th>
                    <th>Location</th>
                    <th>Missions</th>
                </tr>
        `;
        
        for (const member of report.members) {
            html += `
                <tr>
                    <td>${member.name}</td>
                    <td>${member.role}</td>
                    <td>${member.level}</td>
                    <td>${member.health}</td>
                    <td>${member.location}</td>
                    <td>${member.missions}</td>
                </tr>
            `;
        }
        
        html += '</table>';
        
        if (report.highlights.length > 0) {
            html += '<h3>Recent Highlights</h3><ul>';
            for (const highlight of report.highlights) {
                html += `<li>${highlight}</li>`;
            }
            html += '</ul>';
        }
        
        return html;
    }
    
    formatReportText(report) {
        const timestamp = new Date(report.timestamp).toLocaleString();
        
        let text = `N'OG NOG CREW REPORT
${'='.repeat(40)}
Time: ${timestamp}

`;
        
        text += `CREW SUMMARY
`;
        text += `Total: ${report.crewSummary.total} | `;
        text += `Active: ${report.crewSummary.active} | `;
        text += `Injured: ${report.crewSummary.injured}\n\n`;
        
        text += `ACTIVE CREW:\n`;
        for (const member of report.members) {
            text += `${member.name} (${member.role}) - ${member.level}\n`;
            text += `  Health: ${member.health} | Location: ${member.location}\n`;
            text += `  Missions: ${member.missions} | Discoveries: ${member.discoveries}\n\n`;
        }
        
        if (report.highlights.length > 0) {
            text += `HIGHLIGHTS:\n`;
            for (const highlight of report.highlights) {
                text += `• ${highlight}\n`;
            }
        }
        
        return text;
    }
    
    // Send discovery alert
    async sendDiscoveryAlert(crewMember, discovery) {
        const subject = `Discovery: ${discovery.name || 'Unknown Anomaly'}`;
        const text = `${crewMember.name} has discovered ${discovery.name || 'something'} in ${discovery.location || 'unknown space'}!\n\n`;
        
        await this.sendTelegram(`🔭 <b>Discovery Alert!</b>\n\n${text}`, { parse_mode: 'HTML' });
        await this.sendEmail(subject, `<p>${text}</p>`, 'high');
    }
    
    // Send emergency alert
    async sendEmergencyAlert(crewMember, situation) {
        const text = `⚠️ <b>EMERGENCY</b>\n\n${crewMember.name} reports: ${situation}\n\nStatus: ${crewMember.status}\nHealth: ${crewMember.stats.health}/${crewMember.stats.maxHealth}`;
        
        await this.sendTelegram(text, { parse_mode: 'HTML' });
        await this.sendEmail('EMERGENCY - Crew Alert', `<p>${situation}</p>`, 'high');
    }
    
    // Get message history
    getHistory(limit = 50) {
        return this.messageHistory.slice(-limit);
    }
}

module.exports = CrewComms;