# tour_bus_django

20220719
1.App 端要做一個確認刪除的 dialog
2.App 端要呼叫 delete url (用 Get 寫的, 不知為何 delete 在 postman 不能用?)

20220718
ok 1.關聯有 Order, TourBus, AnnounceMent(公告), 次關聯 PayInfo(跟 Order 相關)
ok 2.如果 User 刪除, 將關聯欄位設為 SET_NULL

a.將 Order, TourBus 的表單加入 name, phone, company 
(先確認有哪些資料必要留下? 都不留也可以, 相關地方都顯示 "此用戶已刪除")
=> 要顯示"此用戶已刪除"

ok b.TourBus 如果用戶刪除, 則"下架所有車輛", 並刪除所有"可接單時間"~
ok c.如果刪除時, 還有訂單未執行, 則取消所有訂單~

3.檢查 AnnounceMent 跟 PayInfo 會不會有影響
=> 好像是不用~

ok 4.檢查 App 跟 後台影響到的相關頁面, 承 2.a 執行~
5.App 要多一個 "退出並刪除資料" 的按鈕, 並做一個相應的 api

看 2.a 要留下哪些資料, 3 個欄位內 => 14,000 
=> 如果多了, 再看是哪些欄位~

如果都不留資料(全部顯示"此用戶已刪除") => 8,000

執行天數預計是 4 天, 會變更資料庫跟檢測,
如果第 4 點有漏網情況, 日後不加價協助修復.
