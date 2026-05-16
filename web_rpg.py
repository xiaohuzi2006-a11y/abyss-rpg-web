import streamlit as st
import requests
import json
import os


# ==========================================
# 1. 核心图纸 (Classes)
# ==========================================
class Hero:
    def __init__(self, name, hp, max_hp, attack_power, gold=0):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack_power = attack_power
        self.gold = gold

    def attack(self, target):
        target.hp -= self.attack_power


class Monster:
    def __init__(self, name, hp, attack_power, drop_item):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.drop_item = drop_item

    def attack(self, target):
        target.hp -= self.attack_power


# ==========================================
# 2. 自动读档与初始化逻辑 (核心升级)
# ==========================================
# 只要不刷新网页，session_state 就会保留；如果刷新，则尝试从 JSON 文件读取
if 'player' not in st.session_state:
    # 检查本地是否有存档文件
    if os.path.exists("web_save.json"):
        with open("web_save.json", "r", encoding="utf-8") as f:
            save_data = json.load(f)

        # 使用存档数据初始化英雄
        st.session_state.player = Hero(
            save_data["name"],
            save_data["hp"],
            save_data["max_hp"],
            save_data["attack_power"],
            save_data["gold"]
        )
        st.toast("📂 存档已自动加载！欢迎回来，大侠。")
    else:
        # 没有任何存档时，创建初始亚瑟
        st.session_state.player = Hero("亚瑟", 1000, 1000, 150)

if 'goblin' not in st.session_state:
    st.session_state.goblin = Monster("哥布林", 500, 150, "Goblin Ear")

if 'battle_log' not in st.session_state:
    st.session_state.battle_log = ["📜 冒险开始了..."]

if 'joke' not in st.session_state:
    st.session_state.joke = "🍺 酒馆老板正忙着擦杯子，还没说话。"

# 简化对象引用
player = st.session_state.player
goblin = st.session_state.goblin

# ==========================================
# 3. 网页视觉布局 (UI)
# ==========================================
st.set_page_config(page_title="深渊探索 RPG", page_icon="⚔️")
st.title("⚔️ 深渊探索 RPG - 网页完全体")
# ==========================================
# 🎁 新增模块：国际黑市 (Global Item Shop)
# ==========================================
# 使用 with 语句，下面所有缩进的内容都会自动放进侧边栏！
with st.sidebar:
    st.title("🛒 Global Black Market")
    st.write("神秘的外国商人向你敞开大门：'Show me your gold!'")

    # 商店库存字典
    shop_items = {
        "Iron Sword (铁剑)": {"cost": 50, "attack": 100, "type": "weapon"},
        "Health Potion (恢复药水)": {"cost": 30, "heal": 200, "type": "potion"},
        "Dragon Armor (龙鳞甲)": {"cost": 100, "max_hp": 500, "type": "armor"}
    }

    # 这里的 st.info 会自动变成 st.sidebar.info
    st.info(f"💳 Your Balance: {player.gold} Gold")

    for item_name, stats in shop_items.items():
        st.write(f"**{item_name}**")
        st.write(f"🪙 Price: {stats['cost']} Gold")

        # 这里的 st.button 也会自动放进侧边栏
        if st.button(f"Buy {item_name.split(' ')[0]}"):
            if player.gold >= stats['cost']:
                player.gold -= stats['cost']

                if stats['type'] == "weapon":
                    player.attack_power += stats['attack']
                    st.success(f"⚔️ Attack Up! (+{stats['attack']})")

                elif stats['type'] == "potion":
                    player.hp = min(player.max_hp, player.hp + stats['heal'])
                    st.success(f"🧪 HP Recovered! (+{stats['heal']})")

                elif stats['type'] == "armor":
                    player.max_hp += stats['max_hp']
                    player.hp += stats['max_hp']
                    st.success(f"🛡️ Max HP Up! (+{stats['max_hp']})")

                st.rerun()

            else:
                st.error("❌ Not enough gold!")

    st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"🦸‍♂️ {player.name}")
    # 确保进度条比例在 0.0 到 1.0 之间
    hp_ratio = max(0.0, min(1.0, player.hp / player.max_hp))
    st.write(f"🩸 HP: {player.hp} / {player.max_hp}")
    st.progress(hp_ratio)
    st.write(f"⚔️ 攻击: {player.attack_power} | 💰 金币: {player.gold}")

with col2:
    st.subheader(f"👹 {goblin.name}")
    g_hp_ratio = max(0.0, min(1.0, goblin.hp / 300))
    st.write(f"🩸 HP: {goblin.hp} / 300")
    st.progress(g_hp_ratio)
    st.write(f"🎁 掉落: {goblin.drop_item}")

st.divider()

# ==========================================
# 4. 战斗交互逻辑
# ==========================================
if player.hp > 0 and goblin.hp > 0:
    if st.button("挥剑攻击！ ⚔️", type="primary", use_container_width=True):
        # 1. 玩家攻击
        player.attack(goblin)
        st.session_state.battle_log.append(f"🗡️ 你砍了哥布林一剑，造成 {player.attack_power} 点伤害！")

        # 2. 怪物反击
        if goblin.hp > 0:
            goblin.attack(player)
            st.session_state.battle_log.append(f"🐾 哥布林反击，造成 {goblin.attack_power} 点伤害！")
        else:
            st.session_state.battle_log.append(f"🏆 击败了哥布林！获得 20 金币！")
            player.gold += 20
            st.balloons()

        st.rerun()

elif goblin.hp <= 0:
    st.success("🎉 哥布林已倒下！你可以继续去酒馆增强实力或保存进度。")
    if st.button("复活怪物"):
        st.session_state.goblin.hp = 300
        st.rerun()

elif player.hp <= 0:
    st.error("☠️ 你已力战而亡。")
    if st.button("满血复活"):
        st.session_state.player.hp = st.session_state.player.max_hp
        st.rerun()

st.divider()

# --- 智慧酒馆 (API 联动) ---
st.write("### 🍺 智慧酒馆")
st.info(st.session_state.joke)

if st.button("找老板聊聊（听笑话提升生命上限）", use_container_width=True):
    try:
        url = "https://official-joke-api.appspot.com/random_joke"
        res = requests.get(url, timeout=5)
        data = res.json()
        st.session_state.joke = f"【老板说】：{data['setup']} —— {data['punchline']}"
        player.max_hp += 50
        player.hp = player.max_hp  # 补满血
        st.toast("✨ 生命上限提升了！")
        st.rerun()
    except:
        st.error("📡 酒馆断网了。")

st.divider()

# --- 记忆神殿 (存档功能) ---
st.write("### 💾 记忆神殿")
col_save, col_clear = st.columns(2)

with col_save:
    if st.button("💾 保存当前进度", use_container_width=True):
        save_data = {
            "name": player.name,
            "hp": player.hp,
            "max_hp": player.max_hp,
            "attack_power": player.attack_power,
            "gold": player.gold
        }
        with open("web_save.json", "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=4)
        st.success("进度已保存！下次打开会自动加载。")

with col_clear:
    if st.button("🗑️ 删除存档并重置", use_container_width=True):
        if os.path.exists("web_save.json"):
            os.remove("web_save.json")
        st.cache_data.clear()
        st.write("存档已删，请手动刷新页面重置游戏。")

st.divider()

# --- 战斗日志 ---
st.write("### 📜 冒险记录")
for log in reversed(st.session_state.battle_log):
    st.write(log)

