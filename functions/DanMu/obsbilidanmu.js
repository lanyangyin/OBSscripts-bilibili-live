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
    onUpdate: (percentage, ticker) => {
        console.log(`当前百分比: ${percentage}%`);
    },
    onRemove: (ticker) => {
        console.log('小金额消息已移除');
    }
});

// 添加到页面
tickerContainer.appendChild(smallAmount.getElement());




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
            moderatorBadge: '', // SVG图标，使用内联SVG
            memberBadges: {
                '1': './blivechat_files/guard-level-1.png', // 总督
                '2': './blivechat_files/guard-level-2.png', // 提督
                '3': './blivechat_files/guard-level-3.png'  // 舰长
            },
            emojis: {
                'dog': './blivechat_files/4428c84e694fbf4e0ef6c06e958d9352c3582740.png',
                '比心': './blivechat_files/4e029593562283f00d39b99e0557878c4199c71d.png',
                '喝彩': './blivechat_files/b51824125d09923a4ca064f0c0b49fc97d3fab79.png',
                '吃瓜': './blivechat_files/ffb53c252b085d042173379ac724694ce3196194.png'
            },
            contentImages: {
                'huangdou_xihuan': './blivechat_files/huangdou_xihuan.png',
                'sakaban_jiayu_yutou': './blivechat_files/sakaban_jiayu_yutou.png',
                'miaoa': './blivechat_files/miaoa.png',
                'lipu': './blivechat_files/lipu.png'
            },
            decorativeImages: {
                'hat': './blivechat_files/hat.png',
                'ear': './blivechat_files/ear.png',
                'scarf': './blivechat_files/scarf.png',
                'leftEar': './blivechat_files/leftEar.png',
                'rightEar': './blivechat_files/rightEar.png',
                'kiti-scarf': './blivechat_files/scarf(1).png',
                'tail': './blivechat_files/tail.png',
                'flower': './blivechat_files/flower.png'
            },

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
            moderatorBadge: '', // SVG图标，使用内联SVG
            memberBadges: {
                '1': './blivechat_files/guard-level-1.png', // 总督
                '2': './blivechat_files/guard-level-2.png', // 提督
                '3': './blivechat_files/guard-level-3.png'  // 舰长
            },
            emojis: {
                'dog': './blivechat_files/4428c84e694fbf4e0ef6c06e958d9352c3582740.png',
                '比心': './blivechat_files/4e029593562283f00d39b99e0557878c4199c71d.png',
                '喝彩': './blivechat_files/b51824125d09923a4ca064f0c0b49fc97d3fab79.png',
                '吃瓜': './blivechat_files/ffb53c252b085d042173379ac724694ce3196194.png'
            },
            contentImages: {
                'huangdou_xihuan': './blivechat_files/huangdou_xihuan.png',
                'sakaban_jiayu_yutou': './blivechat_files/sakaban_jiayu_yutou.png',
                'miaoa': './blivechat_files/miaoa.png',
                'lipu': './blivechat_files/lipu.png'
            },
            decorativeImages: {
                'hat': './blivechat_files/hat.png',
                'ear': './blivechat_files/ear.png',
                'scarf': './blivechat_files/scarf.png',
                'leftEar': './blivechat_files/leftEar.png',
                'rightEar': './blivechat_files/rightEar.png',
                'kiti-scarf': './blivechat_files/scarf(1).png',
                'tail': './blivechat_files/tail.png',
                'flower': './blivechat_files/flower.png'
            },

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
            moderatorBadge: '', // SVG图标，使用内联SVG
            memberBadges: {
                '1': './blivechat_files/guard-level-1.png', // 总督
                '2': './blivechat_files/guard-level-2.png', // 提督
                '3': './blivechat_files/guard-level-3.png'  // 舰长
            },
            emojis: {
                'dog': './blivechat_files/4428c84e694fbf4e0ef6c06e958d9352c3582740.png',
                '比心': './blivechat_files/4e029593562283f00d39b99e0557878c4199c71d.png',
                '喝彩': './blivechat_files/b51824125d09923a4ca064f0c0b49fc97d3fab79.png',
                '吃瓜': './blivechat_files/ffb53c252b085d042173379ac724694ce3196194.png'
            },
            contentImages: {
                'huangdou_xihuan': './blivechat_files/huangdou_xihuan.png',
                'sakaban_jiayu_yutou': './blivechat_files/sakaban_jiayu_yutou.png',
                'miaoa': './blivechat_files/miaoa.png',
                'lipu': './blivechat_files/lipu.png'
            },
            decorativeImages: {
                'hat': './blivechat_files/hat.png',
                'ear': './blivechat_files/ear.png',
                'scarf': './blivechat_files/scarf.png',
                'leftEar': './blivechat_files/leftEar.png',
                'rightEar': './blivechat_files/rightEar.png',
                'kiti-scarf': './blivechat_files/scarf(1).png',
                'tail': './blivechat_files/tail.png',
                'flower': './blivechat_files/flower.png'
            },

            ...data
        };

        const message = this.createMembershipMessageTemplate().cloneNode(true);

        message.setAttribute('privilegetype', data.privilegeType || '0');
        message.style.setProperty('--x-offset', `${data.offsetX || 0}px`);
        message.style.setProperty('--y-offset', `${data.offsetY || 0}px`);

        this.fillMembershipMessageContent(message, data);

        return message;
    }

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

        this.updateBadges(element, 'member', data.privilegeType);
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
                    const img = document.createElement('img');
                    img.className = 'el-image__inner';
                    img.src = item.src;
                    div.appendChild(img);
                    container.appendChild(div);
                }
            });
        }
    }

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
                    <!-- SVG内容 -->
                </yt-icon>
            </div>
        `;

        return badge;
    }

    createMemberBadge(privilegeType) {
        const badge = document.createElement('yt-live-chat-author-badge-renderer');
        badge.className = 'style-scope yt-live-chat-author-chip';
        badge.setAttribute('type', 'member');

        const levelImages = {
            '1': 'guard-level-1.png', // 总督
            '2': 'guard-level-2.png', // 提督
            '3': 'guard-level-3.png'  // 舰长
        };

        const altTexts = {
            '1': '总督',
            '2': '提督',
            '3': '舰长'
        };

        badge.innerHTML = `
            <div class="el-tooltip style-scope yt-live-chat-author-badge-renderer" tabindex="0">
                <img alt="${altTexts[privilegeType]}" class="style-scope yt-live-chat-author-badge-renderer"
                     src="./blivechat_files/${levelImages[privilegeType]}">
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


const chatBuilderManager = new YouTubeChatMessageBuilder();

// 使用示例
const chatBuilder = new YouTubeChatMessageBuilder();

// 创建普通消息
const textMessage = chatBuilder.createTextMessage({
    authorType: 'member',
    privilegeType: '0',
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
itemContainer.appendChild(paidMessage);
itemContainer.appendChild(membershipMessage);
scrollableContainer.scrollTop = scrollableContainer.scrollHeight;






















class DanmuWebSocketClient {
    constructor() {
        this.socket = null;
        this.isConnecting = false;
        this.autoReconnect = true;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.reconnectInterval = 3000; // 3秒
        this.reconnectTimer = null;

        // 统计变量
        this.interactCount = 0;
        this.giftCount = 0;
        this.systemCount = 0;

        // 新的统计变量
        this.watchedCount = 0;
        this.popularRankCount = 0;
        this.onlineRankCount = 0;
        this.likeCount = 0;

        this.initializeElements();

        // 页面加载后自动连接
        setTimeout(() => {
            this.connect();
        }, 1000);
    }

    initializeElements() {
        // 消息容器
        this.danmuMessagesContainer = document.getElementById('danmuMessages');
        this.giftMessagesContainer = document.getElementById('giftMessages');
        this.superchatMessagesContainer = document.getElementById('superchatMessages');
        this.interactMessagesContainer = document.getElementById('interactMessages');
        this.systemMessagesContainer = document.getElementById('systemMessages');

        // 空状态提示
        this.danmuEmpty = document.getElementById('danmuEmpty');
        this.giftEmpty = document.getElementById('giftEmpty');
        this.superchatEmpty = document.getElementById('superchatEmpty');
        this.interactEmpty = document.getElementById('interactEmpty');
        this.systemEmpty = document.getElementById('systemEmpty');

        // 计数元素
        this.watchedCountElement = document.getElementById('watchedCount');
        this.popularRankElement = document.getElementById('popularRankCount');
        this.onlineRankCountElement = document.getElementById('onlineRankCount');
        this.likeCountElement = document.getElementById('likeCount');
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
                this.addSystemMessage({
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
                    this.addSystemMessage({
                        type: 'system',
                        message: '解析消息错误',
                        timestamp: Date.now() / 1000
                    });
                }
            };

            this.socket.onclose = (event) => {
                console.log('WebSocket连接关闭:', event);
                this.addSystemMessage({
                    type: 'system',
                    message: `连接已断开 (代码: ${event.code})`,
                    timestamp: Date.now() / 1000
                });
                this.handleReconnect();
            };

            this.socket.onerror = (error) => {
                console.error('WebSocket错误:', error);
                this.addSystemMessage({
                    type: 'system',
                    message: '连接错误',
                    timestamp: Date.now() / 1000
                });
            };

        } catch (error) {
            console.error('创建连接错误:', error);
            this.addSystemMessage({
                type: 'system',
                message: '创建连接错误',
                timestamp: Date.now() / 1000
            });
            this.handleReconnect();
        }
    }

    handleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            this.addSystemMessage({
                type: 'system',
                message: `连接失败，已尝试 ${this.reconnectAttempts} 次`,
                timestamp: Date.now() / 1000
            });
            return;
        }

        this.reconnectAttempts++;
        const delay = Math.min(this.reconnectInterval * Math.pow(1.5, this.reconnectAttempts - 1), 60000); // 最大60秒

        this.addSystemMessage({
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
            case 'danmu':
                this.addDanmuMessage(data);
                break;

            case 'gift':
            case 'combo_gift':
            case 'guard_buy':
            case 'red_pocket':
            case 'red_pocket_v2':
            case 'user_toast':
            case 'user_toast_v2':
                this.addGiftMessage(data);
                break;

            case 'super_chat':
            case 'super_chat_jpn':
                this.addSuperChatMessage(data);
                break;

            case 'interact':
            case 'like_click':
            case 'interaction_combo':
                this.addInteractMessage(data);
                break;

            case 'watched_change':
                this.watchedCount = data.num;
                this.watchedCountElement.textContent = this.watchedCount;
                break;

            case 'online_rank_count':
                this.onlineRankCount = data.count;
                this.onlineRankCountElement.textContent = this.onlineRankCount;
                break;

            case 'like_update':
                this.likeCount = data.click_count;
                this.likeCountElement.textContent = this.likeCount;
                break;

            case 'live_start':
            case 'popular_rank_changed':
                this.popularRankCount = data.rank;
                this.popularRankElement.textContent = this.popularRankCount
                break;

            case 'system':
                this.addSystemMessage(data);
                break;

            default:
                this.addUnknownMessage(data);
        }
    }

    // 辅助函数：隐藏空状态提示
    hideEmptyState(container, emptyElement) {
        if (emptyElement.style.display !== 'none') {
            emptyElement.style.display = 'none';
        }
    }

    // 辅助函数：创建消息元素
    createMessageElement(data, className, content) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${className}`;
        messageElement.innerHTML = content;
        return messageElement;
    }

    // 弹幕消息
    addDanmuMessage(data) {
        const time = new Date(data.timestamp * 1000).toLocaleTimeString();
        const content = `
            <div class="message-header">
                <span>${time}</span>
                <span>弹幕</span>
            </div>
            <div class="message-content">
                <span class="wealth-info">${data.wealth || ''}</span>
                <span class="medal-info">${data.medal || ''}</span>
                <span class="user-info">${data.user}</span>：
                ${data.content}
                ${data.reply_to ? `<span style="color: #888;">${data.reply_to}</span>` : ''}
            </div>
        `;

        const messageElement = this.createMessageElement(data, 'message-danmu', content);
        this.danmuMessagesContainer.appendChild(messageElement);
        this.hideEmptyState(this.danmuMessagesContainer, this.danmuEmpty);
        this.scrollToBottom(this.danmuMessagesContainer);
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
        this.hideEmptyState(this.giftMessagesContainer, this.giftEmpty);
        this.scrollToBottom(this.giftMessagesContainer);
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

    // 互动消息
    addInteractMessage(data) {
        const time = new Date(data.timestamp * 1000).toLocaleTimeString();
        let content = '';
        let className = 'message-interact';

        if (data.type === 'like_click') {
            content = `
                <div class="message-header">
                    <span>${time}</span>
                    <span>点赞</span>
                </div>
                <div class="message-content">
                    <span class="wealth-info">${data.wealth || ''}</span>
                    <span class="medal-info">${data.medal || ''}</span>
                    <span class="user-info">${data.user}</span>
                    👍 ${data.like_text}
                </div>
            `;
            className = 'message-interact message-like';
        } else if (data.type === 'interaction_combo') {
            content = `
                <div class="message-header">
                    <span>${time}</span>
                    <span>连续互动</span>
                </div>
                <div class="message-content">
                    ${data.message}
                </div>
            `;
        } else {
            content = `
                <div class="message-header">
                    <span>${time}</span>
                    <span>互动</span>
                </div>
                <div class="message-content">
                    <span class="wealth-info">${data.wealth || ''}</span>
                    <span class="medal-info">${data.medal || ''}</span>
                    <span class="user-info">${data.user}</span>
                    ${data.action}
                </div>
            `;
        }

        const messageElement = this.createMessageElement(data, className, content);
        this.interactMessagesContainer.appendChild(messageElement);
        this.hideEmptyState(this.interactMessagesContainer, this.interactEmpty);
        this.scrollToBottom(this.interactMessagesContainer);
    }

    // 系统消息
    addSystemMessage(data) {
        const time = new Date(data.timestamp * 1000).toLocaleTimeString();
        let content = '';

        switch(data.type) {
            case 'system':
                content = `
                    <div class="message-header">
                        <span>${time}</span>
                        <span>系统</span>
                    </div>
                    <div class="message-content">
                        ${data.message}
                    </div>
                `;
                break;
        }

        const messageElement = this.createMessageElement(data, 'message-system', content);
        this.systemMessagesContainer.appendChild(messageElement);
        this.hideEmptyState(this.systemMessagesContainer, this.systemEmpty);
        this.scrollToBottom(this.systemMessagesContainer);
    }

    addUnknownMessage(data) {
        const time = new Date(data.timestamp * 1000).toLocaleTimeString();
        const content = `
            <div class="message-header">
                <span>${time}</span>
                <span>未知消息</span>
            </div>
            <div class="message-content">
                未知命令: ${data.cmd}
            </div>
        `;

        const messageElement = this.createMessageElement(data, 'message-system', content);
        this.systemMessagesContainer.appendChild(messageElement);
        this.hideEmptyState(this.systemMessagesContainer, this.systemEmpty);
        this.scrollToBottom(this.systemMessagesContainer);
    }

    scrollToBottom(container) {
        container.scrollTop = container.scrollHeight;
    }
}

// 初始化客户端
document.addEventListener('DOMContentLoaded', () => {
    new DanmuWebSocketClient();
});

