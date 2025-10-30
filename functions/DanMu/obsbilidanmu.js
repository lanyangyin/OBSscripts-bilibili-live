// 付费消息
const tickerContainer = document.querySelector('.style-scope.yt-live-chat-ticker-renderer#items');
// 弹幕消息
const itemContainer = document.querySelector('.style-scope.yt-live-chat-item-list-renderer#items');
// 可滚动容器
const scrollableContainer = document.querySelector('.style-scope.yt-live-chat-item-list-renderer.animated#item-scroller'); // 或其他选择器

// 付费消息类
class PaidMessageTicker {
    constructor(options = {}) {
        this.config = {
            // 基础配置
            width: '106px',
            text: 'CN¥39.00',
            avatarSrc: './blivechat_files/noface.gif',

            // 颜色配置
            primaryColor: 'rgb(29, 233, 182)',
            secondaryColor: 'rgb(0, 191, 165)',

            // 倒计时配置
            initialPercentage: 100,
            countdownDuration: 10000, // 毫秒
            countdownInterval: 50, // 更新间隔（毫秒）

            // 回调函数
            onRemove: null, // 删除回调，参数是实例
            onUpdate: null, // 倒计时进度条更新回调, 第一个参数是剩余百分比，第二个是实例

            ...options
        };

        this.currentPercentage = this.config.initialPercentage;
        this.countdownInterval = null;
        this.startTime = null;
        this.element = null;

        this.init();
    }

    init() {
        this.createElement();
        this.startCountdown();
    }

    createElement() {
        this.element = document.createElement('yt-live-chat-ticker-paid-message-item-renderer');
        this.element.className = 'style-scope yt-live-chat-ticker-renderer';
        this.element.style.overflow = 'hidden';
        this.element.style.width = this.config.width;
        this.element.tabIndex = 0;

        this.updateElement();
    }

    updateElement() {
        const gradientStyle = `linear-gradient(90deg, ${this.config.primaryColor}, ${this.config.primaryColor} ${this.currentPercentage}%, ${this.config.secondaryColor} ${this.currentPercentage}%, ${this.config.secondaryColor})`;

        this.element.innerHTML = `
            <div class="style-scope yt-live-chat-ticker-paid-message-item-renderer" dir="ltr" id="container"
                 style="background: ${gradientStyle};">
                <div class="style-scope yt-live-chat-ticker-paid-message-item-renderer" id="content"
                     style="color: ${this.getTextColor()};">
                    <yt-img-shadow class="no-transition style-scope yt-live-chat-ticker-paid-message-item-renderer"
                                  height="24" id="author-photo" loaded=""
                                  style="background-color: transparent;" width="24">
                        <img alt="" class="style-scope yt-img-shadow" height="24" id="img"
                             src="${this.config.avatarSrc}" width="24">
                    </yt-img-shadow>
                    <span class="style-scope yt-live-chat-ticker-paid-message-item-renderer" dir="ltr"
                          id="text">${this.config.text}</span>
                </div>
            </div>
        `;
    }

    getTextColor() {
        // 根据背景颜色亮度自动选择合适的文字颜色
        const primaryColor = this.config.primaryColor;
        const rgbMatch = primaryColor.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);

        if (rgbMatch) {
            const r = parseInt(rgbMatch[1]);
            const g = parseInt(rgbMatch[2]);
            const b = parseInt(rgbMatch[3]);

            // 计算亮度 (使用相对亮度公式)
            const brightness = (r * 0.299 + g * 0.587 + b * 0.114) / 255;

            return brightness > 0.5 ? 'rgb(0, 0, 0)' : 'rgb(255, 255, 255)';
        }

        return 'rgb(255, 255, 255)'; // 默认白色
    }

    startCountdown() {
        this.startTime = Date.now();

        this.countdownInterval = setInterval(() => {
            const elapsed = Date.now() - this.startTime;
            const progress = elapsed / this.config.countdownDuration;

            this.currentPercentage = Math.max(1, this.config.initialPercentage - (progress * (this.config.initialPercentage - 1)));

            this.updateElement();

            // 触发更新回调
            if (this.config.onUpdate) {
                this.config.onUpdate(this.currentPercentage, this);
            }

            // 检查是否应该删除
            if (this.currentPercentage <= 1) {
                this.remove();
            }
        }, this.config.countdownInterval);
    }

    remove() {
        if (this.countdownInterval) {
            clearInterval(this.countdownInterval);
            this.countdownInterval = null;
        }

        if (this.element && this.element.parentNode) {
            this.element.parentNode.removeChild(this.element);
        }

        // 触发删除回调
        if (this.config.onRemove) {
            this.config.onRemove(this);
        }
    }

    // 手动更新百分比
    setPercentage(percentage) {
        this.currentPercentage = Math.max(1, Math.min(100, percentage));
        this.updateElement();
    }

    // 获取DOM元素
    getElement() {
        return this.element;
    }

    // 销毁实例
    destroy() {
        this.remove();
    }
}

// 管理器类，用于管理多个付费消息
class PaidMessageTickerManager {
    constructor() {
        this.tickers = new Set();
    }


    createTicker(options) {
        const ticker = new PaidMessageTicker({
            ...options,
            onRemove: (removedTicker) => {
                this.tickers.delete(removedTicker);
                if (options.onRemove) {
                    options.onRemove(removedTicker);
                }
            }
        });

        this.tickers.add(ticker);

        return ticker;
    }

    removeAll() {
        this.tickers.forEach(ticker => ticker.destroy());
        this.tickers.clear();
    }

    getCount() {
        return this.tickers.size;
    }
}

// 使用示例
const manager = new PaidMessageTickerManager();

// 创建不同类型的付费消息
const smallAmount = manager.createTicker({
    width: '106px',
    primaryColor: 'rgb(29, 233, 182)',
    secondaryColor: 'rgb(0, 191, 165)',
    text: 'CN¥39.00',
    avatarSrc: './blivechat_files/noface.gif',
    countdownDuration: 8000, // 8秒
//    onUpdate: (percentage, ticker) => {
//        console.log(`当前百分比: ${percentage}%`);
//    },
//    onRemove: (ticker) => {
//        console.log('小金额消息已移除');
//    }
});

// 创建不同类型的付费消息
const smallAmount1 = manager.createTicker({
    width: '106px',
    primaryColor: 'rgb(29, 233, 182)',
    secondaryColor: 'rgb(0, 191, 165)',
    text: 'CN¥39.00',
    avatarSrc: './blivechat_files/noface.gif',
    countdownDuration: 8000, // 8秒
//    onUpdate: (percentage, ticker) => {
//        console.log(`当前百分比: ${percentage}%`);
//    },
//    onRemove: (ticker) => {
//        console.log('小金额消息已移除');
//    }
});

// 添加到页面
tickerContainer.appendChild(smallAmount.getElement());
// 添加到页面
tickerContainer.appendChild(smallAmount1.getElement());






class YouTubeChatMessageBuilder {
    constructor() {
        this.TextMessages = new Set();
        this.PaidMessages = new Set();
        this.MembershipMessages = new Set();
    }

    // 创建普通文本消息
    createTextMessage(data) {
        // 先初始化默认图片配置
        this.defaultImages = {
            avatar: './blivechat_files/noface.gif',
            memberBadges: "",

            ...data
        };

        const message = this.createTextMessageTemplate().cloneNode(true);

        // 设置基础属性
        message.setAttribute('author-type', data.authorType || '');
        message.setAttribute('privilegetype', data.privilegeType || '0');
        message.style.setProperty('--x-offset', `${data.offsetX || 0}px`);
        message.style.setProperty('--y-offset', `${data.offsetY || 0}px`);

        // 填充内容
        this.fillTextMessageContent(message, data);

        return message;
    }

    // 创建付费消息
    createPaidMessage(data) {
        // 先初始化默认图片配置
        this.defaultImages = {
            avatar: './blivechat_files/noface.gif',
            memberBadges: "",

            ...data
        };

        const message = this.createPaidMessageTemplate().cloneNode(true);

        message.setAttribute('price', data.price);
        message.setAttribute('price-level', data.priceLevel);
        message.style.setProperty('--x-offset', `${data.offsetX || 0}px`);
        message.style.setProperty('--y-offset', `${data.offsetY || 0}px`);

        this.fillPaidMessageContent(message, data);

        return message;
    }

    // 创建会员加入消息
    createMembershipMessage(data) {
        // 先初始化默认图片配置
        this.defaultImages = {
            avatar: './blivechat_files/noface.gif',
            memberBadges: "",

            ...data
        };

        const message = this.createMembershipMessageTemplate().cloneNode(true);

        message.setAttribute('privilegetype', data.privilegeType || '0');
        message.style.setProperty('--x-offset', `${data.offsetX || 0}px`);
        message.style.setProperty('--y-offset', `${data.offsetY || 0}px`);

        this.fillMembershipMessageContent(message, data);

        return message;
    }
    //-----------------//
    // 填充文本消息内容
    fillTextMessageContent(element, data) {

        // 时间戳
        const timestamp = element.querySelector('#timestamp');
        if (timestamp) timestamp.textContent = data.timestamp || '00:00';

        // 用户名称
        const authorName = element.querySelector('#author-name-text');
        if (authorName) authorName.textContent = data.authorName || '用户';

        // 消息内容
        const messageContent = element.querySelector('#message');
        if (messageContent) {
            this.buildMessageContent(messageContent, data.message);
        }

        // 徽章
        this.updateBadges(element, data.authorType, data.privilegeType);
    }

    // 填充付费消息内容
    fillPaidMessageContent(element, data) {
        const authorName = element.querySelector('#author-name');
        const purchaseAmount = element.querySelector('#purchase-amount');
        const timestamp = element.querySelector('#timestamp');
        const messageContent = element.querySelector('#message');

        if (authorName) authorName.textContent = data.authorName;
        if (purchaseAmount) purchaseAmount.textContent = `CN¥${data.price}`;
        if (timestamp) timestamp.textContent = data.timestamp || '00:00';
        if (messageContent) messageContent.textContent = data.message;
    }

    // 填充会员消息内容
    fillMembershipMessageContent(element, data) {
        const authorName = element.querySelector('#author-name');
        const headerSubtext = element.querySelector('#header-subtext');
        const timestamp = element.querySelector('#timestamp');

        if (authorName) authorName.textContent = data.authorName;
        if (headerSubtext) headerSubtext.textContent = data.subtext || '新会员';
        if (timestamp) timestamp.textContent = data.timestamp || '00:00';

        this.updateBadges(element, data.authorType, data.privilegeType);
    }

    // 构建消息内容（支持文本和表情）
    buildMessageContent(container, content) {
        container.innerHTML = '';

        if (typeof content === 'string') {
            container.innerHTML = content;
        } else if (Array.isArray(content)) {
            content.forEach(item => {
                if (item.type === 'text') {
                    const span = document.createElement('span');
                    span.textContent = item.text;
                    span.style.setProperty('color', item.color, 'important');
                    container.appendChild(span);
                } else if (item.type === 'emoji') {
                    const img = document.createElement('img');
                    img.className = 'emoji yt-formatted-string style-scope yt-live-chat-text-message-renderer';
                    img.alt = item.alt;
                    img.src = item.src;
                    img.width = item.width || 59;
                    img.height = item.height || 59;
                    container.appendChild(img);
                } else if (item.type === 'image') {
                    const div = document.createElement('div');
                    div.className = 'el-image content-img';
                    div.style.width = item.width || '120px';
                    div.style.height = item.height || '120px';
                    const img = document.createElement('img');
                    img.className = 'el-image__inner';
                    img.src = item.src;
                    div.appendChild(img);
                    container.appendChild(div);
                }
            });
        }
    }
    //-----------------//
    // 更新用户徽章
    updateBadges(element, authorType, privilegeType) {
        const badgesContainer = element.querySelector('#chat-badges');
        if (!badgesContainer) return;

        badgesContainer.innerHTML = '';

        // 房管徽章
        if (authorType === 'moderator') {
            const badge = this.createModeratorBadge();
            badgesContainer.appendChild(badge);
        }

        // 会员徽章
        if (authorType === 'member' && privilegeType && privilegeType !== '0') {
            const badge = this.createMemberBadge(privilegeType);
            badgesContainer.appendChild(badge);
        }
    }

    createModeratorBadge() {
        // 创建房管徽章SVG
        const badge = document.createElement('yt-live-chat-author-badge-renderer');
        badge.className = 'style-scope yt-live-chat-author-chip';
        badge.setAttribute('type', 'moderator');

        // 这里简化了SVG创建，实际使用时需要完整的SVG代码
        badge.innerHTML = `
            <div class="el-tooltip style-scope yt-live-chat-author-badge-renderer" tabindex="0">
                <yt-icon class="style-scope yt-live-chat-author-badge-renderer">
                    <svg
                                        class="style-scope yt-icon"
                                        focusable="false"
                                        preserveAspectRatio="xMidYMid meet"
                                        style="pointer-events: none; display: block; width: 100%; height: 100%;"
                                        viewBox="0 0 16 16"><g
                                        class="style-scope yt-icon"><path
                                        class="style-scope yt-icon"
                                        d="M9.64589146,7.05569719 C9.83346524,6.562372 9.93617022,6.02722257 9.93617022,5.46808511 C9.93617022,3.00042984 7.93574038,1 5.46808511,1 C4.90894765,1 4.37379823,1.10270499 3.88047304,1.29027875 L6.95744681,4.36725249 L4.36725255,6.95744681 L1.29027875,3.88047305 C1.10270498,4.37379824 1,4.90894766 1,5.46808511 C1,7.93574038 3.00042984,9.93617022 5.46808511,9.93617022 C6.02722256,9.93617022 6.56237198,9.83346524 7.05569716,9.64589147 L12.4098057,15 L15,12.4098057 L9.64589146,7.05569719 Z"></path></g></svg>
                </yt-icon>
            </div>
        `;

        return badge;
    }

    createMemberBadge(privilegeType) {
        const badge = document.createElement('yt-live-chat-author-badge-renderer');
        badge.className = 'style-scope yt-live-chat-author-chip';
        badge.setAttribute('type', 'member');

        const altTexts = {
            '1': '总督',
            '2': '提督',
            '3': '舰长'
        };

        badge.innerHTML = `
            <div class="el-tooltip style-scope yt-live-chat-author-badge-renderer" tabindex="0">
                <img alt="${altTexts[privilegeType]}" class="style-scope yt-live-chat-author-badge-renderer" src="${this.defaultImages.memberBadges}">
            </div>
        `;

        return badge;
    }

    // 模板创建方法
    createTextMessageTemplate() {
        const template = document.createElement('yt-live-chat-text-message-renderer');
        template.className = 'style-scope yt-live-chat-item-list-renderer';

        // 这里应该包含完整的HTML结构，简化示例
        template.innerHTML = `
            <yt-img-shadow class="no-transition style-scope yt-live-chat-text-message-renderer" height="24" id="author-photo">
                <img class="style-scope yt-img-shadow" height="24" src="${this.defaultImages.avatar}" width="24">
            </yt-img-shadow>
            <div class="style-scope yt-live-chat-text-message-renderer" id="content">
                <span class="style-scope yt-live-chat-text-message-renderer" id="timestamp"></span>
                <yt-live-chat-author-chip class="style-scope yt-live-chat-text-message-renderer">
                    <span class="style-scope yt-live-chat-author-chip" dir="auto" id="author-name">
                        <span id="author-name-text"></span>
                    </span>
                    <span class="style-scope yt-live-chat-author-chip" id="chat-badges"></span>
                </yt-live-chat-author-chip>
                <span class="style-scope yt-live-chat-text-message-renderer" id="message"></span>
            </div>
        `;

        return template;
    }

    createPaidMessageTemplate() {
        const template = document.createElement('yt-live-chat-paid-message-renderer');
        template.className = 'style-scope yt-live-chat-item-list-renderer style-scope yt-live-chat-item-list-renderer';

        // 付费消息的HTML结构
        template.innerHTML = `
            <div class="style-scope yt-live-chat-paid-message-renderer" id="card">
                <div class="style-scope yt-live-chat-paid-message-renderer" id="header">
                    <yt-img-shadow class="no-transition style-scope yt-live-chat-paid-message-renderer" height="40" id="author-photo">
                        <img class="style-scope yt-img-shadow" height="40" src="${this.defaultImages.avatar}" width="40">
                    </yt-img-shadow>
                    <div class="style-scope yt-live-chat-paid-message-renderer" id="header-content">
                        <div class="style-scope yt-live-chat-paid-message-renderer" id="header-content-primary-column">
                            <div class="style-scope yt-live-chat-paid-message-renderer" id="author-name"></div>
                            <div class="style-scope yt-live-chat-paid-message-renderer" id="purchase-amount"></div>
                        </div>
                        <span class="style-scope yt-live-chat-paid-message-renderer" id="timestamp"></span>
                    </div>
                </div>
                <div class="style-scope yt-live-chat-paid-message-renderer" id="content">
                    <div class="style-scope yt-live-chat-paid-message-renderer" dir="auto" id="message"></div>
                </div>
            </div>
        `;

        return template;
    }

    createMembershipMessageTemplate() {
        const template = document.createElement('yt-live-chat-membership-item-renderer');
        template.className = 'style-scope yt-live-chat-item-list-renderer style-scope yt-live-chat-item-list-renderer';

        // 会员消息的HTML结构
        template.innerHTML = `
            <div class="style-scope yt-live-chat-membership-item-renderer" id="card">
                <div class="style-scope yt-live-chat-membership-item-renderer" id="header">
                    <yt-img-shadow class="no-transition style-scope yt-live-chat-membership-item-renderer" height="40" id="author-photo">
                        <img class="style-scope yt-img-shadow" height="40" src="${this.defaultImages.avatar}" width="40">
                    </yt-img-shadow>
                    <div class="style-scope yt-live-chat-membership-item-renderer" id="header-content">
                        <div class="style-scope yt-live-chat-membership-item-renderer" id="header-content-primary-column">
                            <div class="style-scope yt-live-chat-membership-item-renderer" id="header-content-inner-column">
                                <yt-live-chat-author-chip class="style-scope yt-live-chat-membership-item-renderer">
                                    <span class="member style-scope yt-live-chat-author-chip" dir="auto" id="author-name"></span>
                                    <span class="style-scope yt-live-chat-author-chip" id="chat-badges"></span>
                                </yt-live-chat-author-chip>
                            </div>
                            <div class="style-scope yt-live-chat-membership-item-renderer" id="header-subtext"></div>
                        </div>
                        <div class="style-scope yt-live-chat-membership-item-renderer" id="timestamp"></div>
                    </div>
                </div>
            </div>
        `;

        return template;
    }

    getCount() {
        return this.TextMessages.size;
    }

}

// 使用示例
const chatBuilder = new YouTubeChatMessageBuilder();

// 创建普通消息
const textMessage = chatBuilder.createTextMessage({
    avatar: 'http://39.105.155.193:6380/favicon.ico',
    authorType: 'moderator',
    privilegeType: '0',
    memberBadges: '',
    authorName: '测试用户',
    timestamp: '14:11',
    message: [
        { type: 'text', text: '这是一条' },
        { type: 'emoji', alt: '[比心]', src: './blivechat_files/4e029593562283f00d39b99e0557878c4199c71d.png' },
        { type: 'text', text: '测试消息' }
    ],
    offsetX: 100,
    offsetY: 200
});

// 创建普通消息
const faceMessage = chatBuilder.createTextMessage({
    avatar: 'http://39.105.155.193:6380/favicon.ico',
    authorType: 'member',
    privilegeType: '1',
    memberBadges: './blivechat_files/guard-level-1.png',
    authorName: '测试用户',
    timestamp: '14:11',
    message: [
        { type: 'image', src: './blivechat_files/huangdou_xihuan.png' }
    ],
    offsetX: 100,
    offsetY: 200
});

// 创建付费消息
const paidMessage = chatBuilder.createPaidMessage({
    authorName: '付费用户',
    price: '30.00',
    priceLevel: '30',
    timestamp: '14:11',
    message: '这是一条付费消息',
    offsetX: 150,
    offsetY: 300
});

// 创建会员消息
const membershipMessage = chatBuilder.createMembershipMessage({
    authorName: '新会员',
    privilegeType: '2',
    subtext: '新会员',
    timestamp: '14:11',
    offsetX: 200,
    offsetY: 400
});

// 添加到DOM
itemContainer.appendChild(textMessage);
itemContainer.appendChild(faceMessage);
itemContainer.appendChild(paidMessage);
itemContainer.appendChild(membershipMessage);
scrollableContainer.scrollTop = scrollableContainer.scrollHeight;
itemContainer.appendChild(faceMessage);



class DanmuWebSocketClient {
    constructor() {
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.reconnectInterval = 3000; // 3秒
        this.reconnectTimer = null;

        // 页面加载后自动连接
        setTimeout(() => {
            this.connect();
        }, 1000);
    }

    connect() {
        try {
            // 如果已有连接，先关闭
            if (this.socket) {
                this.socket.close();
            }

            this.socket = new WebSocket('ws://localhost:8765');

            this.socket.onopen = () => {
                this.reconnectAttempts = 0;
                this.addDanmuMessage({
                    type: 'system',
                    message: '成功连接到弹幕服务器',
                    timestamp: Date.now() / 1000
                });
            };

            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                } catch (error) {
                    console.error('解析消息错误:', error);
                    this.addDanmuMessage({
                        type: 'system',
                        message: '解析消息错误',
                        timestamp: Date.now() / 1000
                    });
                }
            };

            this.socket.onclose = (event) => {
                console.log('WebSocket连接关闭:', event);
                this.addDanmuMessage({
                    type: 'system',
                    message: `连接已断开 (代码: ${event.code})`,
                    timestamp: Date.now() / 1000
                });
                this.handleReconnect();
            };

            this.socket.onerror = (error) => {
                console.error('WebSocket错误:', error);
                this.addDanmuMessage({
                    type: 'system',
                    message: '连接错误',
                    timestamp: Date.now() / 1000
                });
            };

        } catch (error) {
            console.error('创建连接错误:', error);
            this.addDanmuMessage({
                type: 'system',
                message: '创建连接错误',
                timestamp: Date.now() / 1000
            });
            this.handleReconnect();
        }
    }

    handleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            this.addDanmuMessage({
                type: 'system',
                message: `连接失败，已尝试 ${this.reconnectAttempts} 次`,
                timestamp: Date.now() / 1000
            });
            return;
        }

        this.reconnectAttempts++;
        const delay = Math.min(this.reconnectInterval * Math.pow(1.5, this.reconnectAttempts - 1), 60000); // 最大60秒

        this.addDanmuMessage({
            type: 'system',
            message: `连接断开，${Math.round(delay/1000)}秒后尝试重连 (${this.reconnectAttempts}/${this.maxReconnectAttempts})`,
            timestamp: Date.now() / 1000
        });
        clearTimeout(this.reconnectTimer);
        this.reconnectTimer = setTimeout(() => {
            this.connect();
        }, delay);
    }

    handleMessage(data) {
        // 根据消息类型处理
        switch (data.type) {
//            case 'gift':
//            case 'combo_gift':
//            case 'guard_buy':
//            case 'red_pocket':
//            case 'red_pocket_v2':
//            case 'user_toast':
//            case 'user_toast_v2':
//                this.addGiftMessage(data);
//                break;
//
//            case 'super_chat':
//            case 'super_chat_jpn':
//                this.addSuperChatMessage(data);
//                break;
//
            case 'live_start':
            case 'system':
            case 'danmu':
                this.addDanmuMessage(data);
                break;

            default:
                console.log('未知消息类型:', data.type);
        }
    }

    // 弹幕消息
    addDanmuMessage(data) {
        const time = new Date(data.timestamp * 1000).toLocaleTimeString();
        let textMessage;
        switch(data.type) {
            case 'system':
                // 创建系统消息
                textMessage = chatBuilder.createTextMessage({
                    authorType: 'moderator',
                    privilegeType: '0',
                    authorName: '系统消息',
                    timestamp: time,
                    message: data.message,
                    offsetX: 100,
                    offsetY: 200
                });
                break;
            case 'live_start':
                // 创建系统消息
                textMessage = chatBuilder.createTextMessage({
                    authorType: 'moderator',
                    privilegeType: '0',
                    authorName: '开播消息',
                    timestamp: time,
                    message: '🔴直播开始：房间' + data.roomid + '时间' + time + '平台' + data.live_platform,
                    offsetX: 100,
                    offsetY: 200
                });
                break;
            case 'danmu':
                // 创建普通消息
                textMessage = chatBuilder.createTextMessage({
                    avatar: data.face,
                    authorType: data.authorType,
                    privilegeType: data.guard_level,
                    memberBadges: data.guard_icon,
                    authorName: data.user,
                    timestamp: time,
                    message: data.message_list,
                    offsetX: 100,
                    offsetY: 200
                });
                break;
        }
        itemContainer.appendChild(textMessage);
        this.scrollToBottom();
    }

    // 礼物消息
    addGiftMessage(data) {
        const time = new Date(data.timestamp * 1000).toLocaleTimeString();
        let content = '';
        let className = 'message-gift';

        switch(data.type) {
            case 'gift':
                const price = (data.total_coin / 1000).toFixed(2);
                content = `
                    <div class="message-header">
                        <span>${time}</span>
                        <span>礼物</span>
                    </div>
                    <div class="message-content">
                        <span class="wealth-info">${data.wealth || ''}</span>
                        <span class="medal-info">${data.medal || ''}</span>
                        <span class="user-info">${data.user}</span>
                        赠送了 ${data.gift_count} 个 ${data.gift_name} (${price}元)
                    </div>
                `;
                break;

            case 'combo_gift':
                const comboPrice = (data.total_coin / 1000).toFixed(2);
                content = `
                    <div class="message-header">
                        <span>${time}</span>
                        <span>连击礼物</span>
                    </div>
                    <div class="message-content">
                        <span class="wealth-info">${data.wealth || ''}</span>
                        <span class="medal-info">${data.medal || ''}</span>
                        <span class="user-info">${data.user}</span>
                        连续赠送 ${data.combo_num} 个 ${data.gift_name} (${comboPrice}元)
                    </div>
                `;
                className = 'message-gift message-combo';
                break;

            case 'guard_buy':
                content = `
                    <div class="message-header">
                        <span>${time}</span>
                        <span>上舰</span>
                    </div>
                    <div class="message-content">
                        <span class="user-info">${data.user}</span>
                        开通了 ${data.guard_name} x${data.guard_count}
                    </div>
                `;
                className = 'message-gift message-guard';
                break;

            case 'red_pocket':
            case 'red_pocket_v2':
                content = `
                    <div class="message-header">
                        <span>${time}</span>
                        <span>红包</span>
                    </div>
                    <div class="message-content">
                        <span class="wealth-info">${data.wealth || ''}</span>
                        <span class="medal-info">${data.medal || ''}</span>
                        <span class="user-info">${data.user}</span>
                        🔖 ${data.action} ${data.price}元
                    </div>
                `;
                className = 'message-gift message-redpocket';
                break;

            case 'user_toast':
            case 'user_toast_v2':
                content = `
                    <div class="message-header">
                        <span>${time}</span>
                        <span>大航海</span>
                    </div>
                    <div class="message-content">
                        <span class="user-info">${data.user}</span>
                        🚢 开通了 ${data.guard_name} (${data.price}元/${data.unit})
                    </div>
                `;
                className = 'message-gift message-toast';
                break;
        }

        const messageElement = this.createMessageElement(data, className, content);
        this.giftMessagesContainer.appendChild(messageElement);
        this.scrollToBottom();
    }

    // 醒目留言消息
    addSuperChatMessage(data) {
        const time = new Date(data.timestamp * 1000).toLocaleTimeString();
        const content = `
            <div class="message-header">
                <span>${time}</span>
                <span>醒目留言</span>
            </div>
            <div class="message-content">
                <span class="medal-info">${data.medal || ''}</span>
                <span class="user-info">${data.user}</span>
                💬 ${data.price}元 ${data.duration}秒
                <div class="superchat-message">${data.message}</div>
            </div>
        `;

        const messageElement = this.createMessageElement(data, 'message-superchat', content);
        this.superchatMessagesContainer.appendChild(messageElement);
        this.hideEmptyState(this.superchatMessagesContainer, this.superchatEmpty);
        this.scrollToBottom(this.superchatMessagesContainer);
    }

    scrollToBottom() {
        scrollableContainer.scrollTop = scrollableContainer.scrollHeight;
    }
}

// 初始化客户端
document.addEventListener('DOMContentLoaded', () => {
    new DanmuWebSocketClient();
});

