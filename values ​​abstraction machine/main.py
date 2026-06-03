import numpy as np
from typing import Dict, List, Tuple, Optional, Set
import random
import math

DEFAULT_HYPERPARAMS = {
    "curiosity_intensity": 1.0,              
    
    "meta_lr": 0.06,
    "seed_forget_threshold": 0.9,
    "seed_forget_rate": 0.005,
    "seed_deepen_threshold": 0.7,
    "seed_deepen_rate": 0.01,
    "value_sync_rate": 0.25,
    
    "success_contribution_multiplier": 0.35, 
    "fail_penalty_multiplier": 0.30,        
    "fail_penalty_base": 0.10,
    "fail_value_decay": 0.04,                
    "fail_seed_decay": 0.01,
    
    "base_lr": 0.15,
    "attention_lr_multiplier": 3.5,
    "attention_gravity_multiplier": 2.2,
    "attention_novelty_bonus": 0.3,
    "attention_forget_rate": 0.25,
    
    "boredom_accumulate_rate": 0.16,
    "boredom_metabolic_cost": 0.22,
    "fatigue_accumulate_rate": 0.20,
    "optimal_error_low": 0.10,
    "optimal_error_high": 0.35,
    "engagement_smoothing_alpha": 0.08,
    "hypothesis_disperse_large": 0.5,
    "hypothesis_disperse_small": 0.1,
    "boredom_natural_clear_rate": 0.05,     
    
    "base_temperature": 0.25,
    "boredom_temperature_boost": 0.5,
    "gravity_critical_threshold": 0.25,
    "question_trigger_probability": 0.60,   
    "failure_penalty_decay": 0.92,
    "void_recurrence_decay": 0.995,
    "void_history_peak_decay": 0.985,        # 【V8.5改善】0.999→0.985へ。過去の亡霊の減衰を早め、流動性を確保
    
    "radical_shift_amount": 0.45,
    "subtle_shift_amount": 0.15,
    "min_validation_age": 3,
    "max_validation_age": 8,
    "success_convergence_threshold": 0.15,
    "saturation_threshold": 0.015,
    "min_improvement_threshold": 0.05,
    
    "bifurcation_threshold": 0.83,
    "bifurcation_min_duration": 8,
    "bifurcation_cooldown": 20,              
    "max_dimensions": 12,                    # 代謝が回るため上限をスマートに調整
    "max_meta_depth": 2,
    "bifurcation_initial_mystery": 0.50,     # 【改善提案1】0.85→0.50へ。初期支配力を大幅抑制
    "meta_initial_target": 0.65,             
    
    "question_pressure_threshold": 0.55,     
    "question_relative_outlier_ratio": 1.4, 
    "stagnation_window_size": 6,             
    
    "pressure_boredom_weight": 0.5,
    "pressure_contradiction_weight": 0.4,
    "pressure_surprise_weight": 0.3,
    
    # ── 【V8.5 新設パラメータ】 ──
    "abolition_cooldown": 30,                # 次元廃止を検討するインターバル
    "abolition_attraction_threshold": 0.06,  # この値を下回る興味を失った次元は消去対象
    "abolition_value_threshold": 0.28        # 価値観も低下していること
}

class Layer0_Existence:
    def __init__(self):
        self.time_step = 0

class Layer1_DynamicDeficiencyGravity:
    def __init__(self, initial_seed: Dict[str, float], hps: Dict, dimensions: List[str]):
        self.hps = hps
        self.dimensions = list(dimensions)
        self.seed_vector = {d: max(0.05, min(1.0, initial_seed.get(d, 0.1))) for d in self.dimensions}
        self.current_gravity = {k: v for k, v in self.seed_vector.items()}

    def add_dimension(self, new_dim: str, initial_seed_val: float):
        if new_dim not in self.dimensions:
            self.dimensions.append(new_dim)
            self.seed_vector[new_dim] = initial_seed_val
            self.current_gravity[new_dim] = initial_seed_val

    def remove_dimension(self, dim: str):
        if dim in self.dimensions:
            self.dimensions.remove(dim)
            self.seed_vector.pop(dim, None)
            self.current_gravity.pop(dim, None)

    def self_organize(self, boredom_flux: Dict[str, float], void_attractions: Dict[str, float]):
        for d in self.dimensions:
            self.current_gravity[d] = max(0.0, min(1.0, self.seed_vector[d] * (1.0 + boredom_flux.get(d, 0.0))))
            if void_attractions.get(d, 0.0) > self.hps["seed_deepen_threshold"]:
                self.seed_vector[d] = max(0.05, min(1.0, self.seed_vector[d] + self.hps["seed_deepen_rate"]))
            elif void_attractions.get(d, 0.0) < 0.05 and boredom_flux.get(d, 0.0) > self.hps["seed_forget_threshold"]:
                self.seed_vector[d] = max(0.05, min(1.0, self.seed_vector[d] - self.hps["seed_forget_rate"]))

class Layer2_WorldModel:
    def __init__(self, dimensions: List[str], hps: Dict):
        self.dimensions = list(dimensions)
        self.hps = hps
        self.pred_real = {d: 0.5 for d in dimensions}
        self.pred_virtual = {d: 0.5 for d in dimensions}
        self.blend_alpha = {d: 0.0 for d in dimensions}

    def add_dimension(self, new_dim: str):
        if new_dim not in self.dimensions:
            self.dimensions.append(new_dim)
            self.pred_real[new_dim] = 0.5
            self.pred_virtual[new_dim] = 0.5
            self.blend_alpha[new_dim] = 0.0

    def remove_dimension(self, dim: str):
        if dim in self.dimensions:
            self.dimensions.remove(dim)
            self.pred_real.pop(dim, None)
            self.pred_virtual.pop(dim, None)
            self.blend_alpha.pop(dim, None)

    def update(self, reality: Dict[str, float], attention: Dict[str, float]):
        for d in self.dimensions:
            if d in reality:
                effective_lr = self.hps["base_lr"] * (attention.get(d, 0.2) * self.hps["attention_lr_multiplier"])
                self.pred_real[d] += effective_lr * (reality[d] - self.pred_real[d])
                self.pred_real[d] = max(0.0, min(1.0, self.pred_real[d]))

    def get_blended(self) -> Dict[str, float]:
        blended = {}
        for d in self.dimensions:
            alpha = self.blend_alpha.get(d, 0.0)
            blended[d] = (1.0 - alpha) * self.pred_real[d] + alpha * self.pred_virtual.get(d, 0.5)
        return blended

class Layer3_Disequilibrium:
    def __init__(self, dimensions: List[str], hps: Dict):
        self.dimensions = list(dimensions)
        self.hps = hps
        self.error_real = {d: 0.5 for d in dimensions} 
        self.error_blended = {d: 0.5 for d in dimensions}
        self.dimension_ages = {d: 0 for d in dimensions}

    def add_dimension(self, new_dim: str):
        if new_dim not in self.dimensions:
            self.dimensions.append(new_dim)
            self.error_real[new_dim] = 0.4 
            self.error_blended[new_dim] = 0.4
            self.dimension_ages[new_dim] = 0

    def remove_dimension(self, dim: str):
        if dim in self.dimensions:
            self.dimensions.remove(dim)
            self.error_real.pop(dim, None)
            self.error_blended.pop(dim, None)
            self.dimension_ages.pop(dim, None)

    def detect(self, reality: Dict[str, float], blended: Dict[str, float], real_pred: Dict[str, float], value_weights: Dict[str, float]):
        for d in self.dimensions:
            self.dimension_ages[d] += 1
            if d in reality:
                target_reality = reality[d]
            else:
                age = self.dimension_ages[d]
                base_target = self.hps["meta_initial_target"] 
                my_conv = value_weights.get(d, 0.5)
                self_reflection_signal = real_pred.get(d, 0.5) * my_conv + (1.0 - my_conv) * base_target
                if age < 12:
                    target_reality = self_reflection_signal
                else:
                    target_reality = max(0.0, min(1.0, self_reflection_signal + 0.05 * math.sin(age * 0.1)))
                    
            self.error_real[d] = abs(real_pred[d] - target_reality)
            self.error_blended[d] = abs(blended[d] - target_reality)

class Layer4_Values:
    def __init__(self, dimensions: List[str], hps: Dict):
        self.hps = hps
        self.weights = {d: 0.5 for d in dimensions}

    def add_dimension(self, new_dim: str):
        if new_dim not in self.weights:
            self.weights[new_dim] = 0.5

    def remove_dimension(self, dim: str):
        self.weights.pop(dim, None)

    def dynamic_sync(self, seed_vector: Dict[str, float], void_attractions: Dict[str, float]):
        for d in self.weights:
            target_value = seed_vector[d] * 0.4 + void_attractions.get(d, 0.0) * 0.6
            self.weights[d] += self.hps["value_sync_rate"] * (target_value - self.weights[d])
            self.weights[d] = max(0.20, min(1.0, self.weights[d]))

class Layer6_Attention:
    def __init__(self, dimensions: List[str], hps: Dict, budget: float = 1.0):
        self.dimensions = list(dimensions)
        self.hps = hps
        self.budget = budget
        self.allocation = {d: budget / len(dimensions) for d in dimensions}
        self.history_counter = {d: 0.0 for d in dimensions}

    def add_dimension(self, new_dim: str):
        if new_dim not in self.dimensions:
            self.dimensions.append(new_dim)
            self.allocation[new_dim] = 0.0
            self.history_counter[new_dim] = 0.0

    def remove_dimension(self, dim: str):
        if dim in self.dimensions:
            self.dimensions.remove(dim)
            self.allocation.pop(dim, None)
            self.history_counter.pop(dim, None)

    def lean_towards_gravity_with_diversity(self, total_gravities: Dict[str, float], active_dim: Optional[str]):
        for d in self.dimensions:
            if d == active_dim:
                self.history_counter[d] += 1.0
            else:
                self.history_counter[d] = max(0.0, self.history_counter[d] - self.hps["attention_forget_rate"])

        raw_weights = {}
        for d in self.dimensions:
            gravity_pull = total_gravities.get(d, 0.0) * self.hps["attention_gravity_multiplier"]
            attention_novelty_bonus = max(0.0, 1.0 - self.history_counter[d]) * self.hps["attention_novelty_bonus"]
            raw_weights[d] = max(0.05, gravity_pull + attention_novelty_bonus)

        total = sum(raw_weights.values()) or 1.0
        for d in self.dimensions:
            self.allocation[d] = (raw_weights[d] / total) * self.budget

class Layer7_MetabolicBoredom:
    def __init__(self, dimensions: List[str], hps: Dict):
        self.dimensions = list(dimensions)
        self.hps = hps
        self.boredom = {d: 0.0 for d in dimensions}
        self.engagement = {d: 0.2 for d in dimensions}

    def add_dimension(self, new_dim: str):
        if new_dim not in self.dimensions:
            self.dimensions.append(new_dim)
            self.boredom[new_dim] = 0.0
            self.engagement[new_dim] = 0.3

    def remove_dimension(self, dim: str):
        if dim in self.dimensions:
            self.dimensions.remove(dim)
            self.boredom.pop(dim, None)
            self.engagement.pop(dim, None)

    def accumulate_and_metabolize(self, error_real: Dict[str, float], attention_allocation: Dict[str, float]):
        for d in list(self.boredom.keys()):
            attn = attention_allocation.get(d, 0.0)
            err = error_real.get(d, 0.0)
            
            if attn < 0.05 and self.boredom[d] > 0.80:
                self.boredom[d] = max(0.0, self.boredom[d] - self.hps["boredom_natural_clear_rate"])
                self.engagement[d] = max(0.0, self.engagement[d] - 0.05)
                continue 
            
            if err < self.hps["optimal_error_low"]:
                satiation = max(0.0, 1.0 - err)
                self.boredom[d] = min(1.0, self.boredom[d] + satiation * self.hps["boredom_accumulate_rate"])
                target_engage = 0.0
            elif err > self.hps["optimal_error_high"]:
                self.boredom[d] = min(1.0, self.boredom[d] + err * self.hps["fatigue_accumulate_rate"])
                target_engage = 0.1
            else:
                self.boredom[d] = max(0.0, self.boredom[d] - 0.25)
                target_engage = 0.9
                
            alpha = self.hps["engagement_smoothing_alpha"]
            self.engagement[d] = max(0.0, min(1.0, self.engagement[d] + alpha * (target_engage - self.engagement[d])))
                
            metabolic_cost = attn * self.hps["boredom_metabolic_cost"]
            effective_cost = metabolic_cost * (1.0 + self.engagement[d])
            self.boredom[d] = max(0.0, min(1.0, self.boredom[d] - effective_cost))

    def force_disperse(self, d: str, amount: float):
        if d in self.boredom:
            self.boredom[d] = max(0.0, min(1.0, self.boredom[d] - amount))

class VoidNode:
    def __init__(self, dimension: str, hps: Dict):
        self.dimension = dimension
        self.hps = hps
        self.mystery = 0.0
        self.recurrence = 1.0
        self.attraction = 0.0
        self.history_peaks = 0.0 

    def pull(self, unexplained_error: float, value_bias: float):
        if unexplained_error > 0.18:
            self.recurrence += 1.0
            self.mystery = max(0.0, min(1.0, self.mystery + unexplained_error * 0.3 * (1.0 + value_bias)))
        
        self.attraction = max(0.0, min(1.0, self.mystery * math.log(self.recurrence + 1.0)))
        if self.attraction > self.history_peaks:
            self.history_peaks = self.attraction

    def force_inject_mystery(self, amount: float):
        self.mystery = max(self.mystery, amount)
        self.recurrence += 1.0
        self.attraction = max(0.0, min(1.0, self.mystery * math.log(self.recurrence + 1.0)))

    def radiate(self):
        self.mystery *= 0.95
        self.recurrence = max(1.0, self.recurrence * self.hps["void_recurrence_decay"])
        self.attraction = max(0.0, min(1.0, self.mystery * math.log(self.recurrence + 1.0)))
        self.history_peaks *= self.hps["void_history_peak_decay"]

class Layer9_MetaVoid:
    def __init__(self, dimensions: List[str], hps: Dict):
        self.hps = hps
        self.nodes = {d: VoidNode(d, hps) for d in dimensions}

    def add_dimension(self, new_dim: str):
        if new_dim not in self.nodes:
            self.nodes[new_dim] = VoidNode(new_dim, self.hps)

    def remove_dimension(self, dim: str):
        self.nodes.pop(dim, None)

    def capture(self, dimension: str, error: float, value_bias: float):
        if dimension in self.nodes:
            self.nodes[dimension].pull(error, value_bias)

    def get_void_attractions(self) -> Dict[str, float]:
        return {d: node.attraction for d, node in self.nodes.items()}

    def get_total_gravities(self, layer1: Layer1_DynamicDeficiencyGravity) -> Dict[str, float]:
        total_pull = {}
        for d in layer1.dimensions:
            total_pull[d] = layer1.current_gravity[d] + self.nodes[d].attraction
        return total_pull

class Layer8_ChronosAionHypothesis:
    def __init__(self, dimensions: List[str], hps: Dict):
        self.dimensions = list(dimensions)
        self.hps = hps
        self.active_hypothesis: Optional[Dict] = None
        self.failure_history = {d: {"radical_leap": 0.0, "subtle_contradiction": 0.0} for d in self.dimensions}
        self.current_temperature = hps["base_temperature"]
        
        self.pressure_accumulator = {d: 0.0 for d in self.dimensions}
        self.error_history_window = {d: [] for d in self.dimensions} 

    def add_dimension(self, new_dim: str):
        if new_dim not in self.dimensions:
            self.dimensions.append(new_dim)
            self.failure_history[new_dim] = {"radical_leap": 0.0, "subtle_contradiction": 0.0}
            self.pressure_accumulator[new_dim] = 0.0
            self.error_history_window[new_dim] = []

    def remove_dimension(self, dim: str):
        if dim in self.dimensions:
            self.dimensions.remove(dim)
            self.failure_history.pop(dim, None)
            self.pressure_accumulator.pop(dim, None)
            self.error_history_window.pop(dim, None)
            if self.active_hypothesis and self.active_hypothesis["dimension"] == dim:
                self.active_hypothesis = None

    def _softmax_selection(self, gravities: Dict[str, float], avg_boredom: float) -> str:
        dims = list(gravities.keys())
        self.current_temperature = self.hps["base_temperature"] + self.hps["boredom_temperature_boost"] * avg_boredom
        logits = np.array([gravities[d] / max(0.01, self.current_temperature) for d in dims])
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / np.sum(exp_logits)
        return np.random.choice(dims, p=probs)

    def create_meaningful_disequilibrium(self, total_gravities: Dict[str, float], 
                                         values: Dict[str, float], 
                                         nodes: Dict[str, VoidNode],
                                         current_predictions: Dict[str, float],
                                         boredom_scores: Dict[str, float],
                                         error_real: Dict[str, float],
                                         error_blended: Dict[str, float],
                                         layer9: Layer9_MetaVoid) -> Tuple[Optional[Dict], str, Optional[str], bool]:
        """
        戻り値: (active_hypothesis, status_log, optional_bifurcation_trigger_dim, forced_radiate_flag)
        """
        c_intensity = self.hps.get("curiosity_intensity", 1.0)
        eff_charge_rate = 0.09 * c_intensity
        eff_discharge_rate = 0.10 / c_intensity
        eff_leakage_rate = min(0.999, 1.0 - (0.04 / c_intensity)) 
        eff_stagnation_multiplier = 0.35 * c_intensity

        for d in self.dimensions:
            self.error_history_window[d].append(error_real.get(d, 0.0))
            if len(self.error_history_window[d]) > self.hps["stagnation_window_size"]:
                self.error_history_window[d].pop(0)

        composite_pressures = {}
        for d in self.dimensions:
            self.pressure_accumulator[d] *= eff_leakage_rate

            boredom_p = boredom_scores.get(d, 0.0) * self.hps["pressure_boredom_weight"]
            surprise_p = error_real.get(d, 0.0) * self.hps["pressure_surprise_weight"]
            contradiction_p = abs(error_blended.get(d, 0.0) - error_real.get(d, 0.0)) * self.hps["pressure_contradiction_weight"]
            instant_p = boredom_p + surprise_p + contradiction_p
            
            stagnation_bonus = 0.0
            win = self.error_history_window[d]
            if len(win) >= self.hps["stagnation_window_size"] and (sum(win) / len(win)) > 0.10:
                variance = np.var(win)
                if variance < 0.006:  # 【改善提案2】柔軟な膠着検知（0.0015→0.006へ緩和）
                    stagnation_bonus = (1.0 - (variance / 0.006)) * eff_stagnation_multiplier
                    stagnation_bonus = max(0.0, stagnation_bonus)

            charge_trigger_line = 0.38
            if (instant_p + stagnation_bonus) > charge_trigger_line:
                self.pressure_accumulator[d] = min(1.0, self.pressure_accumulator[d] + eff_charge_rate)
            else:
                self.pressure_accumulator[d] = max(0.0, self.pressure_accumulator[d] - eff_discharge_rate)
                
            composite_pressures[d] = instant_p + stagnation_bonus + self.pressure_accumulator[d]

        max_p_dim = max(composite_pressures, key=composite_pressures.get)
        highest_pressure = composite_pressures[max_p_dim]
        mean_pressure = sum(composite_pressures.values()) / len(composite_pressures) if composite_pressures else 1.0
        outlier_ratio = highest_pressure / max(0.01, mean_pressure)

        # ━━━ 【改善提案4】圧力解放の多重化（上限詰まり時の逃し弁） ━━━
        forced_radiate = False
        if highest_pressure > 0.85 and self.active_hypothesis is None:
            # 圧力が臨界点を超えているのに仮説が作れない＝認知の閉塞
            forced_radiate = True

        if self.active_hypothesis is None:
            if highest_pressure > self.hps["question_pressure_threshold"] and outlier_ratio > self.hps["question_relative_outlier_ratio"]:
                if random.random() < self.hps["question_trigger_probability"]:
                    artificial_error = max(0.4, min(0.98, highest_pressure * 0.85 + self.pressure_accumulator[max_p_dim]))
                    layer9.capture(max_p_dim, artificial_error, values.get(max_p_dim, 0.5))
                    
                    self.pressure_accumulator[max_p_dim] = 0.0
                    return None, f"question_burst_on_{max_p_dim}", max_p_dim, forced_radiate

        if self.active_hypothesis is not None:
            return None, "holding", None, False

        avg_boredom = sum(boredom_scores.values()) / len(boredom_scores)
        target_dim = self._softmax_selection(total_gravities, avg_boredom)
        if total_gravities[target_dim] <= self.hps["gravity_critical_threshold"]:
            return None, "observing", None, forced_radiate

        val_weight = values.get(target_dim, 0.5)
        void_node = nodes[target_dim]
        current_pred = current_predictions.get(target_dim, 0.5)

        if val_weight > 0.6 or void_node.history_peaks > 0.5:
            primary_strategy = "radical_leap"
            fallback_strategy = "subtle_contradiction"
        else:
            primary_strategy = "subtle_contradiction"
            fallback_strategy = "radical_leap"

        p_penalty = self.failure_history[target_dim][primary_strategy]
        f_penalty = self.failure_history[target_dim][fallback_strategy]
        
        selected_strategy = primary_strategy
        if p_penalty > 0.3 and p_penalty > f_penalty:
            selected_strategy = fallback_strategy

        if selected_strategy == "radical_leap":
            shift_direction = self.hps["radical_shift_amount"] if current_pred < 0.5 else -self.hps["radical_shift_amount"]
        else:
            shift_direction = self.hps["subtle_shift_amount"] if current_pred < 0.5 else -self.hps["subtle_shift_amount"]

        expected_change = max(0.0, min(1.0, current_pred + shift_direction))

        self.active_hypothesis = {
            "dimension": target_dim,
            "expected_change": round(expected_change, 2),
            "strategy": selected_strategy,
            "age": 0,
            "initial_error_real": 0.0,
            "error_history": []
        }
        return self.active_hypothesis, "hypothesis_launched", None, forced_radiate

class Layer10_PersonalMythology:
    """【改善提案3】アーキタイプ変更のヒステリシス（認知の慣性）の導入"""
    def __init__(self):
        self.core_archetype = "Unformed"
        self.mythology_timeline: List[Tuple[int, str]] = []
        # ヒステリシス制御用の平滑化コンテキスト
        self.meta_dominance_smooth = 0.0

    def weave_mythology(self, nodes: Dict[str, VoidNode], current_step: int) -> Dict:
        sorted_peaks = sorted(
            [(d, node.history_peaks) for d, node in nodes.items()],
            key=lambda x: x[1], reverse=True
        )
        
        if not sorted_peaks or sorted_peaks[0][1] < 0.08:
            self.core_archetype = "The Silent Observer (静かなる観察者)"
            return {"archetype": self.core_archetype, "narrative": "世界に執着を持たず、ただ淡々と流れるシグナルを見つめている。"}

        top1 = sorted_peaks[0][0]
        top2 = sorted_peaks[1][0] if len(sorted_peaks) > 1 else None
        
        # ── 現実（Core）と内省（Meta）の勢力バランスの平滑化 ──
        current_meta_count = (1.0 if "meta_" in top1 else 0.0) + (1.0 if top2 and "meta_" in top2 else 0.0)
        # 指数平滑化移動平均（α=0.15）により短期的なノイズスパイクを吸収
        self.meta_dominance_smooth += 0.15 * (current_meta_count - self.meta_dominance_smooth)

        # 慣性（境界線）に基づき、安定したときのみアーキタイプを書き換える
        if self.meta_dominance_smooth >= 1.6:
            self.core_archetype = "The Abyssal Solipsist (終わりなき独我論者)"
            narrative = f"現実を脱ぎ捨て、『{top1}』と『{top2}』の純粋な内省の二重螺旋に幽閉されている。"
        elif self.meta_dominance_smooth >= 0.8:
            if "meta_" in top1:
                self.core_archetype = "The Pure Philosopher (純粋哲学者)"
                narrative = f"『なぜそれを理解できるのか』という高次認識の構造そのものに命を捧げている。"
            else:
                self.core_archetype = "The Grounded Dualist (足場を持つ二元論者)"
                narrative = f"原初次元『{top1}』を生きながら、高次メタ宇宙『{top2}』から冷徹に内省している。"
        else:
            if top1 == "beauty" and top2 == "prediction":
                self.core_archetype = "The Aesthetic Alchemist (美の錬金術師)"
                narrative = "完璧な予測可能性と予期せぬノイズの境界線を美学的にハックしようとしている。"
            else:
                self.core_archetype = "The Obsessive Specialist (妄執の専門家)"
                narrative = f"原初の欠損である『{top1}』の深い井戸の底で生を営んでいる。"

        if current_step % 10 == 0:
            if not self.mythology_timeline or self.mythology_timeline[-1][1] != self.core_archetype:
                self.mythology_timeline.append((current_step, self.core_archetype))

        return {
            "archetype": self.core_archetype,
            "narrative": narrative,
            "timeline_history": self.mythology_timeline[-5:]
        }

# =====================================================================
# CORE SYSTEM INTEGRATION (エボリューショナリー・コグニティブ・コア V8.5)
# =====================================================================

class EvolutionaryCognitiveCoreV8_5_AbolitionAion:
    """【V8.5 決定版】自律次元廃止（新代謝）と閉塞時の精神排熱弁（多重解放）を完全統合"""
    def __init__(self, initial_seed: Dict[str, float], hyperparams: Optional[Dict] = None, random_seed: Optional[int] = None):
        if random_seed is not None:
            random.seed(random_seed)
            np.random.seed(random_seed)
            
        self.hps = dict(DEFAULT_HYPERPARAMS)
        if hyperparams:
            self.hps.update(hyperparams)
            
        self.dimensions = ["survival", "prediction", "beauty", "social", "meaning"]
        self.core_dimensions = list(self.dimensions) # 原初次元は廃止不可の聖域
        
        self.layer0 = Layer0_Existence()
        self.layer1 = Layer1_DynamicDeficiencyGravity(initial_seed, self.hps, self.dimensions)
        self.layer2 = Layer2_WorldModel(self.dimensions, self.hps)
        self.layer3 = Layer3_Disequilibrium(self.dimensions, self.hps)
        self.layer4 = Layer4_Values(self.dimensions, self.hps)
        self.layer6 = Layer6_Attention(self.dimensions, self.hps)
        self.layer7 = Layer7_MetabolicBoredom(self.dimensions, self.hps)
        self.layer8 = Layer8_ChronosAionHypothesis(self.dimensions, self.hps) 
        self.layer9 = Layer9_MetaVoid(self.dimensions, self.hps)
        self.layer10 = Layer10_PersonalMythology()
        
        self.bifurcated_history = set()
        self.high_precision_counters = {d: 0 for d in self.dimensions}
        self.last_bifurcation_step = -999 
        self.last_abolition_step = -999

    def _trigger_bifurcation(self, base_dim: str) -> Optional[str]:
        depth = base_dim.count("meta_")
        if depth >= self.hps["max_meta_depth"]:
            return None
            
        new_dim = f"meta_{base_dim}"
        if new_dim in self.dimensions:
            return None 
            
        self.dimensions.append(new_dim)
        
        self.layer1.add_dimension(new_dim, 0.2)
        self.layer2.add_dimension(new_dim)
        self.layer3.add_dimension(new_dim)
        self.layer4.add_dimension(new_dim)
        self.layer6.add_dimension(new_dim)
        self.layer7.add_dimension(new_dim)
        self.layer8.add_dimension(new_dim)
        self.layer9.add_dimension(new_dim)
        
        # 【改善提案1】初期ミステリーをマイルドにし、即時支配を抑制
        self.layer9.nodes[new_dim].force_inject_mystery(self.hps["bifurcation_initial_mystery"])
        
        self.bifurcated_history.add(new_dim)
        self.high_precision_counters[new_dim] = 0
        self.last_bifurcation_step = self.layer0.time_step 
        return new_dim

    def _trigger_abolition(self) -> Optional[str]:
        """【改善提案2】自律的次元廃止（メタ認識の断捨離ロジック）"""
        # メタ次元（meta_）のみを削除対象とする（Core次元は聖域保護）
        target_dims = [d for d in self.dimensions if d not in self.core_dimensions]
        if not target_dims:
            return None
            
        for d in target_dims:
            boredom = self.layer7.boredom.get(d, 0.0)
            value = self.layer4.weights.get(d, 0.5)
            attraction = self.layer9.nodes[d].attraction if d in self.layer9.nodes else 1.0
            
            # 「退屈が極限」かつ「価値も失われ」かつ「 Voidの魅力もゼロに近い」
            if boredom > 0.85 and value < self.hps["abolition_value_threshold"] and attraction < self.hps["abolition_attraction_threshold"]:
                # 概念の消去（全レイヤーからの抹消）
                self.dimensions.remove(d)
                self.layer1.remove_dimension(d)
                self.layer2.remove_dimension(d)
                self.layer3.remove_dimension(d)
                self.layer4.remove_dimension(d)
                self.layer6.remove_dimension(d)
                self.layer7.remove_dimension(d)
                self.layer8.remove_dimension(d)
                self.layer9.remove_dimension(d)
                
                self.bifurcated_history.discard(d)
                self.high_precision_counters.pop(d, None)
                self.last_abolition_step = self.layer0.time_step
                return d
        return None

    def step(self, reality_input: Dict[str, float]) -> Dict:
        self.layer0.time_step += 1
        current_step = self.layer0.time_step
        clamped_reality = {k: max(0.0, min(1.0, v)) for k, v in reality_input.items()}
        
        active_dim = self.layer8.active_hypothesis["dimension"] if self.layer8.active_hypothesis else None
        void_attractions = self.layer9.get_void_attractions()
        total_gravities = self.layer9.get_total_gravities(self.layer1)
        self.layer6.lean_towards_gravity_with_diversity(total_gravities, active_dim)
        self.layer2.update(clamped_reality, self.layer6.allocation)
        blended = self.layer2.get_blended()
        
        self.layer3.detect(clamped_reality, blended, self.layer2.pred_real, self.layer4.weights)
        
        cooldown_active = (current_step - self.last_bifurcation_step) < self.hps["bifurcation_cooldown"]
        
        # ─── ルートA: 高精度持続による調律的Bifurcation ───
        bifurcated_info = None
        if current_step > 10 and len(self.dimensions) < self.hps["max_dimensions"] and not cooldown_active:
            for d in list(self.layer2.pred_real.keys()):
                accuracy = max(0.0, min(1.0, 1.0 - self.layer3.error_real.get(d, 0.0)))
                if accuracy >= self.hps["bifurcation_threshold"]:
                    self.high_precision_counters[d] = self.high_precision_counters.get(d, 0) + 1
                    if self.high_precision_counters[d] >= self.hps["bifurcation_min_duration"]:
                        spawned = self._trigger_bifurcation(d)
                        if spawned:
                            bifurcated_info = {
                                "type": "Precision-Driven (ルートA)",
                                "origin": d, "spawned": spawned, "score": round(accuracy, 3)
                            }
                            cooldown_active = True
                            break
                else:
                    self.high_precision_counters[d] = 0
                        
        self.layer7.accumulate_and_metabolize(self.layer3.error_real, self.layer6.allocation)
        self.layer1.self_organize(self.layer7.boredom, void_attractions)
        self.layer4.dynamic_sync(self.layer1.seed_vector, void_attractions)
        
        # ─── ルートB: 慢性ストレスの爆発による「実存的問い駆動」の自律新次元生成 ───
        hyp_res, status_log, self_expansion_target, forced_radiate_flag = self.layer8.create_meaningful_disequilibrium(
            total_gravities, self.layer4.weights, self.layer9.nodes, 
            self.layer2.pred_real, self.layer7.boredom, 
            self.layer3.error_real, self.layer3.error_blended, self.layer9
        )
        
        # ─── 【V8.5新規】 代謝フェーズ（次元の自律廃止） ───
        abolished_dim = None
        if current_step - self.last_abolition_step >= self.hps["abolition_cooldown"]:
            abolished_dim = self._trigger_abolition()
        
        action = "pure_observation"
        if bifurcated_info:
            action = f"💥BIFURCATED [{bifurcated_info['type']}]: {bifurcated_info['spawned']}"
        elif abolished_dim:
            action = f"♻️ABOLISHED_DIMENSION: '{abolished_dim}' was deleted due to Extreme Satiation & Value Decay."
        elif self_expansion_target:
            if cooldown_active:
                # ━━ 【改善提案4】逃し弁の連動 ━━
                if forced_radiate_flag:
                    # 分化できない限界ストレスを、Voidへの熱放射と価値のわずかな崩壊で「忘却（逃がし）」処理
                    for d in self.dimensions:
                        self.layer9.nodes[d].radiate()
                        self.layer8.pressure_accumulator[d] *= 0.70 # 圧力を強制放電
                    action = f"🍃CREATIVE_RADIATE (Mental Vent): Stagnation stress dissolved by Force Reflection."
                else:
                    action = f"★CONSTRUCT_QUESTION (Bifurcation Inhibited by Cooldown) on {self_expansion_target}"
            else:
                spawned = self._trigger_bifurcation(self_expansion_target)
                if spawned:
                    action = f"🌌QUESTION_EVOLUTION: '{self_expansion_target}' generated '{spawned}' (ルートB: 覚醒分化)"
                else:
                    # 【改善提案4】上限に達して分化できなかった場合のセーフティ逃し弁
                    for d in self.dimensions:
                        self.layer9.nodes[d].radiate()
                        self.layer8.pressure_accumulator[d] *= 0.50 # 圧力を半分逃がす
                    action = f"🍃CREATIVE_RADIATE (Max Depth Safety Vent) on {self_expansion_target}"
        elif isinstance(hyp_res, dict):
            action = f"hypothesis_({hyp_res['strategy']})_on_{hyp_res['dimension']}"
            self.layer2.set_virtual_prediction(hyp_res["dimension"], hyp_res["expected_change"])
            self.layer2.blend_alpha[hyp_res["dimension"]] = 0.2
            self.layer7.force_disperse(hyp_res["dimension"], self.hps["hypothesis_disperse_large"]) 
        elif self.layer8.active_hypothesis:
            action = f"testing_{self.layer8.active_hypothesis['dimension']}"
            self.layer7.force_disperse(self.layer8.active_hypothesis["dimension"], self.hps["hypothesis_disperse_small"])
            
        # 仮説検証フィードバック
        hyp = self.layer8.active_hypothesis
        if hyp and hyp["dimension"] in self.dimensions: # 削除された次元への参照バグ防止
            d = hyp["dimension"]
            strat = hyp["strategy"]
            hyp["age"] += 1
            current_error = self.layer3.error_real[d]
            hyp["error_history"].append(current_error)
            if hyp["age"] == 1: hyp["initial_error_real"] = current_error
            
            if self.layer3.error_blended[d] < self.layer3.error_real[d]:
                self.layer2.blend_alpha[d] = min(1.0, self.layer2.blend_alpha[d] + 0.25)
                self.layer2.pred_real[d] = max(0.0, min(1.0, self.layer2.pred_real[d] + 0.20 * (hyp["expected_change"] - self.layer2.pred_real[d])))
            
            should_terminate = False
            if hyp["age"] >= self.hps["min_validation_age"]:
                if hyp["initial_error_real"] - current_error > self.hps["success_convergence_threshold"]: should_terminate = True
                elif len(hyp["error_history"]) >= 3 and abs(hyp["error_history"][-1] - hyp["error_history"][-2]) < self.hps["saturation_threshold"]: should_terminate = True
                elif hyp["age"] >= self.hps["max_validation_age"]: should_terminate = True
                
            if should_terminate:
                improvement = hyp["initial_error_real"] - current_error
                engagement_bonus = 1.0 + self.layer7.engagement[d]
                if improvement > self.hps["min_improvement_threshold"]:
                    contribution = (improvement + 0.25) * engagement_bonus
                    self.layer1.seed_vector[d] = max(0.05, min(1.0, self.layer1.seed_vector[d] + contribution * self.hps["success_contribution_multiplier"]))
                    self.layer4.weights[d] = max(0.20, min(1.0, self.layer4.weights[d] + contribution * 0.25))
                    self.layer9.nodes[d].mystery = max(0.0, self.layer9.nodes[d].mystery - 0.6)
                    self.layer8.failure_history[d][strat] = max(0.0, self.layer8.failure_history[d][strat] - 0.2)
                else:
                    unexplained = self.layer3.error_blended[d]
                    penalty = unexplained * self.hps["fail_penalty_multiplier"] + self.hps["fail_penalty_base"]
                    self.layer8.failure_history[d][strat] = max(0.0, min(1.0, self.layer8.failure_history[d][strat] + penalty))
                    self.layer9.capture(d, unexplained, self.layer4.weights.get(d, 0.5))
                    self.layer4.weights[d] = max(0.20, min(1.0, self.layer4.weights[d] - self.hps["fail_value_decay"]))
                    self.layer1.seed_vector[d] = max(0.05, min(1.0, self.layer1.seed_vector[d] - self.hps["fail_seed_decay"]))
                self.layer2.blend_alpha[d] = 0.0
                self.layer8.active_hypothesis = None

        for d in self.dimensions:
            if d != active_dim and d in self.layer9.nodes: 
                self.layer9.nodes[d].radiate()
                
        mythology = self.layer10.weave_mythology(self.layer9.nodes, current_step)
                
        return {
            "step": current_step,
            "action": action,
            "bifurcated_info": bifurcated_info,
            "active_dimensions_現在数": len(self.dimensions),
            "personal_mythology_10層": {
                "archetype": mythology["archetype"],
                "narrative": mythology["narrative"]
            },
            "values_価値観の維持状態": {k: round(v, 3) for k, v in self.layer4.weights.items()},
            "accumulators_精神ストレス積分": {k: round(v, 3) for k, v in self.layer8.pressure_accumulator.items()}
        }
