import random
from typing import Dict, List, Any

class EconomySystem:
    """
    Handles all economic calculations and simulations for the game.
    This includes GDP growth, trade relationships, sanctions, and financial markets.
    """
    
    def __init__(self):
        self.base_growth_rate = 0.025  # 2.5% annual growth
        self.max_growth_rate = 0.10    # 10% max growth
        self.min_growth_rate = -0.05   # -5% recession
        
        # Trade impact factors
        self.trade_boost_factor = 0.02  # Each trade partner can boost GDP by up to 2%
        self.sanction_penalty_factor = 0.03  # Each sanction can reduce GDP by up to 3%
        
    def calculate_gdp_growth(self, nation: Dict[str, Any], world_state: Dict[str, Any]) -> float:
        """
        Calculate the GDP growth for a nation based on various factors:
        - Base growth rate
        - Trade relationships
        - Sanctions
        - Research investments
        - Random events
        
        Args:
            nation: Dictionary containing nation data
            world_state: Dictionary containing global game state
            
        Returns:
            float: Growth rate as a decimal (e.g., 0.03 for 3% growth)
        """
        # Start with base growth rate
        growth_rate = self.base_growth_rate
        
        # Adjust for nation's economic policies
        tax_rate = nation.get('tax_rate', 0.25)
        research_spending = nation.get('research_spending', 0.05)
        
        # Higher taxes reduce growth, but research spending increases it
        growth_rate -= (tax_rate - 0.25) * 0.1  # Penalty for taxes above 25%
        growth_rate += research_spending * 0.2  # Bonus for research spending
        
        # Adjust for trade relationships
        trade_partners = self._get_trade_partners(nation, world_state)
        growth_rate += len(trade_partners) * self.trade_boost_factor * random.uniform(0.5, 1.0)
        
        # Adjust for sanctions
        sanctions = self._get_sanctions(nation, world_state)
        growth_rate -= len(sanctions) * self.sanction_penalty_factor * random.uniform(0.7, 1.0)
        
        # Add random factor (-1% to +1%)
        growth_rate += random.uniform(-0.01, 0.01)
        
        # Ensure growth rate is within bounds
        growth_rate = max(self.min_growth_rate, min(growth_rate, self.max_growth_rate))
        
        return growth_rate
    
    def update_gdp(self, nation: Dict[str, Any], world_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a nation's GDP based on calculated growth rate.
        
        Args:
            nation: Dictionary containing nation data
            world_state: Dictionary containing global game state
            
        Returns:
            Dict: Updated nation dictionary
        """
        growth_rate = self.calculate_gdp_growth(nation, world_state)
        current_gdp = nation.get('gdp', 0)
        
        # Calculate new GDP
        new_gdp = current_gdp * (1 + growth_rate)
        
        # Update nation dictionary
        updated_nation = nation.copy()
        updated_nation['gdp'] = new_gdp
        updated_nation['gdp_growth_rate'] = growth_rate
        
        return updated_nation
    
    def calculate_trade_impact(self, nation1: Dict[str, Any], nation2: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate the economic impact of trade between two nations.
        
        Args:
            nation1: First nation
            nation2: Second nation
            
        Returns:
            Dict: Economic impact for both nations
        """
        # Calculate trade volume based on GDP sizes
        gdp1 = nation1.get('gdp', 0)
        gdp2 = nation2.get('gdp', 0)
        
        # Trade volume is proportional to the smaller GDP
        smaller_gdp = min(gdp1, gdp2)
        trade_volume = smaller_gdp * random.uniform(0.05, 0.15)  # 5-15% of smaller GDP
        
        # Calculate benefit for each nation (smaller economies benefit more)
        benefit1 = trade_volume / gdp1 * random.uniform(0.8, 1.2)
        benefit2 = trade_volume / gdp2 * random.uniform(0.8, 1.2)
        
        return {
            'nation1_benefit': benefit1,
            'nation2_benefit': benefit2,
            'trade_volume': trade_volume
        }
    
    def apply_sanction(self, from_nation: Dict[str, Any], to_nation: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate the economic impact of sanctions.
        
        Args:
            from_nation: Nation imposing sanctions
            to_nation: Nation being sanctioned
            
        Returns:
            Dict: Economic impact for both nations
        """
        # Sanctions hurt both nations, but the sanctioned nation more
        from_gdp = from_nation.get('gdp', 0)
        to_gdp = to_nation.get('gdp', 0)
        
        # Calculate sanction impact
        sanction_impact = min(from_gdp, to_gdp) * random.uniform(0.01, 0.05)
        
        # Larger economies can impose more damaging sanctions
        power_ratio = from_gdp / to_gdp if to_gdp > 0 else 10.0
        power_factor = min(power_ratio, 10.0) / 10.0  # Normalize to 0-1
        
        # Calculate damage to each nation
        damage_to_sanctioned = sanction_impact * (0.5 + power_factor * 0.5)
        damage_to_imposer = sanction_impact * 0.3 * (1 - power_factor * 0.5)
        
        return {
            'damage_to_sanctioned': damage_to_sanctioned / to_gdp,
            'damage_to_imposer': damage_to_imposer / from_gdp,
            'sanction_impact': sanction_impact
        }
    
    def _get_trade_partners(self, nation: Dict[str, Any], world_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all trade partners for a nation"""
        # This would normally check treaties and alliances
        # For now, return a simple placeholder
        nation_id = nation.get('id', 0)
        all_nations = world_state.get('nations', [])
        
        # Filter out the current nation and any nations with sanctions
        sanctions = self._get_sanctions(nation, world_state)
        sanctioned_ids = [s.get('id', -1) for s in sanctions]
        
        return [n for n in all_nations if n.get('id', -1) != nation_id and n.get('id', -1) not in sanctioned_ids]
    
    def _get_sanctions(self, nation: Dict[str, Any], world_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all nations imposing sanctions on this nation"""
        # This would normally check treaties and diplomatic status
        # For now, return a simple placeholder
        return [] 