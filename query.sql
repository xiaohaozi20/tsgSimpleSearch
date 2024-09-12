WITH RandomizedData AS (
    SELECT A.索书号,
           B.登录号,
           A.题名2 AS 题名,
           A.责任者2 AS 责任者,
           A.题名 AS 出版者,
           A.标准编码,
           B.批次号,
           D.部门名称,
           ROW_NUMBER() OVER (PARTITION BY D.部门名称 ORDER BY DBMS_RANDOM.VALUE) AS rn
    FROM 馆藏书目库 A
    INNER JOIN 馆藏典藏库 C ON A.主键码 = C.主键码
    INNER JOIN 采购库 B ON A.主键码 = B.主键码
    INNER JOIN 馆藏地址定义 D ON C.馆藏地址 = D.馆藏地址
    WHERE B.库键码 = 1 
      AND B.主键码 > 0 
      AND B.状态 = 'G'
      AND (
          D.部门名称 LIKE '%二楼%'
          OR D.部门名称 LIKE '%一楼%'
          OR D.部门名称 LIKE '%三楼%'
          OR D.部门名称 LIKE '%旧书%'
          OR D.部门名称 LIKE '%基藏书库%'
      )
)
SELECT *
FROM RandomizedData
WHERE rn <= 2
ORDER BY 部门名称, rn