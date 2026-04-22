// 全局变量
let currentUser = null;
let accessToken = localStorage.getItem('accessToken');

// API基础URL
const API_BASE = '';

// 显示提示信息
function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, duration);
}

// 获取请求头
function getHeaders() {
    const headers = {
        'Content-Type': 'application/json',
    };
    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }
    return headers;
}

// ===== 登录相关 =====

// 发送验证码
async function sendCode() {
    const email = document.getElementById('email').value.trim();

    if (!email) {
        showToast('请输入邮箱地址');
        return;
    }

    if (!validateEmail(email)) {
        showToast('请输入有效的邮箱地址');
        return;
    }

    const btn = document.getElementById('btnSendCode');
    btn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/api/auth/send-code`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email }),
        });

        const data = await response.json();

        if (data.success) {
            showToast(data.message);

            // 倒计时60秒
            let countdown = 60;
            btn.textContent = `${countdown}秒后重发`;
            const timer = setInterval(() => {
                countdown--;
                btn.textContent = `${countdown}秒后重发`;
                if (countdown <= 0) {
                    clearInterval(timer);
                    btn.disabled = false;
                    btn.textContent = '发送验证码';
                }
            }, 1000);
        } else {
            showToast(data.message || '发送失败');
            btn.disabled = false;
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('发送失败，请检查网络连接');
        btn.disabled = false;
    }
}

// 邮箱验证
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// 登录
async function login() {
    const email = document.getElementById('email').value.trim();
    const code = document.getElementById('verificationCode').value.trim();

    if (!email) {
        showToast('请输入邮箱地址');
        return;
    }

    if (!code) {
        showToast('请输入验证码');
        return;
    }

    const btn = document.querySelector('.btn-primary');
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = '登录中...';

    try {
        const response = await fetch(`${API_BASE}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, code }),
        });

        const data = await response.json();

        if (response.ok) {
            accessToken = data.access_token;
            localStorage.setItem('accessToken', accessToken);

            currentUser = data.user;

            // 切换到主界面
            showMainSection();
            showToast('登录成功！');
        } else {
            showToast(data.detail || '登录失败');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('登录失败，请检查网络连接');
    } finally {
        btn.disabled = false;
        btn.textContent = originalText;
    }
}

// 退出登录
function logout() {
    localStorage.removeItem('accessToken');
    accessToken = null;
    currentUser = null;

    document.getElementById('loginSection').style.display = 'block';
    document.getElementById('mainSection').style.display = 'none';
    showToast('已退出登录');
}

// 显示主界面
function showMainSection() {
    document.getElementById('loginSection').style.display = 'none';
    document.getElementById('mainSection').style.display = 'block';

    // 更新用户信息
    document.getElementById('userEmail').textContent = currentUser.email;

    // 加载用户数据
    loadUserData();
    loadPackages();
    loadHistory();
}

// ===== 用户数据相关 =====

// 加载用户数据
async function loadUserData() {
    try {
        const response = await fetch(`${API_BASE}/api/auth/me`, {
            headers: getHeaders(),
        });

        if (response.ok) {
            const data = await response.json();
            updateUserBalance(data);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// 更新余额显示
function updateUserBalance(data) {
    document.getElementById('remainingCount').textContent = data.remaining_count;
    document.getElementById('totalPurchased').textContent = data.total_purchased;
    document.getElementById('totalUsed').textContent = data.total_used;
}

// ===== 内容生成相关 =====

// 生成内容
async function generateContent() {
    const topic = document.getElementById('topic').value.trim();
    const needImages = document.getElementById('needImages').checked;

    if (!topic) {
        showToast('请输入主题');
        return;
    }

    const btn = document.getElementById('btnGenerateText');
    const btnElement = document.querySelector('.btn-primary');
    const originalText = btn.textContent;
    btnElement.disabled = true;
    btn.textContent = '生成中...';

    try {
        const response = await fetch(`${API_BASE}/api/content/generate`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({
                topic,
                need_images: needImages,
            }),
        });

        const data = await response.json();

        if (data.success) {
            displayResult(data.data);
            loadUserData(); // 更新余额
            loadHistory(); // 更新历史记录
            showToast('生成成功！');
        } else {
            showToast(data.message || '生成失败');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('生成失败，请检查网络连接');
    } finally {
        btnElement.disabled = false;
        btn.textContent = originalText;
    }
}

// 显示生成结果
function displayResult(data) {
    const resultSection = document.getElementById('resultSection');
    resultSection.style.display = 'block';

    // 设置标题
    document.getElementById('resultTitle').textContent = data.title;

    // 设置正文
    document.getElementById('resultBody').textContent = data.body;

    // 设置标签
    const tagsContainer = document.getElementById('resultTags');
    tagsContainer.innerHTML = data.tags.map(tag => `<span>${tag}</span>`).join('');

    // 设置图片
    const imagesContainer = document.getElementById('resultImages');
    if (data.images && data.images.length > 0) {
        imagesContainer.innerHTML = data.images.map(url =>
            `<img src="${url}" alt="生成的图片" />`
        ).join('');
    } else {
        imagesContainer.innerHTML = '';
    }

    // 滚动到结果区域
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// 复制文案
function copyContent() {
    const title = document.getElementById('resultTitle').textContent;
    const body = document.getElementById('resultBody').textContent;
    const tags = document.getElementById('resultTags').textContent;

    const fullContent = `${title}\n\n${body}\n\n${tags}`;

    navigator.clipboard.writeText(fullContent).then(() => {
        showToast('文案已复制到剪贴板！');
    }).catch(err => {
        showToast('复制失败，请手动复制');
    });
}

// ===== 套餐购买相关 =====

// 加载套餐列表
async function loadPackages() {
    try {
        const response = await fetch(`${API_BASE}/api/payment/packages`);
        const data = await response.json();

        if (data.success) {
            displayPackages(data.data);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// 显示套餐列表
function displayPackages(packages) {
    const grid = document.getElementById('packagesGrid');

    grid.innerHTML = packages.map((pkg, index) => `
        <div class="package-card ${index === 1 ? 'popular' : ''}" onclick="createOrder(${pkg.id})">
            <div class="package-name">${pkg.name}</div>
            <div class="package-count">${pkg.count}<span>次</span></div>
            <div class="package-price">¥${pkg.price}</div>
            <div class="package-unit">约 ¥${(pkg.price / pkg.count).toFixed(2)}/次</div>
            <div class="package-desc">${pkg.description || ''}</div>
            ${index === 1 ? '<div class="package-tag">热门</div>' : ''}
        </div>
    `).join('');
}

// 创建订单
async function createOrder(packageId) {
    try {
        const response = await fetch(`${API_BASE}/api/payment/create-order`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ package_id: packageId }),
        });

        const data = await response.json();

        if (data.success) {
            // 模拟支付（实际开发中需要调用微信/支付宝）
            const shouldPay = confirm(
                `订单号：${data.order_no}\n金额：¥${data.payment_params.amount}\n\n确认支付？（开发模式：点击确定模拟支付成功）`
            );

            if (shouldPay) {
                await mockPayment(data.order_no);
            }
        } else {
            showToast(data.message || '创建订单失败');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('创建订单失败');
    }
}

// 模拟支付
async function mockPayment(orderNo) {
    try {
        const response = await fetch(`${API_BASE}/api/payment/mock-pay/${orderNo}`);
        const data = await response.json();

        if (data.success) {
            showToast('支付成功！');
            loadUserData(); // 更新余额
        } else {
            showToast(data.message || '支付失败');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('支付失败');
    }
}

// ===== 历史记录相关 =====

// 加载历史记录
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/api/content/history`, {
            headers: getHeaders(),
        });

        const data = await response.json();

        if (data.success) {
            displayHistory(data.data);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// 显示历史记录
function displayHistory(logs) {
    const list = document.getElementById('historyList');

    if (logs.length === 0) {
        list.innerHTML = '<p style="text-align: center; color: #999;">暂无使用记录</p>';
        return;
    }

    list.innerHTML = logs.map(log => `
        <div class="history-item">
            <div class="history-topic">${log.topic} ${log.need_images ? '🖼️' : ''}</div>
            <div class="history-time">${new Date(log.created_at).toLocaleString('zh-CN')}</div>
        </div>
    `).join('');
}

// ===== 初始化 =====

// 页面加载时检查登录状态
window.addEventListener('load', () => {
    if (accessToken) {
        // 自动登录检查
        fetch(`${API_BASE}/api/auth/me`, {
            headers: getHeaders(),
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Token invalid');
            })
            .then(data => {
                currentUser = data;
                showMainSection();
            })
            .catch(() => {
                localStorage.removeItem('accessToken');
                accessToken = null;
            });
    }
});
