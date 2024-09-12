WITH RandomizedData AS (
    SELECT A.�����,
           B.��¼��,
           A.����2 AS ����,
           A.������2 AS ������,
           A.���� AS ������,
           A.��׼����,
           B.���κ�,
           D.��������,
           ROW_NUMBER() OVER (PARTITION BY D.�������� ORDER BY DBMS_RANDOM.VALUE) AS rn
    FROM �ݲ���Ŀ�� A
    INNER JOIN �ݲص�ؿ� C ON A.������ = C.������
    INNER JOIN �ɹ��� B ON A.������ = B.������
    INNER JOIN �ݲص�ַ���� D ON C.�ݲص�ַ = D.�ݲص�ַ
    WHERE B.����� = 1 
      AND B.������ > 0 
      AND B.״̬ = 'G'
      AND (
          D.�������� LIKE '%��¥%'
          OR D.�������� LIKE '%һ¥%'
          OR D.�������� LIKE '%��¥%'
          OR D.�������� LIKE '%����%'
          OR D.�������� LIKE '%�������%'
      )
)
SELECT *
FROM RandomizedData
WHERE rn <= 2
ORDER BY ��������, rn