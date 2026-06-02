import numpy as np

class NarrativeEcosystemAgentV180:
    def __init__(self):
        # 1. 内的欲求コア（Void）
        self.deficiencies = {"cognitive": 0.5, "uncertainty": 0.5, "boredom": 0.5}
        
        # 🌟【問題④改善】精神負荷（Mental Load）の導入。機械的タイマーを廃止
        self.mental_load = 0.0
        
        # 2. 世界構造ポピュレーション（W-Layer）
        self.world_hypotheses = {
            "W_linear_base": {
                "type": "LINEAR", "param": 0.5, "confidence": 0.5, "age": 0, "complexity": 1,
                "history_predictability": 1.0, "history_novelty": 0.1          
            },
            "W_phase_base": {
                "type": "PHASE_SHIFT", "param": 3.0, "confidence": 0.5, "age": 0, "complexity": 3,
                "history_predictability": 0.5, "history_novelty": 0.5
            }
        }
        
        # 3. 自己・人格ポピュレーション（S-Layer）
        # 🌟【問題③改善】血統主義を廃止し、二人の親（parent_a, parent_b）を持つ交配構造へ
        self.self_hypotheses = {
            "S_Alpha_v1": {"trigger": "cognitive", "confidence": 0.34, "age": 0, "parents": ("origin", "origin"), "generation": 1},
            "S_Beta_v1":  {"trigger": "uncertainty", "confidence": 0.33, "age": 0, "parents": ("origin", "origin"), "generation": 1},
            "S_Gamma_v1": {"trigger": "boredom", "confidence": 0.33, "age": 0, "parents": ("origin", "origin"), "generation": 1}
        }
        
        # 4. 🌟【問題②改善】意味付けのベクトル化（Meaning Vector）
        # 各ファクトフラグ（success/failure/chaos）を、3軸のどの比率で解釈するかのポートフォリオ
        self.meaning_rules = {
            "S_Alpha_v1": {
                "success": {"Autonomy": 0.7, "Order": 0.1, "Symbiosis": 0.2},
                "failure": {"Autonomy": 0.2, "Order": 0.6, "Symbiosis": 0.2},
                "chaos":   {"Autonomy": 0.8, "Order": 0.1, "Symbiosis": 0.1}
            },
            "S_Beta_v1": {
                "success": {"Autonomy": 0.1, "Order": 0.8, "Symbiosis": 0.1},
                "failure": {"Autonomy": 0.1, "Order": 0.7, "Symbiosis": 0.2},
                "chaos":   {"Autonomy": 0.0, "Order": 0.9, "Symbiosis": 0.1}
            },
            "S_Gamma_v1": {
                "success": {"Autonomy": 0.2, "Order": 0.2, "Symbiosis": 0.6},
                "failure": {"Autonomy": 0.1, "Order": 0.1, "Symbiosis": 0.8},
                "chaos":   {"Autonomy": 0.3, "Order": 0.1, "Symbiosis": 0.6}
            }
        }
        
        # 5. 🌟【問題①改善】信念体系（Belief）の完全ゼロサム・競争化
        # 初期状態でL1正規化（合計=1.0）
        self.belief_systems = {
            "S_Alpha_v1": {"Libertarianism": 0.6, "Authoritarianism": 0.2, "Communitarianism": 0.2},
            "S_Beta_v1":  {"Libertarianism": 0.2, "Authoritarianism": 0.6, "Communitarianism": 0.2},
            "S_Gamma_v1": {"Libertarianism": 0.2, "Authoritarianism": 0.2, "Communitarianism": 0.6}
        }
        
        # 6. 🌟【究極の進化】物語記憶層（Narrative Memory Layer）
        # 文化が独自に紡ぎ、語り継ぐ「主観的な神話・歴史的トラウマ」のアーカイブ
        self.narrative_memories = {
            "S_Alpha_v1": [], # 例: {"text": "我々は自由によって救われた", "impact": {"Libertarianism": 0.2}}
            "S_Beta_v1": [],
            "S_Gamma_v1": []
        }
        
        # 7. 価値観マトリクス（Value Matrix）
        self.value_matrix = {
            "S_Alpha_v1": {"predictability": 0.33, "novelty": 0.33, "symbiosis": 0.33},
            "S_Beta_v1":  {"predictability": 0.33, "novelty": 0.33, "symbiosis": 0.33},
            "S_Gamma_v1": {"predictability": 0.33, "novelty": 0.33, "symbiosis": 0.33}
        }

        self.current_dominant_W = "W_linear_base"
        self.current_dominant_S = "S_Beta_v1"
        self.regime_shift_count = 0
        self.mutation_count = 0

    def _execute_structure(self, w_type, param, last_val, complexity):
        if w_type == "LINEAR": 
            return last_val + (param * (1.0 + 0.05 * complexity))
        elif w_type == "MULTIPLY": 
            clipped_param = max(0.01, min(10.0, param))
            effective_param = max(0.1, min(5.0, clipped_param ** (1.0 + 0.02 * complexity)))
            return last_val * effective_param
        elif w_type == "PHASE_SHIFT": 
            thresh = param / (1.0 + 0.1 * complexity)
            return last_val * 1.8 if last_val > thresh else last_val * 0.4
        return 0.0

    def step_forward(self, actual_world_val, last_world_val, turn_idx):
        # ── ① 客観経験（Experience）の発生 ──
        expected_error = 0.0
        w_errors = {}
        w_preds = {}
        
        for wid, wdata in self.world_hypotheses.items():
            wdata["age"] += 1
            pred = self._execute_structure(wdata["type"], wdata["param"], last_world_val, wdata["complexity"])
            w_preds[wid] = pred
            error = abs(pred - actual_world_val)
            w_errors[wid] = error
            expected_error += wdata["confidence"] * error

            pred_delta = abs(pred - last_world_val)
            w_pred_success = max(0.0, 1.0 - error)
            wdata["history_predictability"] = 0.9 * wdata["history_predictability"] + 0.1 * w_pred_success
            wdata["history_novelty"] = 0.9 * wdata["history_novelty"] + 0.1 * pred_delta

        # ── ② Void（内的欲求）と🌟精神負荷（Mental Load）の更新 ──
        u_delta = (expected_error * 0.08) if expected_error > 0.5 else -0.06
        self.deficiencies["uncertainty"] = max(0.05, min(0.95, self.deficiencies["uncertainty"] + u_delta))

        dom_s_trigger = self.self_hypotheses[self.current_dominant_S]["trigger"]
        for v_key in self.deficiencies:
            if v_key == dom_s_trigger:
                self.deficiencies[v_key] = max(0.05, min(0.95, self.deficiencies[v_key] - 0.08))
            else:
                self.deficiencies[v_key] = max(0.05, min(0.95, self.deficiencies[v_key] + 0.05))

        # 🌟【問題④改善】精神負荷の蓄積。エラーの大きさと仮説突然変異の激しさに比例して脳が疲弊する
        self.mental_load += expected_error * 1.2
        
        # ── ③ 5層連鎖チェーン（意味ベクトル・ゼロサム信念・神話の書き込み） ──
        dom_w_error = w_errors[self.current_dominant_W]
        dom_w_pred_delta = abs(w_preds[self.current_dominant_W] - last_world_val)
        
        fact_tag = "success" if dom_w_error < 0.6 else "failure"
        if dom_w_pred_delta > 2.0:
            fact_tag = "chaos"

        for sid, sdata in list(self.self_hypotheses.items()):
            share = sdata["confidence"]
            learning_rate = 0.045 * share
            
            # Layer 2: 🌟【問題②改善】意味付けベクトル（Meaning Vector）の抽出
            m_vector = self.meaning_rules[sid].get(fact_tag, {"Autonomy": 0.33, "Order": 0.33, "Symbiosis": 0.33})
            
            # 成功体験に基づく意味ベクトルのマイルドなゆらぎ進化
            if fact_tag == "success" and np.random.rand() < 0.12:
                target_key = np.random.choice(["Autonomy", "Order", "Symbiosis"])
                self.meaning_rules[sid][fact_tag][target_key] = min(0.9, self.meaning_rules[sid][fact_tag][target_key] + 0.05)
                # 正規化
                m_sum = sum(self.meaning_rules[sid][fact_tag].values()) + 1e-9
                for k in self.meaning_rules[sid][fact_tag]: self.meaning_rules[sid][fact_tag][k] /= m_sum
            
            # Layer 3: 🌟【問題①改善】信念体系（Belief）の更新と完全ゼロサム（L1）競争化
            # 意味ベクトルの配分比率に応じて、各信念に推進力が分配される
            self.belief_systems[sid]["Libertarianism"] += learning_rate * m_vector["Autonomy"]
            self.belief_systems[sid]["Authoritarianism"] += learning_rate * m_vector["Order"]
            self.belief_systems[sid]["Communitarianism"] += learning_rate * m_vector["Symbiosis"]
            
            # 「脅威」による防衛的秩序引き込み
            if fact_tag in ["failure", "chaos"]:
                self.belief_systems[sid]["Authoritarianism"] += learning_rate * 0.2

            # 🌟 ゼロサム拘束：全肯定ドグマを破壊し、思想を奪い合わせる
            for b_key in self.belief_systems[sid]:
                self.belief_systems[sid][b_key] = max(0.05, self.belief_systems[sid][b_key])
            b_total = sum(self.belief_systems[sid].values()) + 1e-9
            for b_key in self.belief_systems[sid]:
                self.belief_systems[sid][b_key] = (self.belief_systems[sid][b_key] / b_total) * 1.5 # 総和を1.5に固定

            # 🌟【究極進化：物語（Narrative）の自発的生成と書き込み】
            # 歴史的な大成功（超予測）または大トラウマ（大破滅）が起きた時、主流派思想はそれを「神話・記憶」として刻む
            if share > 0.40 and (fact_tag == "chaos" or dom_w_error < 0.15):
                narrative_impact = {"Libertarianism": m_vector["Autonomy"] * 0.15, "Authoritarianism": m_vector["Order"] * 0.15, "Communitarianism": m_vector["Symbiosis"] * 0.15}
                if dom_w_error < 0.15:
                    story_text = f"【神話】我々は{max(m_vector, key=m_vector.get)}の調和によって救われた(Turn {turn_idx})"
                else:
                    story_text = f"【大災害記憶】{max(m_vector, key=m_vector.get)}の混沌が世界を襲った(Turn {turn_idx})"
                
                # 最大3つまで物語を記憶（古いものは忘却される）
                self.narrative_memories[sid].append({"text": story_text, "impact": narrative_impact})
                if len(self.narrative_memories[sid]) > 3:
                    self.narrative_memories[sid].pop(0)

            # Layer 4: 価値観（Value）の湧出 ＋ 🌟【物語による主観バイアス補正】
            # 信念ベースの基本価値に、蓄積された「過去の神話（Narrative）」の補正値が加算される
            story_bias = {"Libertarianism": 0.0, "Authoritarianism": 0.0, "Communitarianism": 0.0}
            for story in self.narrative_memories[sid]:
                for k, v in story["impact"].items():
                    story_bias[k] += v

            self.value_matrix[sid]["novelty"] = self.belief_systems[sid]["Libertarianism"] + story_bias["Libertarianism"]
            self.value_matrix[sid]["predictability"] = self.belief_systems[sid]["Authoritarianism"] + story_bias["Authoritarianism"]
            self.value_matrix[sid]["symbiosis"] = self.belief_systems[sid]["Communitarianism"] + story_bias["Communitarianism"]

            # 価値観のL1正規化
            v_mat = self.value_matrix[sid]
            v_total = v_mat["predictability"] + v_mat["novelty"] + v_mat["symbiosis"] + 1e-9
            for key in v_mat:
                v_mat[key] = max(0.05, (v_mat[key] / v_total) * 1.0)

        # ── 🌟【問題④改善】動的睡眠・内省（Mental Load Triggered Consolidation） ──
        # 精神負荷が臨界値（5.0）を突破した時に、自発的に深い睡眠・内省に入る
        if self.mental_load > 5.0:
            rest_strength = 0.15 + (self.deficiencies["boredom"] * 0.15)
            
            for sid in list(self.self_hypotheses.keys()):
                # 1. 信念をゆるやかに中央値へ回帰（過激化のクールダウン）
                for b_key in self.belief_systems[sid]:
                    val = self.belief_systems[sid][b_key]
                    self.belief_systems[sid][b_key] = val * (1.0 - rest_strength) + 0.5 * rest_strength
                # 2. 弱い思想の忘却
                if self.self_hypotheses[sid]["confidence"] < 0.15:
                    self.self_hypotheses[sid]["confidence"] *= (1.0 - rest_strength * 0.5)
            
            # 負荷の完全リセットと欲求の浄化
            self.mental_load = 0.0
            self.deficiencies["boredom"] = max(0.05, self.deficiencies["boredom"] - 0.30)
            self.deficiencies["cognitive"] = max(0.05, self.deficiencies["cognitive"] - 0.20)
            print(f" 🌙 【動的睡眠フェーズ】 Turn {turn_idx} - 精神負荷限界につき脳内をリフレッシュ。過学習を解除しました。")

        # ── ④ 世界構造（W）のレプリケーター淘汰 ──
        raw_fitness = {}
        current_values = self.value_matrix[self.current_dominant_S]

        for wid, wdata in self.world_hypotheses.items():
            error = w_errors[wid]
            bias_p = current_values["predictability"] * wdata["history_predictability"]
            bias_n = current_values["novelty"] * wdata["history_novelty"]
            bias_s = current_values["symbiosis"] * (1.0 - error) 
            
            stabilized_bias = (bias_p + bias_n + bias_s) ** 0.5
            complexity_penalty = 0.08 * (wdata["complexity"] - 1)
            raw_fitness[wid] = np.exp(-(error + complexity_penalty) * 1.1) * stabilized_bias

        total_fit = sum(raw_fitness.values()) + 1e-9
        floor_base = min(0.12, 0.005 + (self.deficiencies["boredom"] * 0.02) + (current_values["symbiosis"] * 0.04))
        
        for k in self.world_hypotheses:
            self.world_hypotheses[k]["confidence"] = (1.0 - floor_base) * (raw_fitness[k] / total_fit) + (floor_base / len(self.world_hypotheses))

        self.world_hypotheses = {k: v for k, v in self.world_hypotheses.items() if v["confidence"] > 0.005}
        if not self.world_hypotheses:
            self.world_hypotheses = {"W_linear_emergency": {"type": "LINEAR", "param": 0.5, "confidence": 1.0, "age": 0, "complexity": 1, "history_predictability": 0.5, "history_novelty": 0.5}}

        # ── ⑤ 世界観（W）の突然変異 ──
        if len(self.world_hypotheses) < 5 and np.random.rand() < (0.15 + current_values["novelty"] * 0.20):
            dom_w = max(self.world_hypotheses, key=lambda k: self.world_hypotheses[k]["confidence"])
            new_id = f"W_turn{turn_idx}_{len(self.world_hypotheses) + 1}"
            p_love, n_love = current_values["predictability"], current_values["novelty"]
            type_probs = np.array([p_love * 1.5, n_love * 1.0, n_love * 1.5]) / (p_love * 1.5 + n_love * 2.5 + 1e-9)
            next_type = np.random.choice(["LINEAR", "MULTIPLY", "PHASE_SHIFT"], p=type_probs)
            
            self.world_hypotheses[new_id] = {
                "type": next_type, "param": 1.2 if next_type != "MULTIPLY" else 1.05, 
                "confidence": 0.12, "age": 0, "complexity": int(max(1, min(5, self.world_hypotheses[dom_w]["complexity"] + np.random.choice([-1, 0, 1])))),
                "history_predictability": 0.4 + (p_love * 0.4), "history_novelty": n_love * 0.8
            }
            self.mutation_count += 1

        # ── ⑥ 🌟【問題③改善】ミームの文化交配・ハイブリッド繁殖（Meme Crossover） ──
        cultural_fitness = {}
        for sid, sdata in self.self_hypotheses.items():
            pred_contribution = 1.0 - dom_w_error
            meaning_stability = 1.0 - np.std(list(self.belief_systems[sid].values()))
            cultural_fitness[sid] = sdata["confidence"] * 0.5 + max(0.1, pred_contribution * meaning_stability) * 0.5

        # 8%の確率で、プール内の上位2つの覇権思想が交雑し、「新イデオロギー（子供）」が誕生する
        if len(self.self_hypotheses) < 5 and np.random.rand() < 0.08 and len(self.self_hypotheses) >= 2:
            sorted_s = sorted(cultural_fitness, key=cultural_fitness.get, reverse=True)
            parent_a, parent_b = sorted_s[0], sorted_s[1]
            child_id = f"S_mix_turn{turn_idx}"
            
            # 親の世代情報の継承
            max_gen = max(self.self_hypotheses[parent_a]["generation"], self.self_hypotheses[parent_b]["generation"])
            self.self_hypotheses[child_id] = {
                "trigger": np.random.choice([self.self_hypotheses[parent_a]["trigger"], self.self_hypotheses[parent_b]["trigger"]]),
                "confidence": 0.10, "age": 0, "parents": (parent_a, parent_b), "generation": max_gen + 1
            }
            
            # 🌟 ミーム交配：信念と意味解釈ルールを50%ずつ融合（ハイブリッド創発）
            self.belief_systems[child_id] = {}
            for k in self.belief_systems[parent_a]:
                self.belief_systems[child_id][k] = 0.5 * self.belief_systems[parent_a][k] + 0.5 * self.belief_systems[parent_b][k]
                
            self.meaning_rules[child_id] = {}
            for tag in ["success", "failure", "chaos"]:
                self.meaning_rules[child_id][tag] = {}
                for axis in ["Autonomy", "Order", "Symbiosis"]:
                    self.meaning_rules[child_id][tag][axis] = 0.5 * self.meaning_rules[parent_a][tag][axis] + 0.5 * self.meaning_rules[parent_b][tag][axis]
            
            # 物語（歴史観）のブレンド継承
            self.narrative_memories[child_id] = (self.narrative_memories[parent_a] + self.narrative_memories[parent_b])[:2]
            self.value_matrix[child_id] = self.value_matrix[parent_a].copy()
            
            print(f" 🧬 【ミームの文化交配】 【{parent_a}】×【{parent_b}】が交雑し、新思想【{child_id}】が創発・誕生！")

        # 支持率の慣性アップデート
        for sid, sdata in self.self_hypotheses.items():
            sdata["confidence"] = (0.80 * sdata["confidence"]) + (0.20 * self.deficiencies[sdata["trigger"]])

        # 淘汰圧
        if len(self.self_hypotheses) > 3:
            weakest_sid = min(cultural_fitness, key=cultural_fitness.get)
            if weakest_sid != self.current_dominant_S and self.self_hypotheses[weakest_sid]["confidence"] < 0.035:
                print(f" 🪦 【思想淘汰】 交配レースについていけず【{weakest_sid}】が忘却されました。")
                del self.self_hypotheses[weakest_sid]
                del self.meaning_rules[weakest_sid]
                del self.belief_systems[weakest_sid]
                del self.value_matrix[weakest_sid]
                del self.narrative_memories[weakest_sid]

        # 最終正規化
        total_p = sum(w["confidence"] for w in self.world_hypotheses.values())
        for k in self.world_hypotheses: self.world_hypotheses[k]["confidence"] /= total_p
        total_s = sum(v["confidence"] for v in self.self_hypotheses.values())
        for k in self.self_hypotheses: self.self_hypotheses[k]["confidence"] /= total_s

        self.current_dominant_W = max(self.world_hypotheses, key=lambda k: self.world_hypotheses[k]["confidence"])
        self.current_dominant_S = max(self.self_hypotheses, key=lambda k: self.self_hypotheses[k]["confidence"])

    def print_status(self, turn, actual, last):
        print(f"\n■ Turn: {turn} | Fact: Last={last:.2f} ➔ Actual={actual:.2f} | 🧠 精神負荷:{self.mental_load:.2f}")
        print(f" 🪐 [脳内思想神話ポピュレーションログ]")
        for sid in self.self_hypotheses:
            dom_marker = "👑" if sid == self.current_dominant_S else "  "
            b = self.belief_systems[sid]
            v = self.value_matrix[sid]
            print(f"   {dom_marker} {sid} (Gen.{self.self_hypotheses[sid]['generation']}) Share:{self.self_hypotheses[sid]['confidence']*100:.1f}%")
            print(f"     ├ 親系統 ➔ {self.self_hypotheses[sid]['parents']}")
            print(f"     ├ 信念(ゼロサム) ➔ [自由:{b['Libertarianism']:.2f} | 秩序:{b['Authoritarianism']:.2f} | 共生:{b['Communitarianism']:.2f}]")
            print(f"     ├ 価値(物語補正済) ➔ [新奇:{v['novelty']:.2f} | 予測:{v['predictability']:.2f} | 共生:{v['symbiosis']:.2f}]")
            stories = [s["text"] for s in self.narrative_memories[sid]]
            print(f"     └ 紡がれた神話(Narrative) ➔ {stories if stories else 'なし（まだ歴史を持たぬ思想）'}")
        print(f" 🔄 [W-Layer 主流派世界観] 【{self.current_dominant_W}】 Share:{self.world_hypotheses[self.current_dominant_W]['confidence']*100:.1f}%")


# ==================== 200ターン神話創発・文化交配シミュレーション ====================
if __name__ == "__main__":
    agent = NarrativeEcosystemAgentV180()
    print("==========================================================")
    print(" v18.0 主観的神話創発・文化交配生態系シミュレータ")
    print("==========================================================")
    
    def generate_environment_value(t):
        if t <= 50: return 1.0 + (t * 0.01) 
        elif t <= 100: return 1.5 + (t - 50) * 0.4 
        elif t <= 150: return 21.5 + np.random.uniform(-5.0, 5.0) # カオス期
        else: return 40.0 if (t % 10 < 5) else 5.0 # 激しい相転移期

    last_val = 1.0
    for turn in range(1, 201):
        actual_val = generate_environment_value(turn)
        agent.step_forward(actual_val, last_val, turn)
        
        if turn in [1, 25, 51, 75, 101, 125, 151, 175, 200]:
            print(f"\n--- ⏳ 精神史・神話の創発ログ (v18.0) ---")
            agent.print_status(turn, actual_val, last_val)
            
        last_val = actual_val
