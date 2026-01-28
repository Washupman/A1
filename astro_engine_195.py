import math

class AstroEngine_v1_9_5:
    """
    WashUpMan Astrological Logic Engine (Patch 1.9.5)
    Core Philosophy: Structural Integrity & Micro-Logic Correction
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

        # 2. Pushkar Navamsa Mapping (Element -> Navamsa Indices)
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
        """ Calculate S_base based on Sign Dignity """
        ref = self.planets_ref.get(planet_name)
        if not ref: return 5.0
        
        if sign == ref["exalted"]: return 10.0
        if sign in ref["own"]: return 8.0
        if sign == ref["debilitated"]: return 1.0
        
        # Simple Logic for Detriment (Opposite of Own) can be added here
        return 5.0 # Standard/Friend

    def _calculate_parabolic_zm(self, planet_name, degree, current_sign):
        """ Patch 1.8: Parabolic Zone Modifier (Zm) """
        ref = self.planets_ref.get(planet_name)
        if not ref: return 1.0

        # Check if the planet is in a sign that has a Peak degree
        # (Usually Exalted or Debilitated signs define the curve)
        target_deg = ref["peak"]
        
        # Calculate distance (simplified for same sign context)
        # In full version, need to handle cross-sign distance if close to cusp
        distance = abs(degree - target_deg)
        
        # Formula: Zm = 1.0 - ((distance / 30) ^ 2)
        # We cap the penalty to avoid negative multipliers
        zm = 1.0 - math.pow((distance / 30.0), 2)
        return max(0.5, zm)

    def _check_pushkar(self, sign_name, navamsa_seq):
        """ Check Blind Spot 3: Pushkar Navamsa """
        element = self.sign_elements.get(sign_name)
        if not element: return False
        
        valid_seqs = self.pushkar_map.get(element, [])
        return navamsa_seq in valid_seqs

    def calculate_a1_score(self, planet, sign_name, degree, navamsa_seq, 
                           host_strength_score=1.0, 
                           is_burnt=False, 
                           is_war_losing=False,
                           is_vargottama=False):
        """
        MASTER FUNCTION: Calculate A1 (Core Strength) with Patch 1.9.5 Logic
        Equation: A1 = [(S_base * Zm * L_host) + B_pushkar + V_rasi] - Penalties
        """
        
        # 1. Base Score (S_base)
        s_base = self._get_base_score(planet, sign_name)
        
        # 2. Parabolic Modifier (Zm)
        zm = self._calculate_parabolic_zm(planet, degree, sign_name)
        
        # 3. Host/Depositor Strength (L_host) 
        # Input should be: 1.2 (Strong Host), 1.0 (Normal), 0.8 (Weak Host)
        l_host = host_strength_score
        
        # 4. Bonuses
        # Pushkar Bonus
        b_pushkar = 2.5 if self._check_pushkar(sign_name, navamsa_seq) else 0.0
        
        # Vargottama Bonus
        v_rasi = 2.0 if is_vargottama else 0.0
        
        # 5. Penalties
        p_burnt = 4.0 if is_burnt else 0.0
        p_war = 2.0 if is_war_losing else 0.0
        
        # --- THE MASTER EQUATION ---
        raw_score = (s_base * zm * l_host) + b_pushkar + v_rasi
        final_a1 = raw_score - (p_burnt + p_war)
        
        return round(max(0.0, final_a1), 2)

# --- 🧪 EXAMPLE USAGE (Unit Test) ---
if __name__ == "__main__":
    engine = AstroEngine_v1_9_5()

    print("--- Case Study 1: Mars (The Engine) ---")
    # ข้อมูล: อังคารในนวางค์มิถุน (เรือนพุธ), พุธเป็นนิจ (Host Weak)
    score_mars = engine.calculate_a1_score(
        planet="Mars",
        sign_name="Gemini", # นวางค์
        degree=19.28,       # องศาเดิม (ใช้คำนวณ Zm ในบริบทนวางค์)
        navamsa_seq=4,      # นวางค์ลูกที่ 4 (สมมติ)
        host_strength_score=0.8, # L_host: พุธเป็นนิจ
        is_burnt=False,
        is_war_losing=False,
        is_vargottama=False
    )
    print(f"Mars A1 Score (Patch 1.9.5): {score_mars}")

    print("\n--- Case Study 2: Saturn (The Jackpot) ---")
    # ข้อมูล: เสาร์ (มกร 15.16) -> นวางค์พฤษภ (ลูกที่ 5) -> Pushkar!
    # เจ้าบ้านนวางค์คือศุกร์ (ให้ค่ากลางๆ 1.0)
    score_saturn = engine.calculate_a1_score(
        planet="Saturn",
        sign_name="Taurus", # นวางค์
        degree=15.16,
        navamsa_seq=5,      # ลูกที่ 5 ของธาตุดิน = Pushkar
        host_strength_score=1.0,
        is_burnt=False,
        is_war_losing=False,
        is_vargottama=False
    )
    print(f"Saturn A1 Score (Patch 1.9.5): {score_saturn}")
