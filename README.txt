*******IMPORTANT*******
claim id สามารถพิมมั่วๆได้เลยแต่ห้ามขึ้นด้วย 0 และต้องเป็นตัวเลข 8 หลักเท่านั้น
ห้ามซ้ำกับ Claim ID ก่อนหน้าที่เคยพิมไป



 รันโปรแกรม:
   python main.py
 หากเปิด GUI ไม่ได้และขึ้นว่าไม่มี PySide6 ให้ติดตั้ง:
   pip install PySide6
 เวอร์ชันนี้จะล้างข้อมูลเก่าทุกครั้งที่เปิดโปรแกรมใหม่ แล้ว seed ข้อมูลเริ่มต้นอัตโนมัติ

========================================
2) ส่วนประกอบหน้าจอ
========================================
- Login
  - Role: CITIZEN / OFFICER
  - Username
  - Password
  - ปุ่ม Login / Logout
- Submit Claim (Citizen)
  - ช่อง Claim ID (8 หลัก)
  - ปุ่ม Submit + Calculate
  - ปุ่ม Go To Claim List
- Claim List
  - ปุ่ม Refresh Claims
  - ปุ่ม Go To Submit Form
  - ตาราง Claims (แสดงผลคำขอและเงินเยียวยา)

========================================
3) บัญชีทดสอบ
========================================

username/password

Citizen:
- citizen1 / 1234
- citizen2 / 1234
- citizen3 / 1234

Officer:
- officer / admin

========================================
4) วิธีใช้งานหลัก
========================================
Citizen:
1. เลือก Role = CITIZEN
2. กรอก Username/Password และกด Login
3. กรอก Claim ID เป็นตัวเลข 8 หลัก (หลักแรกห้ามเป็น 0)
4. กด Submit + Calculate
5. ระบบจะกลับไปหน้า Claim List อัตโนมัติ
6. ตรวจสอบข้อมูลในตาราง Claims

Officer:
1. เลือก Role = OFFICER
2. กรอก officer / admin และกด Login
3. กด Refresh Claims เพื่อดูรายการทั้งหมด

สิทธิ์การมองเห็นข้อมูล:
- OFFICER: เห็น Claims ทั้งหมด
- CITIZEN: เห็นเฉพาะ Claims ของตนเอง
- Logout: ตาราง Claims ต้องว่าง

========================================
5) Business Rules การคำนวณ
========================================
หมายเหตุ: สูตรคำนวณอยู่ใน Model เท่านั้น และเลือกสูตรจาก monthly_income

1. LOW: รายได้ < 6500
   - เงินเยียวยา = 6500

2. NORMAL: รายได้ตั้งแต่ 6500 ถึงน้อยกว่า 50000
   - เงินเยียวยา = รายได้ต่อเดือน แต่ไม่เกิน 20000

3. HIGH: รายได้ >= 50000
   - เงินเยียวยา = รายได้ต่อเดือน / 5 แต่ไม่เกิน 20000

หลังคำนวณ:
- บันทึกผลลงตาราง Compensations
- อัปเดตสถานะ Claim เป็น CALCULATED
- กลับมาหน้ารายการคำขอ (Claim List) อัตโนมัติ



========================================
7) SQL ตรวจผล (ใช้ตอนส่งงาน/ดีบัก)
========================================
ดูข้อมูลผู้ใช้:
SELECT username, role, claimant_id FROM Users;

ดูคำขอทั้งหมด:
SELECT claim_id, claimant_id, submitted_date, status FROM Claims ORDER BY submitted_date DESC;

ดูผลคำนวณ:
SELECT claim_id, amount, calculated_date FROM Compensations ORDER BY calculated_date DESC;

เช็ค claim ใด claim หนึ่ง:
SELECT c.claim_id, c.status, cp.amount
FROM Claims c
LEFT JOIN Compensations cp ON cp.claim_id = c.claim_id
WHERE c.claim_id = '12345678';

========================================
8) ปัญหาที่พบบ่อย
========================================
1. กด Login แล้วไม่เกิดอะไรขึ้น
- ตรวจว่าใช้ไฟล์ main.py ล่าสุด
- ปิดโปรแกรมแล้วรันใหม่ด้วย python main.py

2. Login ไม่ผ่าน
- ตรวจ username/password
- ลองบัญชีตัวอย่างตามหัวข้อ 3

3. เปิด GUI ไม่ขึ้น
- ติดตั้ง PySide6
- ตรวจ Python environment ที่ใช้งานอยู่
