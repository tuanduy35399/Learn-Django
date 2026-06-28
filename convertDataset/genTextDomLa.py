import random

# Seed for reproducibility if needed, but we want variation
random.seed(42)

# Tone components for Farmer style: Southern/Rustic Vietnamese
# "Bề mặt lá mai nhà em bị nổi các đốm nhỏ xíu như đầu kim, tâm màu đen và có viền vàng bao quanh rải rác khắp nơi"

subjects = [
    "Lá mai nhà em", "Mấy cây mai sau vườn", "Chậu mai trước sân", "Mấy nhánh mai già dưới gốc", "Đọt mai non", 
    "Cây mai vàng chưng tết", "Mấy cây mai bồn", "Lá mai già", "Bìa lá mai", "Mấy cái lá mai dưới thấp",
    "Cây mai nhà tôi", "Mấy gốc mai ngoài vườn", "Lá trên cây mai", "Mấy chậu mai bonsai", "Tàng lá mai dưới gốc",
    "Đọt non cây mai", "Mấy cái lá già", "Mấy nhánh mai sát đất", "Cây mai vàng nuôi mấy năm nay", "Lá mai ở tầng dưới"
]

spots_desc = [
    "bị nổi mấy cái đốm nhỏ xíu như đầu kim, ở giữa màu đen màu nâu mà có cái quầng vàng bao quanh",
    "nổi mấy vết tròn nhỏ màu nâu đen, nhìn kỹ thấy có cái vòng màu vàng nhạt bao xung quanh",
    "xuất hiện đầy mấy cái chấm li ti màu nâu, chung quanh có vệt vàng lạt lạt nhìn lạ lắm",
    "bị lốm đốm mấy vết tròn màu đen thui, viền xung quanh màu vàng sáng rải rác khắp nơi",
    "xuất hiện vệt tròn nhỏ màu nâu sậm, xung quanh đốm đó có cái quầng màu vàng chanh",
    "bị mấy cái chấm tròn nhỏ màu đen, nhìn như bị tàn nhang mà có quầng vàng bao bọc",
    "có mấy đốm tròn nhỏ xíu màu nâu đen, chung quanh có vệt màu vàng nhạt lan ra",
    "bị nổ mấy cái chấm màu nâu, cái viền bên ngoài màu vàng nhẹ nhìn ngộ lắm",
    "nổi đầy vết đốm màu đen sậm, xung quanh vết đó có cái vòng tròn màu vàng bao quanh",
    "có mấy cái chấm màu nâu đen bé tí, nhìn kỹ thấy có cái viền vàng bao bọc xung quanh"
]

spread_desc = [
    "mấy cái đốm này lúc đầu ở lá già dưới gốc xong giờ thấy nó lan lên tới đọt non luôn",
    "nó bị ở mấy cái lá già dày đặc luôn rồi giờ ăn lan qua tới mấy cái chồi non trên ngọn",
    "mấy đốm đó xuất hiện nhiều trên lá già trước, xong giờ thấy nó ăn qua lá non hết trơn",
    "mới đầu thấy ở dưới gốc thôi mà nay thấy lá non với đọt non cũng bị dính vệt vàng luôn",
    "bệnh này từ lá già bên dưới rồi từ từ lan rộng ra mấy cái chồi non mới nhú trên cao",
    "mấy cái vết này ăn từ lá già dưới thấp rồi lan dần lên mấy cái lá non phía trên ngọn",
    "nó bám đầy trên mấy lá già rồi giờ thấy đọt non chồi non cũng bị quầng vàng nhạt nhạt",
    "mấy đốm nhỏ đó tụ lại trên lá già nhiều lắm, xong giờ thấy lan ra mấy nhánh non luôn",
    "lúc đầu bị mấy lá già sát đất thôi mà nay thấy chồi non đọt non cũng bị lốm đốm theo",
    "mấy vệt đó xuất hiện ở lá già trước, xong xuôi giờ lan ra mấy cái đọt non nhìn xơ xác"
]

severe_desc = [
    "nặng quá mấy cái đốm nó dính lại thành mảng lớn màu nâu đen làm lá cháy rụi luôn",
    "bây giờ mấy vết đó bự ra, dính chùm lại thành đốm lớn màu nâu làm lá quăn queo hết",
    "đốm nhỏ dính lại thành mảng lớn màu nâu sậm, bìa lá bị cháy khô quéo lại mất hình dạng",
    "vết bệnh lan rộng ra thành mảng lớn màu đen, lá bị vàng rồi cháy lỗ chỗ nhìn xơ xác",
    "mấy đốm đó dính lại với nhau thành mảng lớn bất định, làm cái bìa lá cháy khô quéo luôn",
    "bị nặng quá nên mấy đốm dính chùm lại thành mảng màu nâu đen, lá quăn queo rụng sạch bách",
    "mấy vệt đó ăn lan ra thành đốm bự màu nâu, lá mai bị cháy khô rồi thủng lỗ chỗ hết",
    "bệnh nặng làm mấy đốm gom lại thành vệt lớn màu nâu sậm, làm cháy bìa lá quăn tít lại",
    "mấy đốm nhỏ giờ dính thành mảng lớn màu đen thui, lá mai bị vàng rực rồi cháy khô hết",
    "vết bệnh loang ra thành mảng bự màu nâu đen, làm lá mai bị cháy bìa quăn queo hết trơn"
]

consequence_desc = [
    "làm cho cái đọt bị cháy khô, cây mai chậm lớn, còi cọc thấy thương luôn á",
    "nhánh non bị cháy xong lá rụng ráo trọi, đọt khô quắt lại làm cây hổng lớn nổi",
    "mấy cái đọt non bị cháy khô hết, cây mai còi cọc hẳn đi, kiểu này chắc tết hổng có hoa đẹp",
    "làm lá bị cháy rồi rụng sạch bách, đọt non cũng khô luôn, cây mai nhìn còi cọc quá chừng",
    "nhánh non bị nhiễm bệnh làm lá cháy rụng hết, đọt khô làm cây mai hổng ra hoa đẹp nổi",
    "làm cho cây mai chậm phát triển, còi cọc, mấy cái đọt bị cháy khô hết trơn rồi",
    "đọt non bị cháy khô quéo, lá rụng rớt đầy gốc, cây mai còi cọc hổng chịu đâm chồi",
    "làm cái đọt bị cháy khô rụng lá, cây mai vàng còi cọc, tết này chắc hoa ra xấu hoắc",
    "mấy nhánh non cháy lá rồi rụng sạch, đọt khô queo, cây mai còi cọc thấy mà rầu",
    "làm cho cây mai chậm lớn, đọt non cháy khô hết, kiểu này hoa ra hổng có đẹp đẽ gì"
]

# General questions (~5% -> 40 sentences)
questions = [
    "Cây mai của tôi đang bị tình trạng lá xuất hiện các đốm tròn nhỏ màu nâu đen, nhìn kỹ thấy có quầng vàng sáng xung quanh đốm. Làm sao để cứu cây mai đây, phun thuốc gì, phun 1 lượng bao nhiêu",
    "Mấy cây mai nhà em tự nhiên lá nổi đốm vàng đốm đen đầy hết trơn, hổng biết bị bệnh gì và mua thuốc nào xịt cho nó hết vậy các bác",
    "Cây mai vàng bị đốm lá nặng quá, lá rụng trắng gốc rồi, giờ có thuốc gì đặc trị chỉ giùm em với chứ rầu quá chừng",
    "Cho hỏi cây mai bị đốm tròn màu nâu có viền vàng là bệnh gì vậy ạ, ra tiệm bảo vệ thực vật mua thuốc gì phun là hiệu quả nhất",
    "Mấy anh chị cho em hỏi cây mai bị cháy bìa lá với nổi đốm đen đầy lá già là bị gì, có cách nào cứu chữa hổng chỉ em với",
    "Cây mai nhà em bị đốm lá dữ quá, đọt non cháy khô hết rồi, giờ phải bón phân hay xịt thuốc gì để nó ra chồi lại vậy",
    "Có ai biết thuốc nào trị dứt điểm bệnh đốm lá quầng vàng trên cây mai không, chỉ giùm tôi với chứ cây mai sắp chết khô rồi",
    "Cây mai bị đốm đen viền vàng xung quanh lá, lan từ lá già lên lá non thì phun thuốc gì và liều lượng ra sao vậy mọi người",
    "Giúp em với, chậu mai trước nhà bị nổi chấm li ti màu nâu đen rồi cháy quăn queo hết lá, giờ xịt thuốc gì cho mau hết bệnh",
    "Mấy gốc mai bồn bị đốm lá vàng đen rụng hết trơn, giờ có cách nào khắc phục hay phun thuốc gì chữa trị kịp tết không ạ"
]

# Empty/Vague sentences (~5% -> 40 sentences)
vague = [
    "Trời mưa xuống cái mấy cây mai trong vườn nhìn đổ bệnh thấy mà phát rầu luôn á",
    "Nhìn vườn mai năm nay bị cái gì đâu không hà, lá lú nhìn chán chường thiệt chớ",
    "Cây mai vàng nuôi mấy năm trời tự nhiên năm nay nhìn nó ngộ lắm, lá nhìn hổng có khỏe gì hết",
    "Hổng biết thời tiết sao mà dạo này mấy chậu mai nhìn xơ xác, lá rụng đầy gốc luôn",
    "Mấy cây mai nhà em dạo này nhìn nó cứ còi cọc, lá thì đổi màu nhìn hổng ra làm sao hết",
    "Nuôi cây mai cực khổ cả năm mà giờ nhìn cái tàng lá của nó muốn bỏ cuộc ngang xương vậy đó",
    "Cây mai sau nhà dạo này bị cái chứng gì lạ lùng lắm, nhìn cái lá là thấy hổng yên tâm rồi",
    "Trời ơi nhìn chậu mai bonsai cưng dữ lắm mà nay cái lá nó bị gì nhìn thảm thương quá chừng",
    "Hổng biết bị cái gì mà lá mai cứ rụng hoài, nhìn cây mai trơ trụi thấy xót ruột quá",
    "Mấy bữa nay ra thăm vườn mai mà thấy lòng buồn rười rượi, cây cối nhìn hổng có chút sức sống nào"
]

# We need 720 symptom sentences. Let's create combinations or variations.
symptom_sentences = []

# Mix elements to create dynamic farmer style sentences
# Variation 1: Subj + spots_desc
# Variation 2: Subj + spots_desc + spread_desc
# Variation 3: Subj + spots_desc + severe_desc
# Variation 4: Subj + severe_desc + consequence_desc
# Variation 5: Subj + spread_desc + consequence_desc
# Let's write a loop that creates highly specific natural sentences.

for i in range(1000):
    s = random.choice(subjects)
    sp = random.choice(spots_desc)
    spr = random.choice(spread_desc)
    sev = random.choice(severe_desc)
    con = random.choice(consequence_desc)
    
    # Create different patterns to avoid repetition
    pattern = i % 8
    if pattern == 0:
        sent = f"{s} {sp} luôn á."
    elif pattern == 1:
        sent = f"{s} {sp}, {spr} nè."
    elif pattern == 2:
        sent = f"{s} {sp}, nhìn kỹ thì {sev} thiệt buồn."
    elif pattern == 3:
        sent = f"{s} {spr}, rồi bị nặng cái {sev} hết trơn."
    elif pattern == 4:
        sent = f"{s} bị từ lá già rồi {sev}, {con}."
    elif pattern == 5:
        sent = f"{s} tự nhiên {sp} rồi {con} luôn."
    elif pattern == 6:
        sent = f"{s} {spr}, {con} thấy thảm chưa kìa."
    else:
        sent = f"{s} bị mấy cái đốm đen quầng vàng dính lại {sev}, làm cho {con}."
        
    # Clean up multiple whitespaces or weird punctuation
    sent = sent.replace("  ", " ").replace(".,", ",").strip()
    # Add to list if unique
    if sent not in symptom_sentences:
        symptom_sentences.append(sent)
    if len(symptom_sentences) >= 720:
        break

# Generate 40 questions (expand from base)
final_questions = []
for i in range(40):
    q = questions[i % len(questions)]
    # Add a bit of variation
    suffix = random.choice([" Thiệt tình rầu quá.", " Chỉ giùm em với.", " Mong mọi người giúp đỡ.", " Đang cần gấp lắm ạ.", " Ai biết chỉ em nghen."])
    final_questions.append(f"{q}{suffix}")

# Generate 40 vague sentences (expand from base)
final_vague = []
for i in range(40):
    v = vague[i % len(vague)]
    suffix = random.choice([" Nhìn xót xa đâu đâu.", " Hổng biết tính sao luôn.", " Ai đời nuôi mai lại bị dị.", " Buồn hết sức buồn.", " Cứu cây mai sao đây trời."])
    final_vague.append(f"{v}{suffix}")

# Mix them according to requested counts
all_sentences = []
# 720 symptom
all_sentences.extend(symptom_sentences[:720])
# 40 questions
all_sentences.extend(final_questions[:40])
# 40 vague
all_sentences.extend(final_vague[:40])

# Shuffle to mix them nicely or keep structured? Let's shuffle so the distribution is natural throughout
random.shuffle(all_sentences)

# Double check total count
print(f"Total sentences: {len(all_sentences)}")

# Let's inspect a few to ensure formatting is correct
for i in range(800):
    print(f'"{all_sentences[i]}",')