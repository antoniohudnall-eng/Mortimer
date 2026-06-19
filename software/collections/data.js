// Collections Data - Accounts Requiring Action
// Excludes paid accounts, includes only: Unpaid, Overdue, Draft, Canceled

const collectionAccounts = [
  // CRITICAL: >30 days overdue
  { date: '04/11/2026', customer: 'Emmanual', email: '', invoice: '000008', amount: 675.00, status: 'Overdue', days: 65, viewed: false, note: 'CONNECTION ISSUES - MICROSALE - HIGHEST PRIORITY', address: '1234 Tech Blvd, Los Angeles, CA 90012' },
  { date: '05/13/2026', customer: 'Fernando', email: '', invoice: '5126103', amount: 421.56, status: 'Overdue', days: 33, viewed: true, note: 'CRITICAL - Priority follow-up', address: '5678 Main Street, Los Angeles, CA 90012' },
  
  // Overdue (1-30 days)
  { date: '05/12/2026', customer: 'Becky NCC', email: '', invoice: '5126101', amount: 312.24, status: 'Overdue', days: 4, viewed: true, address: '9012 Newport Center Dr, Newport Beach, CA 92660' },
  { date: '05/07/2026', customer: 'Scott Walsh', email: '', invoice: '05056101', amount: 382.30, status: 'Overdue', days: 9, viewed: true, address: '3456 Van Ness Ave, Fresno, CA 93721' },
  { date: '05/07/2026', customer: 'Jen Yang SUPPLY ONLY', email: '', invoice: '4306104', amount: 520.86, status: 'Overdue', days: 10, viewed: true, address: '7890 Harbor Blvd, Anaheim, CA 92802' },
  { date: '05/05/2026', customer: 'Travis Hauffman', email: '', invoice: '4306102', amount: 163.24, status: 'Overdue', days: 11, viewed: true, address: '1234 Palm Canyon Dr, Palm Springs, CA 92264' },
  { date: '04/30/2026', customer: 'Heather Manager', email: '', invoice: '4276102', amount: 434.09, status: 'Overdue', days: 16, viewed: true, note: 'Courtesy invoice', address: '5678 Mission St, Sacramento, CA 95814' },
  { date: '04/22/2026', customer: 'Bo Thompson SUPPLY ONLY', email: '', invoice: '4166114', amount: 329.75, status: 'Overdue', days: 24, viewed: true, address: '9012 Broadway, Oakland, CA 94607' },
  { date: '04/23/2026', customer: 'Travis Hauffman', email: '', invoice: '4166108', amount: 242.67, status: 'Overdue', days: 26, viewed: true, address: '1234 Palm Canyon Dr, Palm Springs, CA 92264' },
  
  // Due Soon (Within 14 days) - Unpaid
  { date: '05/22/2026', customer: 'Katie Rondeau', email: '', invoice: '052226001', amount: 553.00, status: 'Unpaid', days: -6, viewed: true, note: 'ORDER # 639326', address: '5678 Beach Blvd, Huntington Beach, CA 92647' },
  { date: '05/20/2026', customer: 'Katie Rondeau', email: '', invoice: '052026001', amount: 178.00, status: 'Unpaid', days: -4, viewed: true, note: 'ORDER # 642281', address: '5678 Beach Blvd, Huntington Beach, CA 92647' },
  { date: '05/29/2026', customer: 'Cory Manager', email: '', invoice: '052226002', amount: 489.35, status: 'Unpaid', days: -6, viewed: true, address: '9012 El Camino Real, San Jose, CA 95129' },
  { date: '05/23/2026', customer: 'Michael General Manager', email: '', invoice: '052226003', amount: 386.90, status: 'Unpaid', days: -7, viewed: true, address: '3456 Wilshire Blvd, Beverly Hills, CA 90210' },
  { date: '05/26/2026', customer: 'Travis Hauffman', email: '', invoice: '052626001', amount: 149.90, status: 'Unpaid', days: -10, viewed: true, address: '1234 Palm Canyon Dr, Palm Springs, CA 92264' },
  { date: '05/26/2026', customer: 'Travis Hauffman', email: '', invoice: '052626002', amount: 149.90, status: 'Unpaid', days: -10, viewed: true, address: '1234 Palm Canyon Dr, Palm Springs, CA 92264' },
  { date: '05/27/2026', customer: 'Becky NCC', email: '', invoice: '052626006', amount: 249.14, status: 'Unpaid', days: -11, viewed: true, address: '5678 Fashion Island, Newport Beach, CA 92660' },
  { date: '06/11/2026', customer: 'Tony Salinas', email: '', invoice: '052626007', amount: 457.99, status: 'Unpaid', days: -13, viewed: true, address: '9012 Salinas Rd, Monterey, CA 93940' },
  { date: '06/02/2026', customer: 'Margarito General Manager', email: '', invoice: '060126001', amount: 512.41, status: 'Unpaid', days: -14, viewed: true, address: '3456 Alameda St, Oakland, CA 94607' },
  
  // Due in 2-4 weeks
  { date: '06/02/2026', customer: 'John', email: '', invoice: '060126003', amount: 161.22, status: 'Unpaid', days: -17, viewed: false, note: 'NOT VIEWED', address: '7890 Telegraph Ave, Berkeley, CA 94704' },
  { date: '06/02/2026', customer: 'Ema Kye', email: '', invoice: '060226004', amount: 150.36, status: 'Unpaid', days: -17, viewed: true, address: '1234 University Ave, Palo Alto, CA 94301' },
  { date: '06/02/2026', customer: 'Joycelin Magno', email: '', invoice: '060226003', amount: 230.93, status: 'Unpaid', days: -17, viewed: true, address: '5678 State St, Santa Barbara, CA 93101' },
  { date: '06/02/2026', customer: 'Renee', email: 'loscaporalestaqueria@outlook.com', invoice: '000015', amount: 360.45, status: 'Unpaid', days: -17, viewed: false, note: 'NOT VIEWED', address: '9012 3rd Street Promenade, Santa Monica, CA 90401' },
  { date: '06/08/2026', customer: 'Caffe Greco', email: '', invoice: '060826005', amount: 104.63, status: 'Unpaid', days: -23, viewed: true, address: '3456 Columbus Ave, San Francisco, CA 94133' },
  { date: '06/08/2026', customer: 'John Caine', email: '', invoice: '060826002', amount: 928.98, status: 'Unpaid', days: -23, viewed: true, address: '7890 Haight St, San Francisco, CA 94117' },
  
  // Draft items (need attention)
  { date: '05/13/2026', customer: 'Chris Davenport', email: '', invoice: '051326004', amount: 0.00, status: 'Draft', days: -33, viewed: false, note: 'Draft - Send now', address: '5678 Business Park, Irvine, CA 92618' },
  { date: '06/15/2026', customer: 'Hector CASIO', email: '', invoice: '6226102', amount: 0.00, status: 'Draft', days: -65, viewed: false, note: 'Draft - Send now', address: '9012 Commerce St, Commerce, CA 90040' },
  
  // Canceled items (for reference)
  { date: '05/20/2026', customer: 'Donato Owner', email: '', invoice: '051326009', amount: 606.67, status: 'Canceled', days: -26, viewed: false, note: 'Canceled on 05/20', address: '3456 Restaurant Row, San Diego, CA 92101' },
  { date: '05/11/2026', customer: 'Katie Fryxell', email: '', invoice: '4306101', amount: 99.16, status: 'Canceled', days: -35, viewed: true, note: 'Canceled on 05/29', address: '7890 Marina Blvd, Marina del Rey, CA 90292' },
  { date: '07/09/2025', customer: 'Don Tom La Torre', email: '', invoice: '000002', amount: 312.16, status: 'Canceled', days: -341, viewed: true, note: 'Canceled on 07/09/2025', address: '1234 La Torre Way, Los Angeles, CA 90012' }
];

// Summary statistics
const collectionStats = {
  totalOutstanding: collectionAccounts.reduce((sum, inv) => sum + inv.amount, 0),
  criticalCount: collectionAccounts.filter(i => i.days > 30 && i.status !== 'Draft' && i.status !== 'Canceled').length,
  overdueCount: collectionAccounts.filter(i => i.days > 0 && i.days <= 30).length,
  dueSoonCount: collectionAccounts.filter(i => i.days <= 0 && i.days >= -14).length,
  draftCount: collectionAccounts.filter(i => i.status === 'Draft' || i.status === 'Canceled').length
};

console.log('Collections data loaded:', collectionStats);
