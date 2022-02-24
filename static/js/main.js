// 讓點擊上一頁也能使網站重新refresh
window.onpageshow = function (event) {
    if (event.persisted) {
        window.location.reload()
    }
};