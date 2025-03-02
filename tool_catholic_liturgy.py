from datetime import datetime, timedelta
from typing import List, Dict, Optional
from langchain_core.tools import tool
import requests
import json

LITURGY_DESCRIPTION="""
# The Liturgy

# Chapter 1: Understanding Liturgy – Its Meaning, History, and Role in Christian Worship

## 1.1 What is Liturgy?

The word **liturgy** refers to the **formal and public worship of God**. It is the structured way in which believers gather to **praise, worship, and offer sacrifices** to God through prayer, Scripture, and sacred rituals. In Christian tradition, the liturgy primarily refers to the **Mass (Eucharist) and other sacraments**, as well as the **Liturgy of the Hours**.

Liturgy is not simply a personal or private act of prayer; it is a **communal and public** form of worship, where the faithful join together as the **Body of Christ** to worship God.

---

## 1.2 Etymology: The Meaning of "Liturgy"

The word **liturgy** comes from the **Greek** word **λειτουργία (leitourgia)**, which means **"public work" or "service of the people."** 

### Breakdown of the Greek Word:
- **"Leitos" (λαός, leitós)** – meaning **"public" or "of the people"**  
- **"Ergon" (ἔργον, érgon)** – meaning **"work" or "service"**

In ancient Greece, "leitourgia" referred to **a public service or duty performed for the community**, often at one's own expense. This could include funding religious festivals, financing naval expeditions, or maintaining city infrastructure.

The early **Christian Church adopted this term** to describe the **worship and sacramental life** of the community, emphasizing that liturgy is an act of service to God and a communal work of worship.

---

## 1.3 The History of Liturgy

### 1.3.1 Liturgy in the Old Testament
Liturgy has its roots in **Jewish worship**. In the Old Testament, God commanded the Israelites to worship Him through:
- **Temple sacrifices** (Exodus 29:38-46)
- **Sung Psalms and prayers** (Book of Psalms)
- **Feast days and rituals** (Leviticus 23)

Priests played a central role in **offering sacrifices**, while the people participated through **prayers, songs, and festivals**.

### 1.3.2 The Liturgy of the Early Church
After Christ's Resurrection, the first Christians continued to gather for **prayer, the reading of Scriptures, and the breaking of bread (Eucharist)**, as seen in **Acts 2:42**:

> "They devoted themselves to the apostles’ teaching and fellowship, to the breaking of bread and the prayers."

The **Eucharistic celebration** (Mass) became the central act of Christian worship, replacing the Old Testament sacrifices with the **Sacrifice of Christ on the Cross**, which is made present at every Mass.

### 1.3.3 Development of Christian Liturgy
As Christianity spread, the liturgy developed into **structured forms**, influenced by Jewish traditions and apostolic practices. Different liturgical traditions emerged in various regions:

- **Roman Rite** (Western Church, Latin-based)
- **Byzantine Rite** (Eastern Orthodox and Eastern Catholic Churches)
- **Coptic, Syriac, and other Eastern Rites** 

The **Council of Trent (1545–1563)** standardized the **Roman Rite** into the **Tridentine Mass**, which remained in use until the reforms of **Vatican II (1962–1965)**, which introduced the **Novus Ordo (New Mass)** in the vernacular.

---

## 1.4 How Liturgy Fits in Christian Worship

### 1.4.1 Liturgy as the Worship of God
Christian liturgy is not a human invention—it is a response to God’s command to **worship Him**. Jesus Himself participated in liturgical worship (Luke 4:16) and instituted the Eucharist as a **new covenantal liturgy** (Luke 22:19-20).

### 1.4.2 The Two Central Liturgies in Catholic Tradition
There are two main forms of liturgy in the Catholic Church:

1. **The Eucharistic Liturgy (The Mass)**
   - The Mass is the highest form of worship, where Catholics celebrate the **Sacrifice of Christ** and receive His **Body and Blood**.
   - The Mass is structured in **two main parts**:
     - **Liturgy of the Word** (Readings, Gospel, Homily, Prayers)
     - **Liturgy of the Eucharist** (Consecration, Communion)

2. **The Liturgy of the Hours (Divine Office)**
   - A daily cycle of prayers prayed by priests, monks, and laypeople.
   - Sanctifies the entire day with Scripture, Psalms, and hymns.

### 1.4.3 The Role of Liturgy in the Christian Life
Liturgy is not just a **routine or ritual**; it is the heart of Christian worship. It serves three main purposes:

- **Glorification of God** – Worshipping God as He deserves.
- **Sanctification of the People** – Transforming the faithful through prayer and sacraments.
- **Participation in Christ’s Sacrifice** – Entering into the mystery of Christ’s life, death, and resurrection.

### 1.4.4 Active Participation in Liturgy
Vatican II emphasized that the faithful should **actively participate** in the liturgy, meaning:
- Responding in prayers and songs.
- Listening attentively to the Word of God.
- Receiving the Eucharist with devotion.
- Living out the liturgy in daily life through faith and works.

---

## 1.5 Conclusion

- **Liturgy means "public work" or "service"** and refers to the Church’s communal worship.
- It has **Jewish roots** and was transformed by Christ into the **New Covenant liturgy**.
- The **Mass and the Liturgy of the Hours** are the two main liturgical prayers in the Church.
- The liturgy is the **central act of Christian worship**, uniting believers with God and with each other.

> *“For where two or three gather in my name, there am I with them.”* – Matthew 18:20

Liturgy is **not just a ceremony**—it is the **life of the Church**, drawing believers deeper into the mystery of Christ.

---

## Liturgical Seasons

### Advent
- **Begins**: Four Sundays before Christmas  
- **Ends**: On Christmas  
- **Liturgical Color**: Purple (except on *Gaudete Sunday* (3rd Sunday of Advent), when it is rose)  
- **Significance**: Marks the beginning of a new liturgical year  

### Christmas
- **Begins**: On Christmas Day  
- **Ends**: On the Feast of the Baptism of Jesus  
- **Liturgical Color**: White  
- **Feast of the Baptism of Jesus**:  
  - Celebrated on the first Sunday after January 6  
  - If Epiphany falls on Sunday, January 7 or January 8, the feast is moved to Monday, January 8 or January 9  

### Lent
- **Begins**: Ash Wednesday  
- **Ends**: Holy Saturday  
- **Liturgical Color**: Purple (except on special days)  
  - *Laetare Sunday* (4th Sunday of Lent) → Rose  
  - *Palm Sunday* and *Good Friday* → Red  

### Easter
- **Most important liturgical season**  
- **Begins**: Easter Sunday  
- **Ends**: Pentecost  
- **Liturgical Color**: White (except on Pentecost, when it is red)  
- **Pentecost**: Marks the birthday of the Church  

### Ordinary Time
- **Occurs**:  
  - From Christmas to Lent  
  - From Pentecost to Advent  
- **Liturgical Color**: Green  

---

## Liturgical Cycles

### Sunday Cycles
There are three Sunday cycles, which determine the Bible readings for Sunday Masses:
- **Cycle A**  
- **Cycle B**  
- **Cycle C**  

### Weekday Cycles
There are two weekday cycles, which determine the Bible readings for weekday Masses:
- **Cycle I**  
- **Cycle II**  

> **Note:** The weekday cycle does not apply during Advent, Christmas, Lent, or Easter, as these readings remain the same each year.

---

## Liturgy of the Hours

The *Liturgy of the Hours* is divided into four volumes:

| Volume | Liturgical Season |
|--------|------------------|
| **I**  | Advent and Christmas |
| **II** | Lent, Triduum, and Easter |
| **III** | Ordinary Time (Weeks 1–17) |
| **IV** | Ordinary Time (Weeks 18–34) |

---

## Rosary Series

There are four sets of *Rosary Mysteries*, each prayed on different days of the week, depending on the Liturgical Season:

- **Glorious Mysteries**
- **Joyful Mysteries**
- **Luminous Mysteries**
- **Sorrowful Mysteries**

### Rosary Schedule by Season

| Day       | **Ordinary Time, Easter** | **Advent, Christmas** | **Lent** |
|-----------|--------------------------|----------------------|----------|
| **Sunday** | Glorious | Joyful | Sorrowful |
| **Monday** | Joyful | Joyful | Joyful |
| **Tuesday** | Sorrowful | Sorrowful | Sorrowful |
| **Wednesday** | Glorious | Glorious | Glorious |
| **Thursday** | Luminous | Luminous | Luminous |
| **Friday** | Sorrowful | Sorrowful | Sorrowful |
| **Saturday** | Joyful | Joyful | Joyful |

# Understanding the Roman Catholic Liturgy

The Roman Catholic Church follows a structured system for worship and prayer throughout the year. This structure is called the **liturgical year**, and it helps guide believers through key events in the life of Jesus Christ. This document explains the liturgical year, the cycles of readings, and the Liturgy of the Hours.

---

## Chapter 1: What is the Liturgical Year?

### Overview
The **liturgical year** is the Church's way of marking time, following the life of Christ from His birth to His resurrection and beyond. It consists of different **seasons**, each with its own meaning, prayers, and readings.

### The Main Liturgical Seasons
The liturgical year is divided into these main seasons:

1. **Advent** (Preparation for the birth of Christ)
2. **Christmas** (Celebrating Christ's birth)
3. **Lent** (A time of penance and preparation for Easter)
4. **Easter** (Celebrating Christ’s Resurrection)
5. **Ordinary Time** (Focusing on the teachings and ministry of Jesus)

Each season has **specific colors**, prayers, and traditions that reflect its meaning.

---

## Chapter 2: What are Liturgical Cycles?

The Church follows a cycle of Scripture readings, ensuring that Catholics hear a broad selection of the Bible over time. These cycles determine which passages are read during Mass.

### Two Types of Cycles:
1. **Sunday Cycle** (Three-Year Cycle: A, B, and C)
2. **Weekday Cycle** (Two-Year Cycle: I and II)

These cycles are used in Mass to determine which readings from the Old Testament, Psalms, Epistles (New Testament letters), and Gospels are proclaimed.

---

## Chapter 3: The Three-Year Sunday Cycle (A, B, C)

The **Sunday Cycle** is divided into **three years** (A, B, and C), with each year focusing on a different Gospel:

- **Year A** → Gospel of Matthew  
- **Year B** → Gospel of Mark (with some readings from John)  
- **Year C** → Gospel of Luke  

> **John's Gospel** is read during special liturgical seasons like Easter and Advent, regardless of the year.

Each cycle starts on the **First Sunday of Advent** and continues until the following Advent.

| Cycle | Gospel Focus | Year Examples |
|-------|-------------|--------------|
| **A** | Matthew | 2022, 2025, 2028 |
| **B** | Mark (+ John) | 2023, 2026, 2029 |
| **C** | Luke | 2024, 2027, 2030 |

> Example: If we are in **Year A**, most Gospel readings will come from Matthew.

---

## Chapter 4: The Two-Year Weekday Cycle (I and II)

The **Weekday Cycle** covers **daily Mass readings** (Monday–Saturday) and runs in a **two-year pattern**:

- **Cycle I** → Odd-numbered years (e.g., 2023, 2025)
- **Cycle II** → Even-numbered years (e.g., 2024, 2026)

Unlike Sundays, where the Gospel readings depend on the three-year cycle, **weekday Gospel readings remain the same every year**. However, the **first readings (Old Testament & New Testament letters)** change according to Cycle I or II.

| Cycle | Applies to | Year Examples |
|-------|-----------|--------------|
| **I** | Odd years | 2023, 2025, 2027 |
| **II** | Even years | 2024, 2026, 2028 |

> Example: If the current year is **2024**, the Church follows **Cycle II** for weekday Mass readings.

---

## Chapter 5: What is the Liturgy of the Hours?

The **Liturgy of the Hours** (also called the **Divine Office**) is the Church’s daily prayer cycle. It is prayed by priests, religious communities, and laypeople to sanctify the day with prayer.

### Structure of the Liturgy of the Hours
The day is divided into different prayer times, including:

1. **Morning Prayer (Lauds)**
2. **Daytime Prayer (Mid-Morning, Midday, or Mid-Afternoon)**
3. **Evening Prayer (Vespers)**
4. **Night Prayer (Compline)**
5. **Office of Readings** (A longer meditation with Psalms and readings)

The prayers include **Psalms, hymns, Scripture readings, and petitions**.

### The Four Volumes of the Liturgy of the Hours
The prayers for the Liturgy of the Hours are contained in **four books**, which change depending on the liturgical season:

| Volume | Covers |
|--------|------------------------|
| **I** | Advent & Christmas |
| **II** | Lent, Triduum & Easter |
| **III** | Ordinary Time (Weeks 1–17) |
| **IV** | Ordinary Time (Weeks 18–34) |

> Example: If it is **Lent**, you would use **Volume II**.

---

## Chapter 6: Summary

- The **liturgical year** follows Christ’s life and is divided into seasons (Advent, Christmas, Lent, Easter, and Ordinary Time).
- **Sunday Mass readings** follow a **three-year cycle (A, B, C)**:
  - **A → Matthew**, **B → Mark**, **C → Luke**.
- **Weekday Mass readings** follow a **two-year cycle (I and II)**:
  - **I → Odd years**, **II → Even years**.
- The **Liturgy of the Hours** is the daily prayer of the Church, divided into **four volumes** based on the liturgical season.

This system ensures that over time, Catholics are exposed to a rich selection of **Scripture, prayers, and traditions**, helping them grow spiritually throughout the year.
"""

SUMMARY_OF_OLD_TESTAMENT="""
# The Old Testament in the Roman Catholic Church

## 1. Introduction

The **Old Testament** is the first part of the **Holy Bible**, containing the sacred writings of the Jewish people, which were later recognized by the Christian Church. It tells the story of **God’s creation, covenant, laws, and the history of Israel** before the coming of Jesus Christ.

The **Catholic Old Testament contains 46 books**, divided into different sections:
1. **The Pentateuch (Torah)**
2. **The Historical Books**
3. **The Wisdom Books**
4. **The Prophetic Books**

> **Note:** The Catholic Old Testament includes **seven deuterocanonical books** (Tobit, Judith, Wisdom, Sirach, Baruch, 1 & 2 Maccabees), which are not included in Protestant Bibles.

---

## 2. Overview of the Old Testament

### Structure of the Old Testament

| Section | Books Included | Key Themes |
|---------|--------------|------------|
| **Pentateuch (Torah)** | Genesis, Exodus, Leviticus, Numbers, Deuteronomy | Creation, the Law, Covenant with Israel |
| **Historical Books** | Joshua, Judges, Ruth, 1 & 2 Samuel, 1 & 2 Kings, 1 & 2 Chronicles, Ezra, Nehemiah, Tobit, Judith, Esther, 1 & 2 Maccabees | Israel’s history, conquest, exile, and restoration |
| **Wisdom Books** | Job, Psalms, Proverbs, Ecclesiastes, Song of Songs, Wisdom, Sirach | Poetry, wisdom, reflections on life and suffering |
| **Prophetic Books** | Isaiah, Jeremiah, Lamentations, Baruch, Ezekiel, Daniel, Hosea, Joel, Amos, Obadiah, Jonah, Micah, Nahum, Habakkuk, Zephaniah, Haggai, Zechariah, Malachi | God’s messages through prophets, call to repentance, prophecies of the Messiah |

---

## 3. Writers of the Old Testament

The books of the Old Testament were written over a span of **more than 1,000 years**, by various authors, including:
- **Moses** (Traditionally credited with writing the Pentateuch)
- **Prophets** (Isaiah, Jeremiah, Ezekiel, Daniel, and others)
- **Kings and Leaders** (David, Solomon, Ezra, Nehemiah)
- **Unknown scribes and authors** (Psalms, Proverbs, Ecclesiastes)

The writings were originally in **Hebrew, Aramaic, and Greek (Septuagint version)**.

---

## 4. Summary of the Books of the Old Testament

### **4.1 The Pentateuch (Torah) – The Law of Moses**
The first five books, also known as the **Torah**, lay the foundation of Jewish and Christian beliefs.

| Book | Summary |
|------|---------|
| **Genesis** | Creation, Adam and Eve, Noah’s flood, Abraham’s covenant, Joseph in Egypt. |
| **Exodus** | Moses, the Ten Plagues, Israel’s escape from Egypt, the Ten Commandments. |
| **Leviticus** | Laws for worship, purity, and holiness. |
| **Numbers** | Israel’s journey in the wilderness. |
| **Deuteronomy** | Moses’ final speeches, the Law restated before entering the Promised Land. |

---

### **4.2 The Historical Books – The History of Israel**
These books recount Israel’s history from **conquest to exile and restoration**.

| Book | Summary |
|------|---------|
| **Joshua** | Conquest of the Promised Land. |
| **Judges** | The cycle of Israel’s faithfulness and sin under various judges. |
| **Ruth** | Story of faithfulness and redemption. |
| **1 & 2 Samuel** | Rise of King Saul and King David. |
| **1 & 2 Kings** | Kingdoms of Israel and Judah, prophets Elijah and Elisha. |
| **1 & 2 Chronicles** | Retelling of Samuel and Kings with focus on the Temple. |
| **Ezra & Nehemiah** | Return from exile, rebuilding of the Temple and Jerusalem. |
| **Tobit, Judith, Esther** | Stories of faith and deliverance in foreign lands. |
| **1 & 2 Maccabees** | Jewish revolts against Greek rulers. |

---

### **4.3 The Wisdom Books – Reflections on Life and Worship**
These books contain **poetry, prayers, wisdom, and philosophical reflections**.

| Book | Summary |
|------|---------|
| **Job** | The problem of suffering and God’s justice. |
| **Psalms** | Hymns and prayers of worship. |
| **Proverbs** | Wise sayings for life and faith. |
| **Ecclesiastes** | The meaning of life and human limitations. |
| **Song of Songs** | Love poem, symbolic of God’s love for His people. |
| **Wisdom** | The pursuit of wisdom and righteousness. |
| **Sirach (Ecclesiasticus)** | Practical wisdom for living a holy life. |

---

### **4.4 The Prophetic Books – God’s Call to His People**
These books contain **prophecies, warnings, and promises of salvation**.

| Book | Key Themes |
|------|------------|
| **Isaiah** | Messianic prophecies, call to repentance. |
| **Jeremiah** | Warning of exile, hope for a new covenant. |
| **Lamentations** | Mourning the destruction of Jerusalem. |
| **Baruch** | Encouragement during exile. |
| **Ezekiel** | Visions of restoration and a new Temple. |
| **Daniel** | Apocalyptic visions and God’s sovereignty. |
| **Hosea - Malachi** | Warnings, hope, and coming of the Messiah. |

---

## 5. Timeline of the Old Testament Books

The Old Testament was written over a period of **1,500 years** (c. **1400 BC – 400 BC**).

| Period | Books Written |
|--------|--------------|
| **1400–1200 BC** | Genesis, Exodus, Leviticus, Numbers, Deuteronomy |
| **1200–1000 BC** | Joshua, Judges, Ruth, Job |
| **1000–900 BC** | 1 & 2 Samuel, Psalms, Proverbs, Song of Songs |
| **900–700 BC** | Isaiah, 1 & 2 Kings, 1 & 2 Chronicles, Ecclesiastes |
| **700–500 BC** | Jeremiah, Lamentations, Ezekiel, Daniel, Minor Prophets |
| **500–400 BC** | Ezra, Nehemiah, Wisdom, Sirach, Baruch, 1 & 2 Maccabees |

> The **Pentateuch (Torah)** is traditionally attributed to Moses (~1400 BC), while the **last books** (Malachi, 2 Maccabees) were written around 400 BC.

---

## 6. Historical Context

The Old Testament was written during:
1. **The Patriarchal Period (2000–1500 BC)** – Abraham, Isaac, Jacob.
2. **The Exodus & Wilderness (1400–1200 BC)** – Moses and the giving of the Law.
3. **The Kingdoms of Israel & Judah (1000–586 BC)** – David, Solomon, divided kingdom.
4. **The Babylonian Exile (586–539 BC)** – Destruction of Jerusalem, captivity.
5. **The Return & Second Temple Period (539–400 BC)** – Rebuilding Jerusalem and awaiting the Messiah.

The Old Testament was **translated into Greek** (the **Septuagint**) around **250 BC**, which became the basis for Catholic Scriptures.

---

## 7. Summary

- The **Catholic Old Testament** contains **46 books**, divided into **four sections**.
- It covers **creation, Israel’s history, wisdom teachings, and prophetic messages**.
- The **deuterocanonical books** are included in Catholic Bibles but not in Protestant ones.
- The Old Testament **prepares for Jesus Christ**, with **prophecies fulfilled in the New Testament**.

> **“All Scripture is inspired by God.” – 2 Timothy 3:16**
"""

SUMMARY_OF_NEW_TESTAMENT="""
# The New Testament in the Roman Catholic Church

## 1. Introduction

The **New Testament** is the second part of the **Holy Bible**, focusing on the life, teachings, death, and resurrection of **Jesus Christ**, as well as the early Christian Church. It is **sacred Scripture** for all Christians, with the **Catholic Church recognizing 27 books** as canonical.

These books contain:
- **The life and mission of Jesus Christ**
- **Teachings and parables of Jesus**
- **The establishment of the Church**
- **Theological letters and prophecies about the end times**

---

## 2. Overview of the New Testament

### Structure
The New Testament is divided into **four main sections**:

1. **The Gospels** (Matthew, Mark, Luke, John)  
   - The life, death, and resurrection of Jesus.
2. **The Acts of the Apostles**  
   - The history of the early Church after Jesus’ resurrection.
3. **The Epistles (Letters)**  
   - Letters written by St. Paul and other Apostles to guide early Christian communities.
4. **The Book of Revelation**  
   - A prophetic book about the end times, written by St. John.

---

## 3. Writers of the New Testament

The New Testament was written by **apostles and early disciples** of Jesus, inspired by the Holy Spirit.

| Book | Traditional Author |
|------|--------------------|
| **Matthew** | St. Matthew (Apostle) |
| **Mark** | St. Mark (Disciple of Peter) |
| **Luke** | St. Luke (Companion of Paul) |
| **John** | St. John (Apostle) |
| **Acts of the Apostles** | St. Luke |
| **Romans - Philemon** | St. Paul (Epistles) |
| **Hebrews** | Anonymous (Traditionally attributed to Paul) |
| **James** | St. James (Brother of the Lord) |
| **1 & 2 Peter** | St. Peter (Apostle) |
| **1, 2, & 3 John** | St. John (Apostle) |
| **Jude** | St. Jude (Apostle) |
| **Revelation** | St. John (Apostle) |

> **Note:** The Gospel of Mark is believed to be based on the teachings of **St. Peter**.

---

## 4. Summary of the Books of the New Testament

### **4.1 The Gospels**
The **four Gospels** tell the **life, ministry, death, and resurrection of Jesus**.

| Gospel | Key Themes |
|--------|-----------|
| **Matthew** | Jesus as the Messiah; fulfillment of Old Testament prophecies. |
| **Mark** | Jesus as the suffering servant; fast-paced and action-driven. |
| **Luke** | Jesus as the compassionate Savior; focus on the poor and outcasts. |
| **John** | Jesus as the divine Son of God; theological depth and spiritual meaning. |

### **4.2 The Acts of the Apostles**
- Written by **St. Luke**.
- Describes the **early Church**, the **coming of the Holy Spirit at Pentecost**, and **Paul’s missionary journeys**.

### **4.3 The Epistles (Letters)**
- **Pauline Epistles** (Letters written by St. Paul)  
- **Catholic Epistles** (Letters written by other apostles)

| Letter | Audience | Theme |
|--------|---------|-------|
| **Romans** | Christians in Rome | Justification by faith. |
| **1 & 2 Corinthians** | Church in Corinth | Unity, spiritual gifts, Christian morality. |
| **Galatians** | Christians in Galatia | Salvation through faith, not just the Law. |
| **Ephesians** | Christians in Ephesus | The Church as the Body of Christ. |
| **Philippians** | Church in Philippi | Joy and humility in Christ. |
| **Colossians** | Church in Colossae | Christ’s supremacy. |
| **1 & 2 Thessalonians** | Church in Thessalonica | Christ’s Second Coming. |
| **1 & 2 Timothy, Titus** | Timothy, Titus | Leadership and pastoral guidance. |
| **Philemon** | Philemon | Forgiveness and Christian brotherhood. |
| **Hebrews** | Jewish Christians | Jesus as the high priest and fulfillment of the Old Testament. |
| **James** | All Christians | Faith and works. |
| **1 & 2 Peter** | Persecuted Christians | Encouragement in suffering. |
| **1, 2, & 3 John** | Early Church | Love and truth. |
| **Jude** | The Church | Warning against false teachers. |

### **4.4 The Book of Revelation**
- Written by **St. John**.
- A prophetic book about **the final victory of Christ**, the **Second Coming**, and the **New Heaven and New Earth**.

---

## 5. Timeline of the New Testament Books

The New Testament was written between **50 AD – 100 AD**.

| Period | Books Written |
|--------|--------------|
| **50–60 AD** | 1 & 2 Thessalonians, Galatians, 1 & 2 Corinthians, Romans |
| **60–70 AD** | Philippians, Colossians, Ephesians, Philemon, Acts |
| **70–80 AD** | Gospel of Mark, Gospel of Matthew, Gospel of Luke |
| **80–90 AD** | Gospel of John, 1 & 2 Timothy, Titus, Hebrews, 1 Peter, James |
| **90–100 AD** | 1, 2, & 3 John, Jude, Revelation |

> The **Gospels** were written after most of Paul’s letters. The earliest writings are **Paul’s letters** (~50 AD).

---

## 6. Historical Context

The New Testament was written in the context of:
1. **The Roman Empire** – Christianity spread despite persecution.
2. **Jewish Traditions** – Many books reference Old Testament prophecies.
3. **Early Church Growth** – Letters were written to guide new Christian communities.

The canon of the **New Testament** was officially recognized by the **Council of Carthage (397 AD)**, affirming the **27 books** we have today.

---

## 7. Summary

- The **New Testament** contains **27 books** focused on the life of Jesus and the early Church.
- **Four Gospels** present different perspectives on Jesus.
- **Acts of the Apostles** details the Church’s early years.
- **Epistles** guide Christian doctrine and faith.
- **Revelation** gives a vision of God’s final victory.

The New Testament is central to the **faith, liturgy, and teachings of the Catholic Church**, forming the foundation of Christian belief.

> **“The word of God is living and active.” – Hebrews 4:12**
"""

from typing import Dict
import requests

def get_liturgy_for_year_and_month(year: int, month: int) -> Optional[List[Dict]]:
    url = f"http://calapi.inadiutorium.cz/api/v0/en/calendars/default/{year}/{month}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error fetching liturgy for {year}-{month}: {e}")
        return None

def get_liturgy_for_day(year: int, month: int, day_of_month: int) -> Optional[Dict]:
    url = f"http://calapi.inadiutorium.cz/api/v0/en/calendars/default/{year}/{month}/{day_of_month}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error fetching liturgy for {year}-{month}-{day_of_month}: {e}")
        return None

@tool
def get_liturgy_for_year_and_month_tool(year: int, month: int) -> str:
    """Returns the liturgy for a given year and month as JSON string"""
    return json.dumps(get_liturgy_for_year_and_month(year, month))

@tool
def get_liturgy_explanation_tool() -> str:
    """Get a full explanation of the Roman Catholic Liturgy in markdown format
       Note: Only use this tool for faith related questions
    """
    return LITURGY_DESCRIPTION

@tool
def get_summary_of_old_testament_tool() -> str:
    """Get a summary of the Old Testament in markdown format
       Note: Only use this tool for faith related questions
    """
    return SUMMARY_OF_OLD_TESTAMENT

@tool
def get_summary_of_new_testament_tool() -> str:
    """Get a summary of the New Testament in markdown format
       Note: Only use this tool for faith related questions
    """
    return SUMMARY_OF_NEW_TESTAMENT
