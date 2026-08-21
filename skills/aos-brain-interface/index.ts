import { WebSocket } from 'ws';

interface BrainConfig {
  brainHost: string;
  brainPort: number;
  timeoutMs: number;
}

interface BrainResponse {
  type: string;
  text?: string;
  tick?: number;
  nodes?: number;
  memory_clusters?: number;
  novelty?: number;
  phase?: string;
  timestamp?: number;
}

export class AOSBrainInterface {
  private config: BrainConfig;
  private ws: WebSocket | null = null;

  constructor(config: BrainConfig) {
    this.config = {
      brainHost: config.brainHost || 'localhost',
      brainPort: config.brainPort || 8765,
      timeoutMs: config.timeoutMs || 5000
    };
  }

  private async connect(): Promise<WebSocket> {
    return new Promise((resolve, reject) => {
      const wsUrl = `ws://${this.config.brainHost}:${this.config.brainPort}`;
      const ws = new WebSocket(wsUrl);

      const timeout = setTimeout(() => {
        ws.terminate();
        reject(new Error('Connection timeout'));
      }, this.config.timeoutMs);

      ws.on('open', () => {
        clearTimeout(timeout);
        resolve(ws);
      });

      ws.on('error', (err) => {
        clearTimeout(timeout);
        reject(err);
      });
    });
  }

  async queryBrain(query: string, context?: string): Promise<string> {
    try {
      this.ws = await this.connect();

      const message = {
        type: 'user_input',
        text: query,
        context: context || '',
        timestamp: Date.now(),
        source: 'openclaw_skill'
      };

      return new Promise((resolve, reject) => {
        const timeout = setTimeout(() => {
          this.ws?.terminate();
          reject(new Error('Query timeout'));
        }, this.config.timeoutMs);

        this.ws!.on('message', (data: WebSocket.Data) => {
          clearTimeout(timeout);
          try {
            const response: BrainResponse = JSON.parse(data.toString());
            if (response.type === 'response' && response.text) {
              resolve(response.text);
            } else if (response.type === 'welcome') {
              // Ignore welcome message, wait for actual response
              return;
            } else {
              resolve('Brain responded but no text content');
            }
          } catch (e) {
            resolve('Received non-JSON response from brain');
          }
        });

        this.ws!.on('error', (err) => {
          clearTimeout(timeout);
          reject(err);
        });

        this.ws!.send(JSON.stringify(message));
      });
    } catch (error) {
      return `Error connecting to AOS Brain: ${error.message}. Is the brain running?`;
    } finally {
      this.ws?.terminate();
    }
  }

  async getStatus(): Promise<BrainResponse | null> {
    try {
      this.ws = await this.connect();

      const message = {
        type: 'status_request',
        timestamp: Date.now()
      };

      return new Promise((resolve, reject) => {
        const timeout = setTimeout(() => {
          this.ws?.terminate();
          reject(new Error('Status request timeout'));
        }, this.config.timeoutMs);

        this.ws!.on('message', (data: WebSocket.Data) => {
          clearTimeout(timeout);
          try {
            const response: BrainResponse = JSON.parse(data.toString());
            if (response.type === 'status') {
              resolve(response);
            } else {
              resolve(null);
            }
          } catch (e) {
            resolve(null);
          }
        });

        this.ws!.on('error', () => {
          clearTimeout(timeout);
          resolve(null);
        });

        this.ws!.send(JSON.stringify(message));
      });
    } catch (error) {
      return null;
    } finally {
      this.ws?.terminate();
    }
  }

  async queryMemory(query: string, tier: string = 'all'): Promise<string> {
    // This would query the Hippocampus via the brain
    // For now, simplified version
    const response = await this.queryBrain(
      `Memory query: ${query} (tier: ${tier})`,
      'memory_retrieval'
    );
    return response;
  }
}

// Tool implementations for OpenClaw
export async function brainQuery(args: { query: string; context?: string }, config: BrainConfig): Promise<string> {
  const brain = new AOSBrainInterface(config);
  return await brain.queryBrain(args.query, args.context);
}

export async function brainStatus(args: {}, config: BrainConfig): Promise<string> {
  const brain = new AOSBrainInterface(config);
  const status = await brain.getStatus();
  
  if (!status) {
    return '❌ AOS Brain not responding. Check if brain is running: tmux list-sessions';
  }
  
  return `🧠 AOS Brain Status:
• Tick: ${status.tick}
• Nodes: ${status.nodes}
• Memory Clusters: ${status.memory_clusters}
• Novelty: ${status.novelty}
• Phase: ${status.phase}
• Personality: Miles (Active)`;
}

export async function brainMemory(args: { query: string; tier?: string }, config: BrainConfig): Promise<string> {
  const brain = new AOSBrainInterface(config);
  return await brain.queryMemory(args.query, args.tier || 'all');
}
