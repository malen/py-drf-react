import json
import random
from datetime import datetime, timedelta

visitors = [
    "张三",
    "李四",
    "王五",
    "赵六",
    "孙七",
    "陈明",
    "刘洋",
    "高桥",
    "山田",
    "铃木",
]

hospitals = [
    "东京大学附属医院",
    "大阪市立综合医疗中心",
    "京都大学医学部附属医院",
    "东京医科大学医院",
    "横滨市民医院",
    "名古屋大学医院",
]

templates = [
    "患者在{hospital}接受医疗检查，使用AI辅助诊断系统对影像数据进行了分析，提高医疗效率。",
    "在{hospital}访问期间，体验了智能医疗设备在临床诊断中的应用，医疗数据实时更新。",
    "{hospital}引入医疗AI系统，用于患者管理与病历分析，提高医院整体医疗服务水平。",
    "医疗人员在{hospital}使用电子病历与AI辅助工具，对患者进行综合诊疗评估。",
    "远程医疗系统在{hospital}投入使用，患者通过AI问诊获得初步医疗建议。",
]


def random_date():
    start = datetime(2025, 1, 1)
    return (start + timedelta(days=random.randint(0, 500))).strftime("%Y-%m-%d")


data = []

for i in range(1000):
    visitor = random.choice(visitors) + str(i)
    hospital = random.choice(hospitals)
    content = random.choice(templates).format(hospital=hospital)

    data.append(
        {
            "visitor": visitor,
            "visit_date": random_date(),
            "visit_address": hospital,
            "visit_content": content,
        }
    )

with open("medical_visits_1000.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("done")
