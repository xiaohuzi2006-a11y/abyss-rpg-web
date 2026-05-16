import streamlit as st
import requests
import json
import os


# ==========================================
# 1. 核心图纸 (Classes) - 加入打怪升级引擎
# ==========================================
class Hero:
    def __init__(self, name, hp, max_hp, attack_power, gold=0, level=1, exp=0):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack_power = attack_power
        self.gold = gold
        self.level = level
        self.exp = exp

    def attack(self, target):
        target.hp -= self.attack_power

    def gain_exp(self, amount):
        self.exp += amount
        log_msg = f"✨ 获得 {amount} 点经验！\n"
        max_exp_needed = self.level * 100

        while self.exp >= max_exp_needed:
            self.exp -= max_exp_needed
            self.level += 1
            self.max_hp += 200
            self.hp = self.max_hp
            self.attack_power += 50
            log_msg += f"🎉 升级啦！当前等级: Lv.{self.level}！属性大幅提升，生命回满！\n"
            max_exp_needed = self.level * 100

        return log_msg


class Monster:
    def __init__(self, name, hp, attack_power, drop_item):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.drop_item = drop_item


# ==========================================
# 2. 存档系统 - 兼容新属性的读写
# ==========================================
def load_game():
    if os.path.exists("web_save.json"):
        with open("web_save.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # 使用 .get() 可以兼容老存档，老存档没 level 默认给 1
            return Hero(
                name=data.get("name", "奶牛"),
                hp=data.get("hp", 1000),
                max_hp=data.get("max_hp", 1000),
                attack_power=data.get("attack_power", 150),
                gold=data.get("gold", 0),
                level=data.get("level", 1),
                exp=data.get("exp", 0)
            )
    return Hero("奶牛", 1000, 1000, 150)


def save_game(player):
    with open("web_save.json", "w", encoding="utf-8") as f:
        json.dump({
            "name": player.name,
            "hp": player.hp,
            "max_hp": player.max_hp,
            "attack_power": player.attack_power,
            "gold": player.gold,
            "level": player.level,  # 保存等级
            "exp": player.exp  # 保存经验
        }, f)


# ==========================================
# 3. 初始化世界记忆 (Session State)
# ==========================================
if 'player' not in st.session_state:
    st.session_state.player = load_game()
if 'monster' not in st.session_state:
    st.session_state.monster = Monster("哥布林", 300, 20, "Goblin Ear")
if 'log' not in st.session_state:
    st.session_state.log = "⚔️ 欢迎来到深渊探索...\n"
if 'joke' not in st.session_state:
    st.session_state.joke = ""

player = st.session_state.player
monster = st.session_state.monster

# ==========================================
# 4. 侧边栏：国际黑市 (Shop)
# ==========================================
with st.sidebar:
    st.header("🛒 国际黑市")
    st.write("神秘的外国商人向你敞开大门：'Show me your gold!'")
    st.info(f"💳 你的余额: {player.gold} 金币")

    st.divider()
    st.write("🗡️ **Iron Sword (铁剑)** - +50 攻击力")
    if st.button("购买 Iron Sword (50 金币)"):
        if player.gold >= 50:
            player.gold -= 50
            player.attack_power += 50
            st.success("购买成功！攻击力提升！")
        else:
            st.error("金币不足！")

    st.write("🧪 **Health Potion (恢复药水)** - 回复 300 HP")
    if st.button("购买 Potion (30 金币)"):
        if player.gold >= 30:
            player.gold -= 30
            player.hp = min(player.hp + 300, player.max_hp)
            st.success("咕噜咕噜... HP 恢复了！")
        else:
            st.error("金币不足！")

# ==========================================
# 5. 网页视觉布局 (UI) - 图片与等级面板
# ==========================================
st.set_page_config(page_title="深渊探索 RPG", page_icon="⚔️")
st.title("⚔️ 深渊探索 RPG - 视觉与数值觉醒版")

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"🦸‍♂️ Lv.{player.level} {player.name}")
    st.caption(f"✨ EXP: {player.exp} / {player.level * 100}")

    try:
        st.image("hero.jpg", use_container_width=True)  # 如果你用的是 png，改这里！
    except FileNotFoundError:
        st.info("🖼️ 等待画师提交英雄立绘...")

    hp_ratio = max(0.0, min(1.0, player.hp / player.max_hp))
    st.write(f"🩸 HP: {player.hp} / {player.max_hp}")
    st.progress(hp_ratio)
    st.write(f"⚔️ 攻击: {player.attack_power} | 💰 金币: {player.gold}")

with col2:
    st.subheader(f"👹 {monster.name}")

    try:
        st.image("goblin.jpg", use_container_width=True)  # 如果你用的是 png，改这里！
    except FileNotFoundError:
        st.info("🖼️ 等待画师提交怪物立绘...")

    g_hp_ratio = max(0.0, min(1.0, monster.hp / 300))
    st.write(f"🩸 HP: {monster.hp} / 300")
    st.progress(g_hp_ratio)
    st.write(f"🎁 掉落: {monster.drop_item}")

st.divider()

# ==========================================
# 6. 战斗交互逻辑
# ==========================================
if st.button("挥剑攻击！ ⚔️", type="primary", use_container_width=True):
    player.attack(monster)
    st.session_state.log += f"🗡️ 你对 {monster.name} 造成了 {player.attack_power} 点伤害！\n"

    if monster.hp > 0:
        player.hp -= monster.attack_power
        st.session_state.log += f"💥 {monster.name} 反击了！你受到了 {monster.attack_power} 点伤害！\n"
        if player.hp <= 0:
            st.session_state.log += "💀 你阵亡了... 请刷新页面重新开始。\n"
    else:
        st.session_state.log += f"💀 {monster.name} 被击败了！\n"
        st.session_state.log += f"💰 获得了 20 金币！\n"
        player.gold += 20

        # 获取经验并判断是否升级
        exp_msg = player.gain_exp(50)
        st.session_state.log += exp_msg

        # 刷新一只新王一成
        st.session_state.monster = Monster("哥布林", 300, 20, "Goblin Ear")

# ==========================================
# 7. 智慧酒馆 (API 交互)
# ==========================================
st.divider()
st.subheader("🍺 智慧酒馆")

if st.session_state.joke:
    st.info(f"【老板说】：{st.session_state.joke}")

if st.button("找老板聊聊（听笑话提升生命上限）"):
    try:
        res = requests.get("https://v2.jokeapi.dev/joke/Any", timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get("type") == "single":
                st.session_state.joke = data["joke"]
            elif data.get("type") == "twopart":
                st.session_state.joke = f"{data['setup']} —— {data['delivery']}"
            else:
                st.session_state.joke = "老板今天不想说话。"

            player.max_hp += 10
            player.hp += 10
            st.session_state.log += "💖 听了老板的笑话，心情大好，生命上限 +10！\n"
        else:
            st.error(f"服务器抗议了，状态码: {res.status_code}")

    except Exception as e:
        st.error(f"📡 酒馆断网了。真实报错原因：{e}")

# ==========================================
# 8. 战斗日志显示
# ==========================================
st.divider()
st.text_area("📜 战斗日志", value=st.session_state.log, height=200)

# ==========================================
# 9. 手动存档按钮
# ==========================================
st.divider()
if st.button("💾 在篝火旁休息（保存游戏）"):
    save_game(player)
    st.success("✅ 游戏进度已保存！")