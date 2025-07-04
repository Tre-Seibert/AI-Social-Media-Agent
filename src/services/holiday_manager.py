"""
Holiday Manager module for detecting and managing holidays.
Handles holiday detection, weekday calculations, and holiday-specific content.
"""

from datetime import date, timedelta
from typing import Dict, Any, List
import random
from ..core.config import HOLIDAYS, HASHTAGS


class HolidayManager:
    """Manages holiday detection and holiday-specific content generation."""
    
    def __init__(self):
        self.holidays = HOLIDAYS
    
    def check_if_holiday(self, check_date: date | None = None) -> Dict[str, Any] | None:
        """Check if the given date (or today) is a holiday."""
        if check_date is None:
            check_date = date.today()
        
        current_month = check_date.month
        current_day = check_date.day
        current_weekday = check_date.strftime("%A").lower()
        
        # Check for exact date matches
        for holiday_key, holiday_info in self.holidays.items():
            holiday_date = holiday_info["date"]
            holiday_month, holiday_day = map(int, holiday_date.split("-"))
            
            # Check if it's an exact date match
            if current_month == holiday_month and current_day == holiday_day:
                return {
                    "key": holiday_key,
                    "name": holiday_info["name"],
                    "type": holiday_info["type"],
                    "date": check_date
                }
            
            # Check for weekday-based holidays (like "third Monday of January")
            if "weekday" in holiday_info:
                required_weekday = holiday_info["weekday"]
                if current_weekday == required_weekday:
                    if holiday_key == "martin_luther_king_day" and current_month == 1:
                        # MLK Day is the third Monday of January
                        if self._is_third_weekday_of_month(check_date, "monday"):
                            return {
                                "key": holiday_key,
                                "name": holiday_info["name"],
                                "type": holiday_info["type"],
                                "date": check_date
                            }
                    elif holiday_key == "presidents_day" and current_month == 2:
                        # Presidents' Day is the third Monday of February
                        if self._is_third_weekday_of_month(check_date, "monday"):
                            return {
                                "key": holiday_key,
                                "name": holiday_info["name"],
                                "type": holiday_info["type"],
                                "date": check_date
                            }
                    elif holiday_key == "memorial_day" and current_month == 5:
                        # Memorial Day is the last Monday of May
                        if self._is_last_weekday_of_month(check_date, "monday"):
                            return {
                                "key": holiday_key,
                                "name": holiday_info["name"],
                                "type": holiday_info["type"],
                                "date": check_date
                            }
                    elif holiday_key == "labor_day" and current_month == 9:
                        # Labor Day is the first Monday of September
                        if self._is_first_weekday_of_month(check_date, "monday"):
                            return {
                                "key": holiday_key,
                                "name": holiday_info["name"],
                                "type": holiday_info["type"],
                                "date": check_date
                            }
                    elif holiday_key == "columbus_day" and current_month == 10:
                        # Columbus Day is the second Monday of October
                        if self._is_second_weekday_of_month(check_date, "monday"):
                            return {
                                "key": holiday_key,
                                "name": holiday_info["name"],
                                "type": holiday_info["type"],
                                "date": check_date
                            }
                    elif holiday_key == "thanksgiving" and current_month == 11:
                        # Thanksgiving is the fourth Thursday of November
                        if self._is_fourth_weekday_of_month(check_date, "thursday"):
                            return {
                                "key": holiday_key,
                                "name": holiday_info["name"],
                                "type": holiday_info["type"],
                                "date": check_date
                            }
        
        return None
    
    def _is_third_weekday_of_month(self, check_date: date, weekday: str) -> bool:
        """Check if the date is the third occurrence of the specified weekday in the month."""
        weekday_num = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, 
                      "friday": 4, "saturday": 5, "sunday": 6}[weekday]
        
        first_day = date(check_date.year, check_date.month, 1)
        first_weekday = first_day.weekday()
        
        # Calculate the first occurrence of the target weekday
        days_until_first = (weekday_num - first_weekday) % 7
        first_occurrence = first_day + timedelta(days=days_until_first)
        
        # Third occurrence is 14 days after the first
        third_occurrence = first_occurrence + timedelta(days=14)
        
        return check_date == third_occurrence
    
    def _is_last_weekday_of_month(self, check_date: date, weekday: str) -> bool:
        """Check if the date is the last occurrence of the specified weekday in the month."""
        weekday_num = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, 
                      "friday": 4, "saturday": 5, "sunday": 6}[weekday]
        
        # Get the last day of the month
        if check_date.month == 12:
            last_day = date(check_date.year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(check_date.year, check_date.month + 1, 1) - timedelta(days=1)
        
        # Work backwards to find the last occurrence of the weekday
        while last_day.weekday() != weekday_num:
            last_day -= timedelta(days=1)
        
        return check_date == last_day
    
    def _is_first_weekday_of_month(self, check_date: date, weekday: str) -> bool:
        """Check if the date is the first occurrence of the specified weekday in the month."""
        weekday_num = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, 
                      "friday": 4, "saturday": 5, "sunday": 6}[weekday]
        
        first_day = date(check_date.year, check_date.month, 1)
        first_weekday = first_day.weekday()
        
        # Calculate the first occurrence of the target weekday
        days_until_first = (weekday_num - first_weekday) % 7
        first_occurrence = first_day + timedelta(days=days_until_first)
        
        return check_date == first_occurrence
    
    def _is_second_weekday_of_month(self, check_date: date, weekday: str) -> bool:
        """Check if the date is the second occurrence of the specified weekday in the month."""
        weekday_num = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, 
                      "friday": 4, "saturday": 5, "sunday": 6}[weekday]
        
        first_day = date(check_date.year, check_date.month, 1)
        first_weekday = first_day.weekday()
        
        # Calculate the first occurrence of the target weekday
        days_until_first = (weekday_num - first_weekday) % 7
        first_occurrence = first_day + timedelta(days=days_until_first)
        
        # Second occurrence is 7 days after the first
        second_occurrence = first_occurrence + timedelta(days=7)
        
        return check_date == second_occurrence
    
    def _is_fourth_weekday_of_month(self, check_date: date, weekday: str) -> bool:
        """Check if the date is the fourth occurrence of the specified weekday in the month."""
        weekday_num = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, 
                      "friday": 4, "saturday": 5, "sunday": 6}[weekday]
        
        first_day = date(check_date.year, check_date.month, 1)
        first_weekday = first_day.weekday()
        
        # Calculate the first occurrence of the target weekday
        days_until_first = (weekday_num - first_weekday) % 7
        first_occurrence = first_day + timedelta(days=days_until_first)
        
        # Fourth occurrence is 21 days after the first
        fourth_occurrence = first_occurrence + timedelta(days=21)
        
        return check_date == fourth_occurrence
    
    def get_holiday_hashtags(self, holiday_info: Dict[str, Any]) -> List[str]:
        """Get holiday-specific hashtags."""
        holiday_name = holiday_info['name']
        
        # Base holiday hashtags
        holiday_hashtags = [f"#{holiday_name.replace(' ', '').replace('-', '')}", f"#{holiday_name.replace(' ', '')}"]
        
        # Major holiday hashtags
        holiday_hashtags.extend(["#Holiday", "#Celebration", "#NationalHoliday"])
        
        return holiday_hashtags[:2]  # Limit to 2 holiday-specific hashtags
    
    def create_holiday_prompt(self, holiday_info: Dict[str, Any]) -> str:
        """Create a specific prompt for holiday posts."""
        holiday_name = holiday_info['name']
        
        base_context = f"""
        Company: Fishtown Web Design
        Location: Fishtown, Philadelphia
        Services: Custom Website Design, E-commerce Development, SEO Optimization, Website Maintenance, Mobile-First Design, Brand Identity Design, Digital Marketing
        Target Audience: Small businesses in Philadelphia, Blue collar businesses, like, plumbers, electricians, and HVAC technicians., Professional services, Startups and entrepreneurs, Non-profit organizations
        Brand Voice: Professional yet approachable, creative, community-focused, tech-savvy but human, philly based
        
        Today is {holiday_name}. Generate a holiday-themed post that celebrates this special day while being relevant to web design and local Philadelphia businesses.
        """
        
        return base_context + f"\n\nCelebrate {holiday_name} with a post that honors the significance of this national holiday while connecting it to web design and local business success."
    
    def create_holiday_image_prompt(self, holiday_info: Dict[str, Any], quality_settings: str) -> str:
        """Create a specific image prompt for holiday posts."""
        holiday_name = holiday_info['name']
        
        if "independence" in holiday_name.lower() or "july" in holiday_name.lower():
            return f"Professional photograph of American flag with modern web design elements subtly integrated. Clean, patriotic composition with red, white, and blue color scheme. {quality_settings}. Perfect for social media."
        elif "christmas" in holiday_name.lower():
            return f"Professional photograph of festive holiday decorations with modern web design elements subtly integrated. Clean, warm composition with holiday colors. {quality_settings}. Perfect for social media."
        elif "thanksgiving" in holiday_name.lower():
            return f"Professional photograph of warm, welcoming Thanksgiving elements with modern web design concepts subtly integrated. Clean, cozy composition with autumn colors. {quality_settings}. Perfect for social media."
        else:
            return f"Professional photograph of celebration elements with modern web design concepts subtly integrated. Clean, festive composition. {quality_settings}. Perfect for social media." 