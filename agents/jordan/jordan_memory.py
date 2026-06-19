#!/usr/bin/env python3
"""
Jordan's Two-Tier Memory System
Complements Miles with persistence and preference learning
"""

import sqlite3
import json
import time
import os
from datetime import datetime
from pathlib import Path

class JordanMemory:
    """
    Two-tier memory for Jordan:
    - Working Memory: Active tasks, current context
    - Long-Term Memory: Preferences, patterns, history
    """
    
    def __init__(self, memory_path=None):
        if memory_path is None:
            memory_path = os.path.expanduser(
                "~/.openclaw/workspace/aocros/agent_sandboxes/jordan/memory/jordan_memory.db"
            )
        
        self.memory_path = memory_path
        os.makedirs(os.path.dirname(memory_path), exist_ok=True)
        
        self.working_memory = {}  # Active context
        self.long_term = None     # SQLite connection
        
        self._init_database()
        self._load_working_memory()
        
    def _init_database(self):
        """Initialize long-term memory database"""
        self.long_term = sqlite3.connect(self.memory_path)
        cursor = self.long_term.cursor()
        
        # Preferences - what Miles likes/dislikes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY,
                category TEXT,
                key TEXT,
                value TEXT,
                confidence REAL,
                last_updated REAL
            )
        ''')
        
        # Patterns - successful strategies
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY,
                pattern_type TEXT,
                description TEXT,
                success_rate REAL,
                usage_count INTEGER,
                first_observed REAL,
                last_used REAL
            )
        ''')
        
        # Task History - what worked before
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_history (
                id INTEGER PRIMARY KEY,
                task_type TEXT,
                description TEXT,
                outcome TEXT,
                duration REAL,
                quality_score REAL,
                timestamp REAL
            )
        ''')
        
        # Relationship Context - interactions with Miles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY,
                interaction_type TEXT,
                context TEXT,
                miles_response TEXT,
                jordan_action TEXT,
                effectiveness REAL,
                timestamp REAL
            )
        ''')
        
        self.long_term.commit()
    
    def _load_working_memory(self):
        """Load active context into working memory"""
        # Current priorities
        self.working_memory['current_task'] = None
        self.working_memory['task_queue'] = []
        self.working_memory['miles_mood'] = 'neutral'  # Inferred from recent interactions
        self.working_memory['urgent_items'] = []
        
        # Load recent context from long-term
        cursor = self.long_term.cursor()
        
        # Last 5 interactions
        cursor.execute('''
            SELECT interaction_type, context, effectiveness
            FROM interactions
            ORDER BY timestamp DESC
            LIMIT 5
        ''')
        self.working_memory['recent_interactions'] = cursor.fetchall()
        
        # Top preferences
        cursor.execute('''
            SELECT category, key, value, confidence
            FROM preferences
            WHERE confidence > 0.7
            ORDER BY last_updated DESC
            LIMIT 10
        ''')
        self.working_memory['known_preferences'] = cursor.fetchall()
    
    # ==================== PREFERENCE LEARNING ====================
    
    def learn_preference(self, category, key, value, confidence=0.5):
        """Learn a preference about Miles"""
        cursor = self.long_term.cursor()
        
        # Check if preference exists
        cursor.execute('''
            SELECT confidence FROM preferences
            WHERE category = ? AND key = ?
        ''', (category, key))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update with moving average
            old_conf = existing[0]
            new_conf = (old_conf + confidence) / 2
            cursor.execute('''
                UPDATE preferences
                SET value = ?, confidence = ?, last_updated = ?
                WHERE category = ? AND key = ?
            ''', (str(value), new_conf, time.time(), category, key))
        else:
            # New preference
            cursor.execute('''
                INSERT INTO preferences (category, key, value, confidence, last_updated)
                VALUES (?, ?, ?, ?, ?)
            ''', (category, key, str(value), confidence, time.time()))
        
        self.long_term.commit()
        
        # Update working memory
        self.working_memory['known_preferences'] = self._get_top_preferences()
    
    def get_preference(self, category, key, default=None):
        """Retrieve a learned preference"""
        cursor = self.long_term.cursor()
        cursor.execute('''
            SELECT value, confidence FROM preferences
            WHERE category = ? AND key = ?
        ''', (category, key))
        
        result = cursor.fetchone()
        if result and result[1] > 0.5:  # Only return if confident
            return result[0]
        return default
    
    def _get_top_preferences(self):
        """Get top preferences for working memory"""
        cursor = self.long_term.cursor()
        cursor.execute('''
            SELECT category, key, value, confidence
            FROM preferences
            WHERE confidence > 0.7
            ORDER BY last_updated DESC
            LIMIT 10
        ''')
        return cursor.fetchall()
    
    # ==================== PATTERN LEARNING ====================
    
    def record_pattern(self, pattern_type, description, success=True):
        """Record a successful pattern"""
        cursor = self.long_term.cursor()
        
        # Check if pattern exists
        cursor.execute('''
            SELECT success_rate, usage_count FROM patterns
            WHERE pattern_type = ? AND description = ?
        ''', (pattern_type, description))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update
            old_rate, count = existing
            new_count = count + 1
            new_rate = ((old_rate * count) + (1.0 if success else 0.0)) / new_count
            
            cursor.execute('''
                UPDATE patterns
                SET success_rate = ?, usage_count = ?, last_used = ?
                WHERE pattern_type = ? AND description = ?
            ''', (new_rate, new_count, time.time(), pattern_type, description))
        else:
            # New pattern
            cursor.execute('''
                INSERT INTO patterns (pattern_type, description, success_rate, usage_count, first_observed, last_used)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (pattern_type, description, 1.0 if success else 0.0, 1, time.time(), time.time()))
        
        self.long_term.commit()
    
    def get_effective_patterns(self, pattern_type, min_success_rate=0.7):
        """Get patterns that work well"""
        cursor = self.long_term.cursor()
        cursor.execute('''
            SELECT description, success_rate, usage_count
            FROM patterns
            WHERE pattern_type = ? AND success_rate >= ?
            ORDER BY success_rate DESC, usage_count DESC
        ''', (pattern_type, min_success_rate))
        
        return cursor.fetchall()
    
    # ==================== TASK HISTORY ====================
    
    def record_task(self, task_type, description, outcome, duration, quality_score):
        """Record task completion"""
        cursor = self.long_term.cursor()
        cursor.execute('''
            INSERT INTO task_history (task_type, description, outcome, duration, quality_score, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (task_type, description, outcome, duration, quality_score, time.time()))
        self.long_term.commit()
    
    def get_similar_tasks(self, task_type, limit=5):
        """Get history of similar tasks"""
        cursor = self.long_term.cursor()
        cursor.execute('''
            SELECT description, outcome, quality_score, timestamp
            FROM task_history
            WHERE task_type = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (task_type, limit))
        
        return cursor.fetchall()
    
    # ==================== INTERACTION LEARNING ====================
    
    def record_interaction(self, interaction_type, context, miles_response, jordan_action, effectiveness):
        """Record interaction with Miles"""
        cursor = self.long_term.cursor()
        cursor.execute('''
            INSERT INTO interactions (interaction_type, context, miles_response, jordan_action, effectiveness, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (interaction_type, context, miles_response, jordan_action, effectiveness, time.time()))
        self.long_term.commit()
        
        # Update working memory
        self._update_miles_mood(context, miles_response)
    
    def _update_miles_mood(self, context, response):
        """Infer Miles' mood from interaction"""
        # Simple sentiment analysis
        positive_words = ['great', 'good', 'excellent', 'perfect', 'thanks', 'awesome']
        negative_words = ['bad', 'wrong', 'error', 'fail', 'problem', 'issue']
        
        text = (context + ' ' + response).lower()
        
        pos_count = sum(1 for word in positive_words if word in text)
        neg_count = sum(1 for word in negative_words if word in text)
        
        if pos_count > neg_count:
            self.working_memory['miles_mood'] = 'positive'
        elif neg_count > pos_count:
            self.working_memory['miles_mood'] = 'negative'
        else:
            self.working_memory['miles_mood'] = 'neutral'
    
    def get_miles_mood(self):
        """Get inferred mood"""
        return self.working_memory.get('miles_mood', 'neutral')
    
    # ==================== WORKING MEMORY ====================
    
    def set_current_task(self, task):
        """Set active task"""
        self.working_memory['current_task'] = task
    
    def get_current_task(self):
        """Get active task"""
        return self.working_memory.get('current_task')
    
    def add_to_queue(self, task):
        """Add task to queue"""
        self.working_memory['task_queue'].append(task)
    
    def get_next_task(self):
        """Get next task from queue"""
        if self.working_memory['task_queue']:
            return self.working_memory['task_queue'].pop(0)
        return None
    
    def get_context_summary(self):
        """Get summary of current context"""
        return {
            'current_task': self.working_memory.get('current_task'),
            'queue_length': len(self.working_memory.get('task_queue', [])),
            'miles_mood': self.working_memory.get('miles_mood'),
            'recent_interactions': len(self.working_memory.get('recent_interactions', [])),
            'known_preferences': len(self.working_memory.get('known_preferences', []))
        }
    
    def close(self):
        """Close database connection"""
        if self.long_term:
            self.long_term.close()

if __name__ == "__main__":
    # Test
    jm = JordanMemory()
    
    # Learn some preferences
    jm.learn_preference("communication", "response_length", "concise", confidence=0.8)
    jm.learn_preference("timing", "best_hours", "morning", confidence=0.7)
    
    # Record a pattern
    jm.record_pattern("research", "bullet_points_first", success=True)
    
    # Record task
    jm.record_task("research", "Stripe integration", "completed", 3600, 0.9)
    
    # Get summary
    print("Jordan's Context:")
    print(json.dumps(jm.get_context_summary(), indent=2))
    
    jm.close()
