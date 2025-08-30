import re
import textstat
import google.generativeai as genai
import os
from collections import Counter
from dotenv import load_dotenv

load_dotenv()

class SocialMediaAnalyzer:
    def __init__(self):
        self.platforms = {
            'twitter': {'max_chars': 280, 'optimal_hashtags': 2},
            'instagram': {'max_chars': 2200, 'optimal_hashtags': 5},
            'facebook': {'max_chars': 63206, 'optimal_hashtags': 3},
            'linkedin': {'max_chars': 3000, 'optimal_hashtags': 3}
        }
        
        # Setup Gemini
        try:
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY'))
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("✅ Gemini API initialized successfully")
        except Exception as e:
            print(f"❌ Gemini API initialization failed: {e}")
            self.model = None
    
    def analyze_content(self, text):
        """Comprehensive content analysis"""
        print(f"🔍 Starting analysis for text: {text[:50]}...")
        
        if not text or not text.strip():
            return {'error': 'No text provided for analysis'}
        
        try:
            # Basic metrics
            print("📊 Calculating basic metrics...")
            metrics = self._calculate_basic_metrics(text)
            
            # Social media specific analysis
            print("📱 Analyzing social elements...")
            social_analysis = self._analyze_social_elements(text)
            
            # Readability analysis
            print("📖 Analyzing readability...")
            readability = self._analyze_readability(text)
            
            # Generate suggestions
            print("💡 Generating suggestions...")
            suggestions = self._generate_suggestions(metrics, social_analysis, readability)
            
            # AI suggestions
            print("🤖 Getting AI suggestions...")
            ai_suggestions = self._get_ai_suggestions(text) if self.model else "Gemini API not available"
            
            print(f"✅ Analysis completed successfully!")
            
            return {
                'metrics': metrics,
                'social_analysis': social_analysis,
                'readability': readability,
                'suggestions': suggestions,
                'ai_suggestions': ai_suggestions,
                'platform_analysis': self._analyze_for_platforms(text)
            }
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return {
                'error': f'Analysis failed: {str(e)}',
                'suggestions': [],
                'ai_suggestions': 'Analysis error occurred'
            }
    
    def _get_ai_suggestions(self, text):
        """Get AI suggestions"""
        if not self.model:
            return "Gemini API not configured"
            
        try:
            prompt = f"""Analyze this social media content and give 3-5 specific suggestions to improve engagement:

Content: "{text}"

Give suggestions in this format:
1. [Specific suggestion]
2. [Specific suggestion]
3. [Specific suggestion]

Focus on: hashtags, call-to-action, emotional appeal, formatting, and audience engagement."""
            
            print("📡 Sending request to Gemini API...")
            response = self.model.generate_content(prompt)
            print(f"✅ AI response received: {len(response.text)} characters")
            return response.text
            
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            return f"AI suggestions unavailable: {str(e)}"
    
    def _calculate_basic_metrics(self, text):
        """Calculate basic text metrics"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return {
            'character_count': len(text),
            'character_count_no_spaces': len(text.replace(' ', '')),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_words_per_sentence': round(len(words) / len(sentences), 2) if sentences else 0,
            'avg_chars_per_word': round(len(text.replace(' ', '')) / len(words), 2) if words else 0
        }
    
    def _analyze_social_elements(self, text):
        """Analyze social media specific elements"""
        hashtags = re.findall(r'#\w+', text)
        mentions = re.findall(r'@\w+', text)
        urls = re.findall(r'https?://[^\s]+', text)
        
        # emoji detection
        emojis = []
        common_emojis = ['😀', '😁', '😂', '🤣', '😃', '😄', '😅', '😆', '😉', '😊', '😋', '😎', '😍', '😘', '🥰', '😗', '😙', '😚', '🙂', '🤗', '🤩', '🤔', '🤨', '😐', '😑', '😶', '🙄', '😏', '😣', '😥', '😮', '🤐', '😯', '😪', '😫', '😴', '😌', '😛', '😜', '😝', '🤤', '😒', '😓', '😔', '😕', '🙃', '🤑', '😲', '🙁', '😖', '😞', '😟', '😤', '😢', '😭', '😦', '😧', '😨', '😩', '🤯', '😬', '😰', '😱', '🥵', '🥶', '😳', '🤪', '😵', '😡', '😠', '🤬', '😷', '🤒', '🤕', '🤢', '🤮', '🤧', '😇', '🥳', '🥴', '🥺', '🤠', '🤡', '🤥', '🤫', '🤭', '🧐', '🤓', '😈', '👿', '👹', '👺', '💀', '👻', '👽', '🤖', '💩', '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔', '❣️', '💕', '💖', '💗', '💘', '💝', '💟', '♥️', '💌', '💤', '💢', '💣', '💥', '💦', '💨', '💫', '💬', '👁️‍🗨️', '🗨️', '🗯️', '💭', '💮', '♨️', '💈', '🛑', '🕛', '🕧', '🕐', '🕜', '🕑', '🕝', '🕒', '🕞', '🕓', '🕟', '🕔', '🕠', '🕕', '🕡', '🕖', '🕢', '🕗', '🕣', '🕘', '🕤', '🕙', '🕥', '🕚', '🕦', '🌍', '🌎', '🌏', '🌐', '🗺️', '🗾', '🧭', '🏔️', '⛰️', '🌋', '🗻', '🏕️', '🏖️', '🏜️', '🏝️', '🏞️', '🏟️', '🏛️', '🏗️', '🧱', '🏘️', '🏚️', '🏠', '🏡', '🏢', '🏣', '🏤', '🏥', '🏦', '🏨', '🏩', '🏪', '🏫', '🏬', '🏭', '🏯', '🏰', '🗼', '🗽', '⛪', '🕌', '🛕', '🕍', '⛩️', '🕋', '⛲', '⛺', '🌁', '🌃', '🏙️', '🌄', '🌅', '🌆', '🌇', '🌉', '♨️', '🎠', '🎡', '🎢', '💈', '🎪', '🚂', '🚃', '🚄', '🚅', '🚆', '🚇', '🚈', '🚉', '🚊', '🚝', '🚞', '🚋', '🚌', '🚍', '🚎', '🚐', '🚑', '🚒', '🚓', '🚔', '🚕', '🚖', '🚗', '🚘', '🚙', '🚚', '🚛', '🚜', '🏎️', '🏍️', '🛵', '🦽', '🦼', '🛴', '🚲', '🛺', '🚨', '🚔', '🚍', '🚘', '🚖', '🚡', '🚠', '🚟', '🚃', '🚋', '🚞', '🚝', '🚄', '🚅', '🚈', '🚂', '🚆', '🚇', '🚊', '🚉', '✈️', '🛫', '🛬', '🛩️', '💺', '🛰️', '🚀', '🛸', '🚁', '🛶', '⛵', '🚤', '🛥️', '🛳️', '⛴️', '🚢', '⚓', '⛽', '🚧', '🚦', '🚥', '🚏', '🗺️', '🗿', '🗽', '🗼', '🏰', '🏯', '🏟️', '🎡', '🎢', '🎠', '⛲', '⛱️', '🏖️', '🏝️', '🏜️', '🌋', '⛰️', '🏔️', '🗻', '🏕️', '⛺', '🏠', '🏡', '🏘️', '🏚️', '🏗️', '🏭', '🏢', '🏬', '🏣', '🏤', '🏥', '🏦', '🏨', '🏪', '🏫', '🏩', '💒', '🏛️', '⛪', '🕌', '🕍', '🛕', '🕋', '⛩️', '🛤️', '🛣️', '🗾', '🎑', '🏞️', '🌅', '🌄', '🌠', '🎇', '🎆', '🌇', '🌆', '🏙️', '🌃', '🌌', '🌉', '🌁']
        
        for emoji in common_emojis:
            if emoji in text:
                emojis.append(emoji)
        
        # Question marks and exclamations
        questions = len(re.findall(r'\?', text))
        exclamations = len(re.findall(r'!', text))
        
        # Call-to-action words
        cta_words = ['click', 'share', 'comment', 'like', 'follow', 'subscribe', 
                    'buy', 'learn', 'discover', 'explore', 'join', 'sign up', 'check out', 'visit', 'download']
        cta_count = sum(1 for word in cta_words if word.lower() in text.lower())
        
        return {
            'hashtags': {'count': len(hashtags), 'list': hashtags},
            'mentions': {'count': len(mentions), 'list': mentions},
            'urls': {'count': len(urls), 'list': urls},
            'emojis': {'count': len(emojis), 'list': list(set(emojis))},  # Remove duplicates
            'questions': questions,
            'exclamations': exclamations,
            'cta_elements': cta_count
        }
    
    def _analyze_readability(self, text):
        """Analyze text readability"""
        try:
            return {
                'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),  # Fixed method name
                'flesch_reading_ease': textstat.flesch_reading_ease(text),
                'automated_readability_index': textstat.automated_readability_index(text),
                'coleman_liau_index': textstat.coleman_liau_index(text),
                'reading_time_minutes': round(len(text.split()) / 200, 1)  # 200 WPM average
            }
        except Exception as e:
            print(f"⚠️ Readability analysis failed: {e}")
            return {
                'flesch_kincaid_grade': 0,
                'flesch_reading_ease': 0,
                'automated_readability_index': 0,
                'coleman_liau_index': 0,
                'reading_time_minutes': round(len(text.split()) / 200, 1)
            }
    
    def _generate_suggestions(self, metrics, social_analysis, readability):
        """Generate improvement suggestions"""
        suggestions = []
        
        # Length suggestions
        if metrics['word_count'] > 50:
            suggestions.append({
                'type': 'Length Optimization',
                'priority': 'high',
                'suggestion': 'Consider shortening your content. Social media posts perform better with 20-50 words.',
                'action': f"Current: {metrics['word_count']} words. Try reducing to under 50 words."
            })
        elif metrics['word_count'] < 5:
            suggestions.append({
                'type': 'Length Optimization',
                'priority': 'medium',
                'suggestion': 'Your post is very short. Add more context to engage your audience.',
                'action': f"Current: {metrics['word_count']} words. Try adding 10-20 more words for better engagement."
            })
        
        # Hashtag suggestions
        if social_analysis['hashtags']['count'] == 0:
            suggestions.append({
                'type': 'Hashtag Strategy',
                'priority': 'high',
                'suggestion': 'Add 3-5 relevant hashtags to increase discoverability.',
                'action': 'Research trending hashtags in your niche and add them strategically.'
            })
        elif social_analysis['hashtags']['count'] > 10:
            suggestions.append({
                'type': 'Hashtag Strategy',
                'priority': 'medium',
                'suggestion': 'Too many hashtags can look spammy.',
                'action': f"Current: {social_analysis['hashtags']['count']} hashtags. Reduce to 3-5 high-quality ones."
            })
        
        # Engagement suggestions
        if social_analysis['questions'] == 0 and social_analysis['exclamations'] == 0:
            suggestions.append({
                'type': 'Engagement',
                'priority': 'high',
                'suggestion': 'Add a question or exclamation to encourage interaction.',
                'action': 'End your post with "What do you think?" or add excitement with exclamation marks!'
            })
        
        # CTA suggestions
        if social_analysis['cta_elements'] == 0:
            suggestions.append({
                'type': 'Call to Action',
                'priority': 'high',
                'suggestion': 'Include a clear call-to-action to guide your audience.',
                'action': 'Add phrases like "Share your thoughts", "Follow for more", or "Click the link".'
            })
        
        # Emoji suggestions
        if social_analysis['emojis']['count'] == 0:
            suggestions.append({
                'type': 'Visual Appeal',
                'priority': 'medium',
                'suggestion': 'Add 1-2 relevant emojis to make your post more visually appealing.',
                'action': 'Choose emojis that match your content tone and message.'
            })
        elif social_analysis['emojis']['count'] > 5:
            suggestions.append({
                'type': 'Visual Appeal',
                'priority': 'low',
                'suggestion': 'Too many emojis can be distracting.',
                'action': f"Current: {social_analysis['emojis']['count']} emojis. Consider reducing to 2-3."
            })
        
        # Readability suggestions
        if readability.get('flesch_reading_ease', 0) < 60:
            suggestions.append({
                'type': 'Readability',
                'priority': 'medium',
                'suggestion': 'Content may be too complex for social media.',
                'action': 'Use simpler words and shorter sentences for better engagement.'
            })
        
        return suggestions
    
    def _analyze_for_platforms(self, text):
        """Analyze content suitability for different platforms"""
        char_count = len(text)
        analysis = {}
        
        for platform, limits in self.platforms.items():
            analysis[platform] = {
                'suitable': char_count <= limits['max_chars'],
                'char_usage': f"{char_count}/{limits['max_chars']}",
                'char_percentage': round((char_count / limits['max_chars']) * 100, 1),
                'recommendation': self._get_platform_recommendation(platform, char_count, limits)
            }
        
        return analysis
    
    def _get_platform_recommendation(self, platform, char_count, limits):
        """Get platform-specific recommendations"""
        if char_count <= limits['max_chars']:
            if char_count <= limits['max_chars'] * 0.5:  # Less than 50% of limit
                return f"✅ Perfect for {platform.capitalize()} - Good length"
            else:
                return f"✅ Suitable for {platform.capitalize()}"
        else:
            excess = char_count - limits['max_chars']
            return f"❌ Too long for {platform.capitalize()} by {excess} characters"