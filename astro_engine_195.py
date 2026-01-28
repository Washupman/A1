import math

class AstroEngine_v1_9_5:
    """
    WashUpMan Astrological Logic Engine (Patch 1.9.5 Unified)
    Core Philosophy: Structural Integrity & Double-Layer Host Audit
    """

    def __init__(self):
        # 1. Reference Data: Peak Degrees & Dignities
        self.planets_ref = {
            "Sun":     {"exalted": "Aries", "own": ["Leo"], "debilitated": "Libra", "peak": 10},
            "Moon":    {"exalted": "Taurus", "own": ["Cancer"], "debilitated": "Scorpio", "peak": 3},
            "Mars":    {"exalted": "Capricorn", "own": ["Aries", "Scorpio"], "debilitated": "Cancer", "peak": 28},
            "Mercury": {"exalted": "Virgo", "own": ["Gemini", "Virgo"], "debilitated": "Pisces", "peak": 15},
            "Jupiter": {"exalted": "Cancer", "own": ["Sagittarius", "Pisces"], "debilitated": "Capricorn", "peak": 5},
            "Venus":   {"exalted": "Pisces", "own": ["Taurus", "Libra"], "debilitated": "Virgo", "peak": 27},
            "Saturn":  {"exalted": "Libra", "own": ["Capricorn", "Aquarius"], "debilitated": "Aries", "peak": 20},
            "Rahu":    {"exalted": "Taurus", "own": ["Aquarius"], "debilitated": "Scorpio", "peak": 15}
        }

        # 2. Pushkar Navamsa Mapping
        self.pushkar_map = {
            "Fire": [7, 9],    # Aries, Leo, Sag (Navamsa 7=Libra, 9=Sag)
            "Earth": [3, 5],   # Tau, Vir, Cap (Navamsa 3=Pisces, 5=Taurus)
            "Air": [6, 8],     # Gem, Lib, Aqu (Navamsa 6=Pisces, 8=Taurus)
            "Water": [1, 3]    # Can, Sco, Pis (Navamsa 1=Cancer, 3=Virgo)
        }

        self.sign_elements = {
            "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
            "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
            "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
            "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water"
        }

    def _get_base_score(self, planet_name, sign):
        ref = self.planets_ref.get(planet_name)
        if not ref: return 5.0
        if sign == ref["exalted"]: return 10.0
        if sign in ref["own"]: return 8.0
        if sign == ref["debilitated"]: return 1.0
        return 5.0 # Normal/Friend

    def _calculate_parabolic_zm(self, planet_name, degree):
        ref = self.planets_ref.get(planet_name)
        if not ref: return 1.0
        target_deg = ref["peak"]
        distance = abs(degree - target_deg)
        zm = 1.0 - math.pow((distance / 30.0), 2)
        return max(0.5, zm)

    def _check_pushkar(self, sign_name, navamsa_seq):
        element = self.sign_elements.get(sign_name)
        if not element: return False
        valid_seqs = self.pushkar_map.get(element, [])
        return navamsa_seq in valid_seqs

    def _calculate_l_host_eff(self, host_dignity, host_house_type):
        """ 
        NEW: Double-Layer Host Audit 
        คำนวณความแข็งแกร่งของเจ้าบ้านจากเลเยอร์ราศีจักร
        """
        dignity_scores = {
            'Exalted': 10.0, 'Own': 8.0, 'Normal': 5.0, 
            'Detriment': 3.0, 'Debilitated': 1.0
        }
        house_modifiers = {
            'Kendra/Trikona': 2.0, 'Neutral': 0.0, 'Dusthana': -2.0
        }
        
        s_base_host = dignity_scores.get(host_dignity, 5.0)
        pos_host = house_modifiers.get(host_house_type, 0.0)
        
        # Formula: L_host = (S_base + Pos) / 10
        l_host = (s_base_host + pos_host) / 10.0
        return max(0.5, min(1.2, l_host)) # Cap 0.5 - 1.2

    def calculate_a1_score(self, planet, sign_name, degree, navamsa_seq, 
                           host_dignity="Normal", 
                           host_house_type="Neutral",
                           is_burnt=False, 
                           is_war_losing=False,
                           is_vargottama=False):
        """
        MASTER FUNCTION: A1 = [(S_base * Zm * L_host_eff) + B_pushkar + V_rasi] - Penalties
        """
        # 1. Base & Modifier
        s_base = self._get_base_score(planet, sign_name)
        zm = self._calculate_parabolic_zm(planet, degree)
        
        # 2. Double-Layer Host Audit (L_host_eff)
        l_host = self._calculate_l_host_eff(host_dignity, host_house_type)
        
        # 3. Bonuses
        b_pushkar = 2.5 if self._check_pushkar(sign_name, navamsa_seq) else 0.0
        v_rasi = 2.0 if is_vargottama else 0.0
        
        # 4. Penalties
        p_burnt = 4.0 if is_burnt else 0.0
        p_war = 2.0 if is_war_losing else 0.0
        
        # 5. Calculation
        raw_score = (s_base * zm * l_host) + b_pushkar + v_rasi
        final_a1 = raw_score - (p_burnt + p_war)
        
        return round(max(0.0, final_a1), 2)

# --- 🧪 TEST CASE: อังคารมกร (มหาอุจจ์) แต่เจ้าบ้าน (เสาร์) เป็นนิจและอยู่ภพวินาศ ---
if __name__ == "__main__":
    engine = AstroEngine_v1_9_5()
    
    # Audit อังคารมกร (A2=10)
    score_mars = engine.calculate_a1_score(
        planet="Mars",
        sign_name="Capricorn", 
        degree=19.0, # อยู่ห่าง Peak นิดหน่อย
        navamsa_seq=4,
        host_dignity="Debilitated", # เจ้าบ้านเสาร์เป็นนิจ
        host_house_type="Dusthana"   # เจ้าบ้านอยู่ภพวินาศ
    )
    
    print(f"Mars A1 Score (Patch 1.9.5 Unified): {score_mars}")
    print(f"Friction Index (FI): {round(score_mars/10.0, 2)}")
