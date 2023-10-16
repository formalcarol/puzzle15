NTOU CSE Class AI Lab2  
Source: [Book] Artificial Intelligence: A Modern Approach  

這是一個15-puzzle的問題，本案有4*4的拼圖，總共有16格，並給予1~15的數值，隨機分布在16格中，則會有1個為空格  
通過拼圖間的交換，我們希望最後結果可以按照順序排列(如圖)  
![Alt text](puzzle.jpg)

本案採3種不同的策略滑動拼圖塊  
1. BFS演算法 暴力搜尋 且 橫向優先  
2. A*演算法+h1啟發函式 min(sum(每個元素不在其正確位置的個數))為優先  
3. A*演算法+h2啟發函式 min(sum(每個元素距離其正確位置的格數))為優先  