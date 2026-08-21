import { generatePrivateKey, privateKeyToAccount } from 'viem/accounts';
import { writeFileSync, chmodSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

// Generate new wallet for Mortimer
const privateKey = generatePrivateKey();
const account = privateKeyToAccount(privateKey);

const wallet = {
  address: account.address,
  privateKey: privateKey,
  createdAt: new Date().toISOString(),
  owner: "Mortimer",
  purpose: "Multi-agent wallet operations"
};

const WALLET_PATH = join(homedir(), '.mortimer-evm-wallet.json');
writeFileSync(WALLET_PATH, JSON.stringify(wallet, null, 2), 'utf8');
chmodSync(WALLET_PATH, 0o600);

console.log(JSON.stringify({
  success: true,
  address: wallet.address,
  created_at: wallet.createdAt,
  path: WALLET_PATH,
  owner: "Mortimer"
}, null, 2));
