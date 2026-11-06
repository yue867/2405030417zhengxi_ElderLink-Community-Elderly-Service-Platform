/* ============================================================
   颐邻通 V1.0 - 前端 API 调用封装
   API_BASE 统一指向 FastAPI 后端（一体化服务，同源即可）
   ============================================================ */

const API_BASE = "";  // 同源部署，直接空字符串；若前后端分离则填 "http://localhost:8000"

/**
 * 通用 fetch 封装：自动处理 JSON、错误抛异常
 */
async function request(url, options = {}) {
    const res = await fetch(API_BASE + url, {
        headers: { "Content-Type": "application/json", ...options.headers },
        ...options,
    });
    const data = await res.json();
    if (!res.ok) {
        // 后端 HTTPException 会返回 {"detail": "..."}
        throw new Error(data.detail || data.msg || `请求失败 (${res.status})`);
    }
    return data;
}

// ---------- 登录 ----------
function apiLogin(account, password) {
    return request("/api/login", {
        method: "POST",
        body: JSON.stringify({ account, password }),
    });
}

// ---------- 工单 ----------
function apiListOrders() {
    return request("/api/orders");
}

function apiCreateOrder(elder_name, content, submitter_id = 1) {
    return request("/api/orders", {
        method: "POST",
        body: JSON.stringify({ elder_name, content, submitter_id }),
    });
}

function apiCancelOrder(id) {
    return request(`/api/orders/${id}/cancel`, { method: "PUT" });
}

function apiAssignOrder(id) {
    return request(`/api/orders/${id}/assign`, { method: "PUT" });
}

function apiReviewOrder(id, review_result, reply_content = "") {
    return request(`/api/orders/${id}/review`, {
        method: "PUT",
        body: JSON.stringify({ review_result, reply_content }),
    });
}

// ---------- 工具 ----------
function showMsg(elId, text, type) {
    const el = document.getElementById(elId);
    if (!el) return;
    el.textContent = text;
    el.className = "msg " + type;
    setTimeout(() => { el.textContent = ""; el.className = "msg"; }, 3000);
}

function statusTag(status) {
    return `<span class="status-tag status-${status}">${status}</span>`;
}
