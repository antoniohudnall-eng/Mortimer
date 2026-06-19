#!/usr/bin/env python3
"""
ENGAGEMENT & TRAFFIC DRIVER
===========================
Optimized content for maximum engagement and traffic

Features:
- Best posting times
- Engagement hooks
- Viral templates
- CTA optimization
- Traffic funnel integration
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

class EngagementOptimizer:
    """Optimize content for engagement and traffic"""
    
    # Best posting times (in user's timezone - assume PST)
    BEST_TIMES = {
        "x_com": [
            {"day": "Tue", "time": "9:00 AM PST", "engagement": "High"},
            {"day": "Wed", "time": "10:00 AM PST", "engagement": "High"},
            {"day": "Wed", "time": "2:00 PM PST", "engagement": "High"},
            {"day": "Thu", "time": "8:00 AM PST", "engagement": "Medium"},
            {"day": "Thu", "time": "11:00 AM PST", "engagement": "High"},
        ],
        "youtube": {
            "best_days": ["Tue", "Wed", "Thu"],
            "best_time": "3:00 PM PST",
            "worst_days": ["Sat", "Sun"],
        }
    }
    
    # Viral hooks that drive engagement
    VIRAL_HOOKS = {
        "controversial": [
            "Hot take: {}",
            "Unpopular opinion: {}",
            "The truth about {} nobody talks about",
            "Stop doing {} immediately",
        ],
        "curiosity": [
            "The {} secret that changed everything",
            "I tried {} for 30 days. Here's what happened.",
            "Nobody talks about {} until now",
            "This {} trick actually works",
        ],
        "numbers": [
            "{} things I learned from {}",
            "{} ways to { } in {} days",
            "{}% of people don't know this about {}",
            "{} signs you need {}",
        ],
        "story": [
            "I made {} in {} with {}",
            "The day I discovered {}",
            "My {} journey (week by week)",
            "From {} to {} in {} months",
        ],
    }
    
    # Traffic-driving elements
    TRAFFIC_ELEMENTS = {
        "urgency": ["Limited spots", "Only X left", "Ends soon", "Act now"],
        "curiosity_gaps": [
            "The method nobody teaches",
            "The real reason you're stuck",
            "What actually works (not the hype)",
        ],
        "social_proof": [
            "Used by {} businesses",
            "Trusted by {} executives",
            "Results in {} days",
        ],
        "value_preview": [
            "Free {} inside",
            "{} part 1 of 3",
            "Complete {} guide",
        ],
    }
    
    def optimize_for_engagement(self, post: str, platform: str = "x") -> dict:
        """Add engagement elements to post"""
        
        optimized = post.copy() if isinstance(post, dict) else {"content": post}
        
        # Add engagement score estimate
        content = optimized.get("content", "")
        
        # Check for engagement elements
        has_question = "?" in content
        has_emoji = any(e in content for e in ["🔥", "💡", "👇", "👆", "⬇️", "❓", "✅", "🏆"])
        has_number = any(c.isdigit() for c in content)
        has_cta = any(word in content.lower() for word in ["dm", "link", "comment", "drop", "subscribe", "follow"])
        has_controversy = any(word in content.lower() for word in ["truth", "stop", "nobody", "secret", "actually"])
        
        # Calculate engagement score (0-100)
        score = 30  # base
        if has_question: score += 15
        if has_emoji: score += 10
        if has_number: score += 15
        if has_cta: score += 20
        if has_controversy: score += 10
        
        optimized["engagement_score"] = min(score, 100)
        optimized["engagement_factors"] = {
            "has_question": has_question,
            "has_emoji": has_emoji,
            "has_number": has_number,
            "has_cta": has_cta,
            "has_controversy": has_controversy,
        }
        
        return optimized
    
    def generate_posting_schedule(self, num_posts: int = 10) -> list:
        """Generate optimal posting schedule"""
        
        schedule = []
        x_times = self.BEST_TIMES["x_com"]
        
        for i in range(num_posts):
            time_slot = x_times[i % len(x_times)]
            
            # Calculate date
            days_ahead = i // len(x_times)
            
            schedule.append({
                "post_number": i + 1,
                "day": time_slot["day"],
                "time": time_slot["time"],
                "engagement_expected": time_slot["engagement"],
                "content_type": self._get_content_type(i),
            })
        
        return schedule
    
    def _get_content_type(self, index: int) -> str:
        """Rotate content types for variety"""
        types = [
            "Stat-driven", "Pain-to-solution", "Story format",
            "Comparison", "Bold claim", "Question",
            "Trending topic", "ROI focus", "CTA style", "Curiosity"
        ]
        return types[index % len(types)]
    
    def add_traffic_elements(self, post: str) -> str:
        """Add traffic-driving elements"""
        
        elements = [
            f" ({self._random_choice(self.TRAFFIC_ELEMENTS['curiosity_gaps'])})",
            f"\n\n👇 Link in bio for more",
            f"\n\n📧 Free guide in my DMs",
        ]
        
        # Don't add if post is already long
        if len(post) > 200:
            return post
        
        return post + self._random_choice(elements)
    
    def _random_choice(self, options: list) -> str:
        import random
        return random.choice(options)
    
    def generate_viral_template(self, hook_type: str = "curiosity") -> str:
        """Generate a viral post template"""
        
        if hook_type not in self.VIRAL_HOOKS:
            hook_type = "curiosity"
        
        hooks = self.VIRAL_HOOKS[hook_type]
        hook = self._random_choice(hooks)
        
        templates = [
            f"{hook.format('AI agents')}...\n\nHere's what I learned:\n\n→ {hook.format('delegation')}\n→ {hook.format('automation')}\n\nDrop a 🔥 if you want part 2",
            
            f"{hook.format('building an AI team')}\n\n{the_funnel()}",
            
            f"{hook.format('hiring my first AI employee')}\n\n{the_funnel()}",
        ]
        
        return self._random_choice(templates)
    
    def generate_content_calendar(self, weeks: int = 2) -> dict:
        """Generate a multi-week content calendar"""
        
        calendar = {
            "calendar_id": f"CAL_{datetime.now().strftime('%Y%m%d')}",
            "weeks": weeks,
            "schedule": [],
        }
        
        # Week structure
        for week in range(weeks):
            week_num = week + 1
            week_content = {
                "week": week_num,
                "theme": self._get_week_theme(week),
                "posts": [],
            }
            
            # 7 posts per week
            for day in range(7):
                post_type = self._get_daily_post_type(day)
                
                week_content["posts"].append({
                    "day": day + 1,
                    "post_type": post_type,
                    "time": self.BEST_TIMES["x_com"][day % len(self.BEST_TIMES["x_com"])]["time"],
                    "hook_type": self._get_hook_type(day),
                })
            
            calendar["schedule"].append(week_content)
        
        return calendar
    
    def _get_week_theme(self, week: int) -> str:
        themes = [
            "AI Agent Introduction",
            "ROI & Results",
            "Pain Points & Solutions",
            "Social Proof & Testimonials",
        ]
        return themes[week % len(themes)]
    
    def _get_daily_post_type(self, day: int) -> str:
        types = [
            "Educational", "Stat-driven", "Story",
            "Comparison", "CTA", "Engagement", "Testimonial",
        ]
        return types[day % len(types)]
    
    def _get_hook_type(self, day: int) -> str:
        hooks = ["curiosity", "controversial", "numbers", "story"]
        return hooks[day % len(hooks)]
    
    def print_engagement_report(self, posts: list):
        """Print engagement optimization report"""
        
        print("\n" + "="*70)
        print("📊 ENGAGEMENT OPTIMIZATION REPORT")
        print("="*70)
        
        for post in posts[:5]:  # Show top 5
            score = post.get("engagement_score", 0)
            factors = post.get("engagement_factors", {})
            
            bar = "█" * (score // 5) + "░" * (20 - score // 5)
            
            print(f"\n📝 Post: {post.get('id', 'N/A')}")
            print(f"   Score: [{bar}] {score}%")
            print(f"   ✅ Question" if factors.get('has_question') else "   ❓ No question")
            print(f"   ✅ Emoji" if factors.get('has_emoji') else "   💭 No emoji")
            print(f"   ✅ Number" if factors.get('has_number') else "   🔢 No number")
            print(f"   ✅ CTA" if factors.get('has_cta') else "   📢 No CTA")
            print(f"   ✅ Controversy" if factors.get('has_controversy') else "   😴 No controversy")
        
        print("\n" + "="*70)
        print("📅 RECOMMENDED POSTING TIMES")
        print("="*70)
        for slot in self.BEST_TIMES["x_com"]:
            print(f"   {slot['day']} @ {slot['time']} — {slot['engagement']}")
        
        print("\n" + "="*70)


def the_funnel() -> str:
    """Traffic funnel template"""
    return """
👇 Link in bio to get your AI agent

→ Free consultation
→ Pick your plan ($99-$1,299/mo)
→ Launch in 24 hours
"""


def main():
    """Run engagement optimizer"""
    
    optimizer = EngagementOptimizer()
    
    # Generate optimized posts
    from social_media_generator import SocialMediaGenerator
    
    gen = SocialMediaGenerator()
    posts = gen.generate_x_posts(10)
    
    # Optimize each post
    optimized = []
    for post in posts:
        opt = optimizer.optimize_for_engagement(post)
        optimized.append(opt)
    
    # Print report
    optimizer.print_engagement_report(optimized)
    
    # Generate content calendar
    calendar = optimizer.generate_content_calendar(2)
    
    print("\n📅 2-WEEK CONTENT CALENDAR")
    print("="*70)
    for week in calendar["schedule"]:
        print(f"\n📆 WEEK {week['week']}: {week['theme']}")
        for post in week["posts"]:
            print(f"   Day {post['day']}: {post['post_type']} ({post['hook_type']}) @ {post['time']}")
    
    print("\n✅ Engagement optimization complete!")


if __name__ == "__main__":
    main()
