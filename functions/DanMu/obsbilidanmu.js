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
            onRemove: null, // 倒计时结束删除时的回调，参数是实例
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
                    <yt-img-shadow class="no-transition style-scope yt-live-chat-ticker-paid-message-item-renderer" height="24" id="author-photo" loaded="" style="background-color: transparent;" width="24">
                        <img alt="" class="style-scope yt-img-shadow" height="24" id="img" src="${this.config.avatarSrc}" width="24">
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
            uName: '', // 昵称
            uId: '', // id
            facePicture: 'https://static.hdslb.com/images/member/noface.gif',  // 头像
            facePictureX: '',  // 头像宽度px
            facePictureY: '',  // 头像高度px
            identityTitle: '', // 身份头衔：管理员 moderator，船员 member，主播 owner，普通为空
            privilegeLevel: '0', // 特权级别 1,2,3,0
            fleetTitle: '',  // 舰队称号
            fanMedalName: '', // 粉丝勋章名称
            fanMedalLevel: '0', //粉丝勋章等级
            fanMedalColorStart: '', // 粉丝勋章开始颜色
            fanMedalColorEnd: '', // 粉丝勋章结束颜色
            fanMedalColorBorder: '', // 粉丝勋章边框颜色
            fanMedalColorText: '', // 粉丝勋章文本色
            fanMedalColorLevel: '', // 粉丝勋章等级颜色
            fanMedalTextSize: '', // 粉丝勋章字体大小
            fleetBadge: '',  // 舰队徽章
            messageData: '',  // 消息数据
            messageTextSize: '', //
            sendTime: '00:00',  // 发送时间
            timeTextSize: '',
            isAdmin: false,  // 是否管理员
            isFanGroup: false, // 是否有粉丝勋章或者是否有本直播间的粉丝勋章
            lineBreakDisplay: false,

            ...data
        };

        const message = this.createTextMessageTemplate().cloneNode(true);
        message.setAttribute('author-type', this.defaultImages.identityTitle);
        if (this.defaultImages.isAdmin) message.setAttribute('is-admin', this.defaultImages.isAdmin);
        if (this.defaultImages.isFanGroup) message.setAttribute('is-fan-group', this.defaultImages.isFanGroup);
        message.setAttribute('medal-level', this.defaultImages.fanMedalLevel);
        message.setAttribute('privilegetype', this.defaultImages.privilegeLevel);
        message.style.position = 'relative';
        message.style.setProperty('font-size', `${this.defaultImages.messageTextSize}px`);  // 字体大小
        message.style.padding = '4px 24px';  // 上下间距 左右间距
        message.style.display = 'flex';
        message.style.setProperty('flex-direction', 'row');
        message.style.setProperty('align-items', 'flex-start');

        const cardElement = message.querySelector('#card');
        cardElement.style.display = 'flex';
        cardElement.style.setProperty('flex-direction', 'row !important');
        cardElement.style.setProperty('align-items', 'flex-start');
        cardElement.style.setProperty('width', '100%');

        // 头像父元素
        const authorPhotoElement = message.querySelector('#author-photo');
        authorPhotoElement.height = `${this.defaultImages.facePictureY}`;
        authorPhotoElement.width = `${this.defaultImages.facePictureX}`;
        authorPhotoElement.style.setProperty('background-color', 'transparent');

        // 头像
        const imgElement = message.querySelector('#img');
        imgElement.height = `${this.defaultImages.facePictureY}`;
        imgElement.width = `${this.defaultImages.facePictureX}`;
        imgElement.src = `${this.defaultImages.facePicture}`;
        imgElement.alt = `${this.defaultImages.uId}`;
        imgElement.style.setProperty('background-color', 'transparent');

        if (this.defaultImages.lineBreakDisplay) {
            const contentElement = message.querySelector('#content');
            contentElement.style.display = 'flex';
            contentElement.style.setProperty('flex-direction', 'column');
            contentElement.style.setProperty('align-items', 'flex-start');
        }

        // 时间戳
        const timestamp = message.querySelector('#timestamp');
        if (timestamp) timestamp.textContent = data.sendTime || '00:00';
        timestamp.style.setProperty('font-size', `${this.defaultImages.fanMedalTextSize}px`);  // 字体大小

        const authorNameElement = message.querySelector('#author-name');
        authorNameElement.setAttribute('type', `${this.defaultImages.identityTitle}`);

        // 用户名称
        const authorNameText = message.querySelector('#author-name-text');
        if (authorNameText) authorNameText.textContent = data.uName || '用户';

        const imgMsg = message.querySelector('#image-and-message');
        imgMsg.style.width = 'auto';
        imgMsg.style.height = 'auto';


        const repeatedElement = message.querySelector('.el-badge.style-scope.yt-live-chat-text-message-renderer');
        repeatedElement.style.setProperty('--repeated-mark-color', 'hsl(210, 100%, 62.5%)');
        repeatedElement.style.display = 'none';

        // 消息内容
        const messageContent = message.querySelector('#message');
        if (messageContent) this.buildMessageContent(messageContent, data.messageData);

        // 徽章
        this.updateBadges(message, data.identityTitle, data.privilegeLevel);

        return message;
    }

    // 创建付费消息
    createPaidMessage(data) {
        // 先初始化默认图片配置
        this.defaultImages = {
            authorName: '', // 昵称
            avatar: './blivechat_files/noface.gif', // 头像位置
            timestamp: '00:00', // 时间
            message: '', // 文字内容
            showOnlyHeader: false, // 是否显示文字区域
            price: '0', // 显示金额（元）
            priceLevel: '0',  // 金额等级
            messagePrimaryColor: 'rgba(29,233,182,1)', // 文字区域颜色
            messageSecondaryColor: 'rgba(0,191,165,1)', // 头像昵称金额区域颜色
            messageHeaderColor: 'rgba(0,0,0,1)', // 金额文字颜色
            messageAuthorNameColor: 'rgba(0,0,0,0.541176)', // 昵称文字颜色
            messageTimestampColor: 'rgba(0,0,0,0.501961)', // 时间文字颜色
            messageColor: 'rgba(0,0,0,1)', // 文字颜色
            offsetX: 0, // 横向偏移量
            offsetY: 0, // 纵向偏移量

            ...data
        };

        const message = this.createPaidMessageTemplate().cloneNode(true);
        message.setAttribute('price', data.price);
        message.setAttribute('price-level', data.priceLevel);
        message.setAttribute('offsetx', `${data.offsetX || 0}px`);
        message.setAttribute('offsety', `${data.offsetY || 0}px`);
        message.style.setProperty('--x-offset', `${data.offsetX || 0}px`);
        message.style.setProperty('--y-offset', `${data.offsetY || 0}px`);
        message.style.setProperty('--yt-live-chat-paid-message-primary-color', this.defaultImages.messagePrimaryColor);
        message.style.setProperty('--yt-live-chat-paid-message-secondary-color', this.defaultImages.messageSecondaryColor);
        message.style.setProperty('--yt-live-chat-paid-message-header-color', this.defaultImages.messageHeaderColor);
        message.style.setProperty('--yt-live-chat-paid-message-author-name-color', this.defaultImages.messageAuthorNameColor);
        message.style.setProperty('--yt-live-chat-paid-message-timestamp-color', this.defaultImages.messageTimestampColor);
        message.style.setProperty('--yt-live-chat-paid-message-color', this.defaultImages.messageColor);
        if (this.defaultImages.showOnlyHeader) {
            message.setAttribute('show-only-header', true);
        }

        this.fillPaidMessageContent(message, data);

        return message;
    }

    // 创建会员加入消息
    createMembershipMessage(data) {
        // 先初始化默认图片配置
        this.defaultImages = {
            authorName: '', // 昵称
            avatar: './blivechat_files/noface.gif', // 头像位置
            memberBadges: "",  // 舰长勋章图标位置
            membershipCardColor: "#820f9d", // 低层颜色
            membershipHeaderColor: "#820f9d",  // 上层颜色
            authorType: "member",
            privilegeType: '1', // 舰长级别
            offsetX: 0, // 横向偏移量
            offsetY: 0, // 纵向偏移量

            ...data
        };

        const message = this.createMembershipMessageTemplate().cloneNode(true);

        message.setAttribute('privilegetype', data.privilegeType || '0');
        message.setAttribute('offsetx', `${data.offsetX || 0}px`);
        message.setAttribute('offsety', `${data.offsetY || 0}px`);
        message.style.setProperty('--x-offset', `${data.offsetX || 0}px`);
        message.style.setProperty('--y-offset', `${data.offsetY || 0}px`);

        this.fillMembershipMessageContent(message, data);

        return message;
    }
    //-----------------//
    // 填充付费消息内容
    fillPaidMessageContent(element, data) {
        const authorName = element.querySelector('#author-name');
        const purchaseAmount = element.querySelector('#purchase-amount');
        const timestamp = element.querySelector('#timestamp');
        const messageContent = element.querySelector('#message');
        const contentContent = element.querySelector('#content');

        if (authorName) authorName.textContent = data.authorName;
        if (purchaseAmount) purchaseAmount.textContent = `CN¥${data.price}`;
        if (timestamp) timestamp.textContent = data.timestamp || '00:00';
        if (messageContent) messageContent.textContent = data.message;
        if (this.defaultImages.showOnlyHeader) {
            if (contentContent) contentContent.style.visibility = 'hidden';
            if (contentContent) contentContent.style.display = 'none';
            if (contentContent) contentContent.style.padding = '0';
        }
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
                    if (item.color !== '') span.style.setProperty('color', item.color, 'important');
                    if (item.shadow !== '') span.style.setProperty('text-shadow', `${item.shadow}`);
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
                    console.log('大表情宽度:', parseInt(div.style.width));
                    div.style.height = `${parseInt(item.height) * parseInt(div.style.width) / parseInt(item.width)}px`;
                    console.log('大表情高度:', div.style.height);
                    const img = document.createElement('img');
                    img.className = 'el-image__inner';
                    img.src = item.src;
                    img.alt = item.alt;
                    div.appendChild(img);
                    container.appendChild(div);
                }
            });
        }
    }
    //-----------------//
    // 更新用户徽章
    updateBadges(element, identityTitle, privilegeLevel) {
        const medalContainer = element.querySelector('#chat-medal');
        if (!medalContainer) return;
        medalContainer.innerHTML = '';

        const badgesContainer = element.querySelector('#chat-badges');
        if (!badgesContainer) return;
        badgesContainer.innerHTML = '';

        // 粉丝徽章
        if (this.defaultImages.isFanGroup) {
            const badge = this.createMedal();
            badge.setAttribute('is-fan-group', `${this.defaultImages.isFanGroup}`);
            badge.setAttribute('medal-name', `${this.defaultImages.fanMedalName}`);
            badge.setAttribute('medal-nevel', `${this.defaultImages.fanMedalLevel}`);
            badge.style.setProperty('--yt-live-chat-medal-background-color', `linear-gradient(to right, ${this.defaultImages.fanMedalColorStart}, ${this.defaultImages.fanMedalColorEnd})`);
            badge.style.setProperty('--yt-live-chat-medal-border-color', this.defaultImages.fanMedalColorBorder);
            badge.style.setProperty('--yt-live-chat-medal-text-color', this.defaultImages.fanMedalColorLevel); // 粉丝勋章等级颜色
            badge.style.margin = '0 0 0 4px'; // 上间隔 右间隔 下间隔 左间隔
            badge.style.setProperty('text-shadow', '0px 0px 0px #000000'); // 水平阴影的位置 垂直阴影的位置 模糊的距离 阴影的颜色.
            badge.style.display = 'inline-block';

            const medalCard = badge.querySelector('#medal-card');
            medalCard.style.position = 'relative';
            medalCard.style.width = 'max-content';
            medalCard.style.background = 'var(--yt-live-chat-medal-background-color,#222)';
            medalCard.style.border = 'var(--yt-live-chat-medal-border-color,#222) solid 2px';
            medalCard.style.border = 'relative';
            medalCard.style.setProperty('border-radius', '4px');
            medalCard.style.setProperty('display', 'flex');
            medalCard.style.setProperty('-ms-flex-direction', 'row');
            medalCard.style.setProperty('-webkit-flex-direction', 'row');
            medalCard.style.setProperty('flex-direction', 'row');
            medalCard.style.setProperty('-ms-flex-align', 'center');
            medalCard.style.setProperty('-webkit-align-items', 'center');
            medalCard.style.setProperty('align-items', 'center');
            medalCard.style.setProperty('overflow', 'hidden');

            const clsMedalRenderer = badge.querySelector('.yt-live-chat-author-medal-renderer');
            clsMedalRenderer.style.setProperty('font-size', `${this.defaultImages.timeTextSize}px`);
            clsMedalRenderer.style.setProperty('line-height', '14px');

            const medalName = badge.querySelector('#medal-name');
            medalName.style.setProperty('text-shadow', 'none');
            medalName.style.padding = '2px 4px';  // 上下间距 左右间距
            medalName.style.color = this.defaultImages.fanMedalColorText;
            medalName.textContent = this.defaultImages.fanMedalName;

            const medalLevel = badge.querySelector('#medal-level');
            medalLevel.style.padding = '2px 4px';  // 上下间距 左右间距
            medalLevel.style.setProperty('font-weight', '700');
            medalLevel.style.setProperty('text-shadow', 'none');
            medalLevel.style.setProperty('text-align', 'center');
            medalLevel.style.setProperty('background-color', '#FFFFFF');
            medalLevel.style.color = 'var(--yt-live-chat-medal-text-color,#222)';
            medalLevel.style.setProperty('border-top-right-radius', '2px');
            medalLevel.style.setProperty('border-bottom-right-radius', '2px');
            medalLevel.textContent = this.defaultImages.fanMedalLevel;

            medalContainer.appendChild(badge);
        }

        // 舰长徽章
        if (privilegeLevel && privilegeLevel !== '0') {
            const badge = this.createMemberBadge();
            const img = badge.querySelector('img');
            img.alt = `${this.defaultImages.fleetTitle}`
            img.src = `${this.defaultImages.fleetBadge}`
            badgesContainer.appendChild(badge);
        }

        // 房管徽章
        if (this.defaultImages.isAdmin) {
            const badge = this.createModeratorBadge();
            badgesContainer.appendChild(badge);
        }
    }

    // 创建粉丝勋章
    createMedal() {
        // 创建粉丝勋章
        const badge = document.createElement('yt-live-chat-author-medal-renderer');
        badge.className = 'style-scope yt-live-chat-author-chip';

        badge.innerHTML = `
            <div class="style-scope yt-live-chat-author-medal-renderer" id="medal-card">
                <div class="style-scope yt-live-chat-author-medal-renderer" id="medal-name">
                    <!-粉丝勋章名称-->
                </div>
                <div class="style-scope yt-live-chat-author-medal-renderer" id="medal-level" >
                    <!-粉丝勋章等级-->
                </div>
            </div>
        `;
        return badge;
    }
    // 创建舰长徽章
    createMemberBadge() {
        // 创建舰长徽章
        const badge = document.createElement('yt-live-chat-author-badge-renderer');
        badge.className = 'style-scope yt-live-chat-author-chip';
        badge.setAttribute('type', 'member');

        badge.innerHTML = `
            <div class="el-tooltip style-scope yt-live-chat-author-badge-renderer" id="image" tabindex="0">
                <img class="style-scope yt-live-chat-author-badge-renderer">
            </div>
        `;

        return badge;
    }
    // 创建房管徽章SVG
    createModeratorBadge() {
        // 创建房管徽章SVG
        const badge = document.createElement('yt-live-chat-author-badge-renderer');
        badge.className = 'style-scope yt-live-chat-author-chip';
        badge.setAttribute('type', 'moderator');

        // SVG代码
        badge.innerHTML = `
            <div class="el-tooltip style-scope yt-live-chat-author-badge-renderer" id="image" tabindex="0">
                <yt-icon class="style-scope yt-live-chat-author-badge-renderer">
                    <svg class="style-scope yt-icon" focusable="false" preserveAspectRatio="xMidYMid meet" style="pointer-events: none; display: block; width: 100%; height: 100%;" viewBox="0 0 16 16">
                        <g class="style-scope yt-icon">
                            <path class="style-scope yt-icon" d="M9.64589146,7.05569719 C9.83346524,6.562372 9.93617022,6.02722257 9.93617022,5.46808511 C9.93617022,3.00042984 7.93574038,1 5.46808511,1 C4.90894765,1 4.37379823,1.10270499 3.88047304,1.29027875 L6.95744681,4.36725249 L4.36725255,6.95744681 L1.29027875,3.88047305 C1.10270498,4.37379824 1,4.90894766 1,5.46808511 C1,7.93574038 3.00042984,9.93617022 5.46808511,9.93617022 C6.02722256,9.93617022 6.56237198,9.83346524 7.05569716,9.64589147 L12.4098057,15 L15,12.4098057 L9.64589146,7.05569719 Z"></path>
                        </g>
                    </svg>
                </yt-icon>
            </div>
        `;

        return badge;
    }

    //-----------------//
    // 模板创建方法
    createTextMessageTemplate() {
        const template = document.createElement('yt-live-chat-text-message-renderer');

        // 这里应该包含完整的HTML结构，简化示例
        template.innerHTML = `
            <div class="style-scope yt-live-chat-text-message-renderer" id="card">
                <div id="author-border" style="display: none;"></div>
                 <yt-img-shadow class="no-transition style-scope yt-live-chat-text-message-renderer" id="author-photo" loaded="">
                    <!--用户头像-->
                    <img alt="" class="style-scope yt-img-shadow" id="img">
                </yt-img-shadow>
                <div class="style-scope yt-live-chat-text-message-renderer" id="content">
                    <yt-live-chat-author-chip class="style-scope yt-live-chat-text-message-renderer" style="vertical-align: top;">
                        <span class="style-scope yt-live-chat-text-message-renderer" id="timestamp">
                            <!--发送时间-->
                        </span>
                        <span class="style-scope yt-live-chat-author-chip" dir="auto" id="author-name">
                            <span id="author-name-text">
                                <!--用户昵称-->
                            </span>
                            <span class="style-scope yt-live-chat-author-chip" id="chip-badges"></span>
                        </span>
                        <span class="style-scope yt-live-chat-author-chip" id="chat-medal">
                            <!--粉丝徽章-->
                        </span>
                        <span class="style-scope yt-live-chat-author-chip" id="chat-badges">
                            <!--舰长徽章-->
                        </span>
                    </yt-live-chat-author-chip>
                    <span class="style-scope yt-live-chat-text-message-renderer" id="image-and-message">
                        <span id="message" style="vertical-align: bottom;">
                            <!--弹幕消息-->
                        </span>
                        <div class="el-badge style-scope yt-live-chat-text-message-renderer">
                            <sup class="el-badge__content"></sup>
                        </div>
                    </span>
                    <div id="content-plus" style="display: none;"></div>
                </div>
            </div>
        `;

        return template;
    }
    // 付费消息的HTML结构
    createPaidMessageTemplate() {
        const template = document.createElement('yt-live-chat-paid-message-renderer');
        template.className = 'style-scope yt-live-chat-item-list-renderer style-scope yt-live-chat-item-list-renderer';

        // 付费消息的HTML结构
        template.innerHTML = `
            <div class="style-scope yt-live-chat-paid-message-renderer" id="card">
                <div class="style-scope yt-live-chat-paid-message-renderer" id="header">
                    <yt-img-shadow class="no-transition style-scope yt-live-chat-paid-message-renderer" height="40" id="author-photo" loaded="" style="background-color: transparent;" width="40">
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
    // 会员消息的HTML结构
    createMembershipMessageTemplate() {
        const template = document.createElement('yt-live-chat-membership-item-renderer');
        template.className = 'style-scope yt-live-chat-item-list-renderer style-scope yt-live-chat-item-list-renderer';

        // 会员消息的HTML结构
        template.innerHTML = `
            <div class="style-scope yt-live-chat-membership-item-renderer" id="card" style="background-color: ${this.defaultImages.membershipCardColor}">
                <div class="style-scope yt-live-chat-membership-item-renderer" id="header" style="background-color: ${this.defaultImages.membershipHeaderColor}">
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
    facePicture: 'https://static.hdslb.com/images/member/noface.gif',
    facePictureX: '40',  // 头像宽度px
    facePictureY: '40',  // 头像高度px
    fanMedalName: '粉丝勋章名称', // 粉丝勋章名称
    fanMedalLevel: '24', // 粉丝勋章等级
    fanMedalColorStart: '#3FB4F699', // 粉丝勋章开始颜色
    fanMedalColorEnd: '#3FB4F699', // 粉丝勋章结束颜色
    fanMedalColorBorder: '#3FB4F699', // 粉丝勋章边框颜色
    fanMedalColorText: '#FFFFFF', // 粉丝勋章文本色
    fanMedalColorLevel: '#3FB4F6E6', // 粉丝勋章等级颜色
    identityTitle: 'moderator',
    privilegeLevel: '0',
    fleetBadge: '',
    uName: '测试用户',
    sendTime: '14:11',
    messageData: [
        { type: 'text', text: '这是一条' },
        { type: 'emoji', alt: '[比心]', src: './blivechat_files/4e029593562283f00d39b99e0557878c4199c71d.png' },
        { type: 'text', text: '测试消息' }
    ],
});

// 创建普通消息
const faceMessage = chatBuilder.createTextMessage({
    facePicture: 'https://static.hdslb.com/images/member/noface.gif',
    facePictureX: '40',  // 头像宽度px
    facePictureY: '40',  // 头像高度px
    identityTitle: 'member',
    privilegeLevel: '1',
    fleetTitle: '总督',
    fleetBadge: './blivechat_files/guard-level-1.png',
    uName: '测试用户',
    sendTime: '14:11',
    messageData: [
        { type: 'image', alt: '[huangdou_xihuan]', src: './blivechat_files/huangdou_xihuan.png' }
    ],
});

// 创建普通消息
const moderatorMessage = chatBuilder.createTextMessage({
    facePicture: 'https://static.hdslb.com/images/member/noface.gif',
    facePictureX: '40',  // 头像宽度px
    facePictureY: '40',  // 头像高度px
    identityTitle: 'moderator',
    privilegeLevel: '1',
    fleetTitle: '总督',
    fleetBadge: './blivechat_files/guard-level-1.png',
    uName: '测试用户',
    sendTime: '14:11',
    messageData: "moderatorMessage",
});

// 创建付费消息
const paidMessage = chatBuilder.createPaidMessage({
    uName: '付费用户',
    price: '30.00',
    priceLevel: '30',
    sendTime: '14:11',
    messageData: '这是一条付费消息',
});

// 创建会员消息
const membershipMessage = chatBuilder.createMembershipMessage({
    uName: '新会员',
    identityTitle: 'owner',
    privilegeLevel: '2',
    fleetTitle: '提督',
    fleetBadge: './blivechat_files/guard-level-2.png',
    subtext: '新会员',
    sendTime: '14:11',
});

// 添加到DOM
itemContainer.appendChild(textMessage);
itemContainer.appendChild(faceMessage);
itemContainer.appendChild(paidMessage);
itemContainer.appendChild(membershipMessage);
itemContainer.appendChild(moderatorMessage);

scrollableContainer.scrollTop = scrollableContainer.scrollHeight;



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
                    messageData: '成功连接到弹幕服务器',
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
                        messageData: '解析消息错误',
                        timestamp: Date.now() / 1000
                    });
                }
            };

            this.socket.onclose = (event) => {
                console.log('WebSocket连接关闭:', event);
                this.addDanmuMessage({
                    type: 'system',
                    messageData: `连接已断开 (代码: ${event.code})`,
                    timestamp: Date.now() / 1000
                });
                this.handleReconnect();
            };

            this.socket.onerror = (error) => {
                console.error('WebSocket错误:', error);
                this.addDanmuMessage({
                    type: 'system',
                    messageData: '连接错误',
                    timestamp: Date.now() / 1000
                });
            };

        } catch (error) {
            console.error('创建连接错误:', error);
            this.addDanmuMessage({
                type: 'system',
                messageData: '创建连接错误',
                timestamp: Date.now() / 1000
            });
            this.handleReconnect();
        }
    }

    handleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            this.addDanmuMessage({
                type: 'system',
                messageData: `连接失败，已尝试 ${this.reconnectAttempts} 次`,
                timestamp: Date.now() / 1000
            });
            return;
        }

        this.reconnectAttempts++;
        const delay = Math.min(this.reconnectInterval * Math.pow(1.5, this.reconnectAttempts - 1), 60000); // 最大60秒

        this.addDanmuMessage({
            type: 'system',
            messageData: `连接断开，${Math.round(delay/1000)}秒后尝试重连 (${this.reconnectAttempts}/${this.maxReconnectAttempts})`,
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
//            case 'combo_gift':
//            case 'guard_buy':
//            case 'red_pocket':
//            case 'red_pocket_v2':
//            case 'user_toast':
//            case 'user_toast_v2':
//            case 'gift':
//                this.addGiftMessage(data);
//                break;

//            case 'super_chat':
//            case 'super_chat_jpn':
//                this.addSuperChatMessage(data);
//                break;

            case 'live_start':
            case 'interact':
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
            case 'live_start':
            case 'system':
                const sysMessageInfo = {
                    facePictureX: '40',  // 头像宽度px
                    facePictureY: '40',  // 头像高度px
                    authorType: 'moderator',
                    privilegeType: '0',
                    authorName: '系统消息',
                    sendTime: time,
                    messageData: data.messageData,
                    isAdmin: true,
                    lineBreakDisplay: true,
                }
                // 创建系统消息
                textMessage = chatBuilder.createTextMessage(sysMessageInfo);
                console.log('系统消息:', sysMessageInfo);
                break;
            case 'interact':
            case 'danmu':
                const danmuMessageInfo = {
                    uName: data.uName,
                    facePicture: data.facePicture,
                    facePictureX: data.facePictureX,
                    facePictureY: data.facePictureY,
                    uId: data.uId,
                    identityTitle: data.identityTitle,
                    privilegeLevel: data.privilegeLevel,
                    fleetTitle: data.fleetTitle,
                    fanMedalName: data.fanMedalName,
                    fanMedalLevel: data.fanMedalLevel,
                    fanMedalColorStart: data.fanMedalColorStart,
                    fanMedalColorEnd: data.fanMedalColorEnd,
                    fanMedalColorBorder: data.fanMedalColorBorder,
                    fanMedalColorText: data.fanMedalColorText,
                    fanMedalColorLevel: data.fanMedalColorLevel,
                    fanMedalTextSize: data.fanMedalTextSize,
                    fleetBadge: data.fleetBadge,
                    messageData: data.messageData,
                    messageTextSize: data.messageTextSize,
                    sendTime: time,
                    timeTextSize: data.timeTextSize,
                    isAdmin: data.isAdmin,
                    isFanGroup: data.isFanGroup,
                    lineBreakDisplay: data.lineBreakDisplay,
                }
                // 创建普通消息
                textMessage = chatBuilder.createTextMessage(danmuMessageInfo);
                console.log('消息:', danmuMessageInfo);
                break;
        }
        itemContainer.appendChild(textMessage);
        this.scrollToBottom();
    }

    // 礼物消息
    addGiftMessage(data) {
        const time = new Date(data.timestamp * 1000).toLocaleTimeString();
        let content = '';

        switch(data.type) {
            case 'gift':
                const price = (data.total_coin / 1000).toFixed(2);
                // 创建付费消息
                const paidMessage = chatBuilder.createPaidMessage({
                    authorName: '付费用户',
                    price: '30.00',
                    priceLevel: '30',
                    timestamp: '14:11',
                    messageData: data.gift_name + 'X' + data.gift_count,
                    offsetX: 150,
                    offsetY: 300
                });
                break;
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

