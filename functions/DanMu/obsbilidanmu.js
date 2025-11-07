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
            tickerMessage: 'CN¥39.00',
            facePicture: './blivechat_files/noface.gif',

            // 颜色配置
            messagePrimaryColor: 'rgb(29, 233, 182)',
            messageSecondaryColor: 'rgb(0, 191, 165)',

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
        this.element.style.width = "fit-content";
        this.element.tabIndex = 0;

        this.updateElement();
    }

    updateElement() {
        const gradientStyle = `linear-gradient(90deg, ${this.config.messagePrimaryColor}, ${this.config.messagePrimaryColor} ${this.currentPercentage}%, ${this.config.messageSecondaryColor} ${this.currentPercentage}%, ${this.config.messageSecondaryColor})`;

        this.element.innerHTML = `
            <div class="style-scope yt-live-chat-ticker-paid-message-item-renderer" dir="ltr" id="container"
                 style="background: ${gradientStyle};">
                <div class="style-scope yt-live-chat-ticker-paid-message-item-renderer" id="content" style="color: ${this.getTextColor()}; border: 3px solid ${this.config.messageSecondaryColor}; background: ${this.config.messagePrimaryColor} !important; border-radius: 50px !important; width: fit-content; padding: 0 0 0 5px;">
                    <yt-img-shadow class="no-transition style-scope yt-live-chat-ticker-paid-message-item-renderer" height="24" id="author-photo" loaded="" style="background-color: transparent;" width="24">
                        <img alt="" class="style-scope yt-img-shadow" height="24" id="img" src="${this.config.facePicture}" width="24">
                    </yt-img-shadow>
                    <span class="style-scope yt-live-chat-ticker-paid-message-item-renderer" dir="ltr"
                          id="text">${this.config.tickerMessage}</span>
                </div>
            </div>
        `;
    }

    getTextColor() {
        // 根据背景颜色亮度自动选择合适的文字颜色
        const primaryColor = this.config.messagePrimaryColor;
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
    messagePrimaryColor: 'rgb(29, 233, 182)',
    messageSecondaryColor: 'rgb(0, 191, 165)',
    tickerMessage: 'CN¥39.00',
    facePicture: './blivechat_files/noface.gif',
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
    messagePrimaryColor: 'rgb(29, 233, 182)',
    messageSecondaryColor: 'rgb(0, 191, 165)',
    tickerMessage: 'CN¥39.00',
    facePicture: './blivechat_files/noface.gif',
    countdownDuration: 8000, // 8秒
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
        this.TextMessageData = {
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
            isTimestampDisplay: false,

            ...data
        };

        const MainMessageWebPageElement = this.createTextMessageTemplate().cloneNode(true);
        MainMessageWebPageElement.setAttribute('author-type', this.TextMessageData.identityTitle);
        if (this.TextMessageData.isAdmin) MainMessageWebPageElement.setAttribute('is-admin', this.TextMessageData.isAdmin);
        if (this.TextMessageData.isFanGroup) MainMessageWebPageElement.setAttribute('is-fan-group', this.TextMessageData.isFanGroup);
        MainMessageWebPageElement.setAttribute('medal-level', this.TextMessageData.fanMedalLevel);
        MainMessageWebPageElement.setAttribute('privilegetype', this.TextMessageData.privilegeLevel);
        MainMessageWebPageElement.style.position = 'relative';
        MainMessageWebPageElement.style.setProperty('font-size', `${this.TextMessageData.messageTextSize}px`);  // 字体大小
        MainMessageWebPageElement.style.padding = '4px 24px';  // 上下间距 左右间距
        MainMessageWebPageElement.style.display = 'flex';
        MainMessageWebPageElement.style.setProperty('flex-direction', 'row');
        MainMessageWebPageElement.style.setProperty('align-items', 'flex-start');

        const cardElement = MainMessageWebPageElement.querySelector('#card');
        cardElement.style.display = 'flex';
        cardElement.style.setProperty('flex-direction', 'row !important');
        cardElement.style.setProperty('align-items', 'flex-start');
        cardElement.style.setProperty('width', '100%');

        // 头像父元素
        const authorPhotoElement = MainMessageWebPageElement.querySelector('#author-photo');
        authorPhotoElement.height = `${this.TextMessageData.facePictureY}`;
        authorPhotoElement.width = `${this.TextMessageData.facePictureX}`;
        authorPhotoElement.style.setProperty('background-color', 'transparent');
        authorPhotoElement.style.setProperty('overflow', 'visible');

        // 头像
        const imgElement = MainMessageWebPageElement.querySelector('#img');
        imgElement.height = `${this.TextMessageData.facePictureY}`;
        imgElement.width = `${this.TextMessageData.facePictureX}`;
        imgElement.src = `${this.TextMessageData.facePicture}`;
        imgElement.alt = `${this.TextMessageData.uId}`;
        imgElement.style.setProperty('background-color', 'transparent');

        if (this.TextMessageData.lineBreakDisplay) {
            const contentElement = MainMessageWebPageElement.querySelector('#content');
            contentElement.style.display = 'flex';
            contentElement.style.setProperty('flex-direction', 'column');
            contentElement.style.setProperty('align-items', 'flex-start');
        }

        // 时间戳
        const timestamp = MainMessageWebPageElement.querySelector('#timestamp');
        timestamp.textContent = data.sendTime || '00:00';
        timestamp.style.setProperty('font-size', `${this.TextMessageData.timeTextSize}px`);  // 字体大小
        if (this.TextMessageData.isTimestampDisplay) {
            timestamp.style.display = "inline";
        } else {
            timestamp.style.display = "none";
        }

        const authorNameElement = MainMessageWebPageElement.querySelector('#author-name');
        authorNameElement.setAttribute('type', this.TextMessageData.identityTitle);

        // 用户名称
        const authorNameText = MainMessageWebPageElement.querySelector('#author-name-text');
        authorNameText.textContent = data.uName || '用户';

        const imgMsg = MainMessageWebPageElement.querySelector('#image-and-message');
        imgMsg.style.width = 'auto';
        imgMsg.style.height = 'auto';


        const repeatedElement = MainMessageWebPageElement.querySelector('.el-badge.style-scope.yt-live-chat-text-message-renderer');
        repeatedElement.style.setProperty('--repeated-mark-color', 'hsl(210, 100%, 62.5%)');
        repeatedElement.style.display = 'none';

        // 消息内容
        const messageContent = MainMessageWebPageElement.querySelector('#message');
        this.buildMessageContent(messageContent, data.messageData);

        // 徽章
        this.updateBadges(MainMessageWebPageElement, this.TextMessageData);

        return MainMessageWebPageElement;
    }

    // 创建付费消息
    createPaidMessage(data) {
        // 先初始化默认图片配置
        this.paidMessageData = {
            uName: '', // 昵称
            uId: '',
            facePicture: 'https://static.hdslb.com/images/member/noface.gif', // 头像位置
            facePictureX: '40',  // 头像宽度px
            facePictureY: '40',  // 头像高度px
            sendTime: '00:00', // 时间
            price: '0', // 显示金额（元）
            priceLevel: '0',  // 金额等级
            messagePrimaryColor: 'rgba(29,233,182,1)', // 文字区域颜色
            messageSecondaryColor: 'rgba(0,191,165,1)', // 头像昵称金额区域颜色
            messageData: '', // 文字内容
            showOnlyHeader: false, // 是否不显示文字区域

            ...data
        };

        const PaidMessageWebPageElement = this.createPaidMessageTemplate().cloneNode(true);
        PaidMessageWebPageElement.setAttribute('price', data.price);
        PaidMessageWebPageElement.setAttribute('price-level', data.priceLevel);
        PaidMessageWebPageElement.style.setProperty('--yt-live-chat-paid-message-primary-color', this.paidMessageData.messagePrimaryColor);
        PaidMessageWebPageElement.style.setProperty('--yt-live-chat-paid-message-secondary-color', this.paidMessageData.messageSecondaryColor);
        if (this.paidMessageData.showOnlyHeader) PaidMessageWebPageElement.setAttribute('show-only-header', true);

        const authorPhotoElement = PaidMessageWebPageElement.querySelector('#author-photo');
        authorPhotoElement.height = this.paidMessageData.facePictureY;
        authorPhotoElement.width = this.paidMessageData.facePictureX;
        authorPhotoElement.loaded = "";
        authorPhotoElement.style.setProperty('background-color', 'transparent');

        const img = PaidMessageWebPageElement.querySelector('#img');
        img.height = "40";
        img.width = "40";
        img.alt = this.paidMessageData.uId
        img.src = this.paidMessageData.facePicture

        const authorName = PaidMessageWebPageElement.querySelector('#author-name');
        if (authorName) authorName.textContent = this.paidMessageData.uName;

        const purchaseAmount = PaidMessageWebPageElement.querySelector('#purchase-amount');
        if (purchaseAmount) purchaseAmount.textContent = `CN¥${this.paidMessageData.price}`;

        const timestamp = PaidMessageWebPageElement.querySelector('#timestamp');
        if (timestamp) timestamp.textContent = this.paidMessageData.sendTime || '00:00';

        const messageContent = PaidMessageWebPageElement.querySelector('#message');
        if (messageContent) messageContent.textContent = this.paidMessageData.messageData;

        const contentContent = PaidMessageWebPageElement.querySelector('#content');
        if (this.paidMessageData.showOnlyHeader) {
            if (contentContent) contentContent.style.visibility = 'hidden';
            if (contentContent) contentContent.style.display = 'none';
            if (contentContent) contentContent.style.padding = '0';
        };
        return PaidMessageWebPageElement;
    }

    // 创建会员加入消息
    createMembershipMessage(data) {
        // 先初始化默认图片配置
        this.membershipMessageData = {
            uName: '', // 昵称
            uId: '', // id
            facePicture: 'https://static.hdslb.com/images/member/noface.gif',  // 头像
            facePictureX: '40',  // 头像宽度px
            facePictureY: '40',  // 头像高度px
            sendTime: '00:00', // 时间
            messageData: '', // 文字内容
            fleetBadge: '',  // 舰队徽章
            membershipHeaderColor: "#820f9d",  // 背景颜色
            identityTitle: '', // 身份头衔：管理员 moderator，船员 member，主播 owner，普通为空
            privilegeLevel: '0', // 特权级别 1,2,3,0
            fleetTitle: '',  // 舰队称号

            ...data
        };

        const membershipMessageWebPageElement = this.createMembershipMessageTemplate().cloneNode(true);
        membershipMessageWebPageElement.setAttribute('privilegetype', this.membershipMessageData.privilegeLevel || '0');
        membershipMessageWebPageElement.setAttribute('show-only-header', "");
        membershipMessageWebPageElement.style.setProperty('--yt-live-chat-sponsor-color', this.membershipMessageData.membershipHeaderColor);

        const card = membershipMessageWebPageElement.querySelector('#card');
        card.style.setProperty('background-color', this.membershipMessageData.membershipCardColor);

        const authorPhoto = membershipMessageWebPageElement.querySelector('#author-photo');
        authorPhoto.height = this.membershipMessageData.facePictureY;
        authorPhoto.width = this.membershipMessageData.facePictureX;
        authorPhoto.style.setProperty('background-color', 'transparent');
        authorPhoto.loaded = '';

        const img = membershipMessageWebPageElement.querySelector('#img');
        img.height = this.membershipMessageData.facePictureY;
        img.width = this.membershipMessageData.facePictureX;
        img.alt = this.membershipMessageData.uId;
        img.src = this.membershipMessageData.facePicture;

        const authorName = membershipMessageWebPageElement.querySelector('#author-name');
        if (authorName) authorName.textContent = this.membershipMessageData.uName;

        const headerSubtext = membershipMessageWebPageElement.querySelector('#header-subtext');
        if (headerSubtext) headerSubtext.textContent = this.membershipMessageData.messageData || '新会员';

        const timestamp = membershipMessageWebPageElement.querySelector('#timestamp');
        if (timestamp) timestamp.textContent = this.membershipMessageData.sendTime || '00:00';

        this.updateBadges(membershipMessageWebPageElement, this.membershipMessageData);

        return membershipMessageWebPageElement;
    }
    //-----------------//
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
                    div.style.height = "auto"; // `${parseInt(item.height) * parseInt(div.style.width) / parseInt(item.width)}px`;
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
    updateBadges(element, data) {
        const medalContainer = element.querySelector('#chat-medal');
        if (!medalContainer) {
        } else {
            medalContainer.style.setProperty('font-size', `${data.fanMedalTextSize}px`);  // 字体大小
            medalContainer.innerHTML = '';
        }

        // 粉丝徽章
        if (data.isFanGroup) {
            const badge = this.createMedal();
            badge.setAttribute('is-fan-group', `${data.isFanGroup}`);
            badge.setAttribute('medal-name', `${data.fanMedalName}`);
            badge.setAttribute('medal-nevel', `${data.fanMedalLevel}`);
            badge.style.setProperty('--yt-live-chat-medal-background-color', `linear-gradient(to right, ${data.fanMedalColorStart}, ${data.fanMedalColorEnd})`);
            badge.style.setProperty('--yt-live-chat-medal-border-color', data.fanMedalColorBorder);
            badge.style.setProperty('--yt-live-chat-medal-text-color', data.fanMedalColorLevel); // 粉丝勋章等级颜色
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
            clsMedalRenderer.style.setProperty('font-size', `${data.timeTextSize}px`);
            clsMedalRenderer.style.setProperty('line-height', '14px');

            const medalName = badge.querySelector('#medal-name');
            medalName.style.setProperty('text-shadow', 'none');
            medalName.style.padding = '2px 4px';  // 上下间距 左右间距
            medalName.style.color = data.fanMedalColorText;
            medalName.textContent = data.fanMedalName;

            const medalLevel = badge.querySelector('#medal-level');
            medalLevel.style.padding = '2px 4px';  // 上下间距 左右间距
            medalLevel.style.setProperty('font-weight', '700');
            medalLevel.style.setProperty('text-shadow', 'none');
            medalLevel.style.setProperty('text-align', 'center');
            medalLevel.style.setProperty('background-color', '#FFFFFF');
            medalLevel.style.color = 'var(--yt-live-chat-medal-text-color,#222)';
            medalLevel.style.setProperty('border-top-right-radius', '2px');
            medalLevel.style.setProperty('border-bottom-right-radius', '2px');
            medalLevel.textContent = data.fanMedalLevel;

            medalContainer.appendChild(badge);
        }

        const badgesContainer = element.querySelector('#chat-badges');
        if (!badgesContainer) {
        } else {
            badgesContainer.innerHTML = '';
        }

        // 舰长徽章
        if (data.privilegeLevel && data.privilegeLevel !== '0') {
            const badge = this.createMemberBadge();
            const img = badge.querySelector('img');
            img.alt = data.fleetTitle;
            img.src = data.fleetBadge;
            badgesContainer.appendChild(badge);
        }

        // 房管徽章
        if (data.isAdmin) {
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
                            <!--房管徽章-->
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
                <div class="joi-style" id="paw" style="display: none;"></div>
                <div class="joi-style" id="star" style="display: none;"></div>
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
                    <yt-img-shadow class="no-transition style-scope yt-live-chat-paid-message-renderer" id="author-photo">
                        <img class="style-scope yt-img-shadow" id="img">
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
            <div class="style-scope yt-live-chat-membership-item-renderer" id="card">
                <div class="style-scope yt-live-chat-membership-item-renderer" id="header">
                    <div id="author-border" style="display: none;"></div>
                    <yt-img-shadow class="no-transition style-scope yt-live-chat-membership-item-renderer" id="author-photo">
                        <img id="img" class="style-scope yt-img-shadow">
                    </yt-img-shadow>
                    <div class="style-scope yt-live-chat-membership-item-renderer" id="header-content">
                        <div class="style-scope yt-live-chat-membership-item-renderer" id="header-content-primary-column">
                            <div class="style-scope yt-live-chat-membership-item-renderer" id="header-content-inner-column">
                                <yt-live-chat-author-chip class="style-scope yt-live-chat-membership-item-renderer">
                                    <span class="member style-scope yt-live-chat-author-chip" dir="auto" id="author-name">
                                        <!--用户昵称-->
                                        <span id="chip-badges" class="style-scope yt-live-chat-author-chip"></span>
                                    </span>
                                    <span class="style-scope yt-live-chat-author-chip" id="chat-badges">
                                        <!--舰长徽章-->
                                        <!--房管徽章-->
                                    </span>
                                </yt-live-chat-author-chip>
                            </div>
                            <div class="style-scope yt-live-chat-membership-item-renderer" id="header-subtext">
                                <!--内容-->
                            </div>
                        </div>
                        <div class="style-scope yt-live-chat-membership-item-renderer" id="timestamp">
                            <!--时间-->
                        </div>
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

// 使用示例 = ============================================================================================================
const chatBuilder = new YouTubeChatMessageBuilder();

// 创建普通消息 粉丝勋章 舰长 管理员 换行 时间
const ordinaryMessage = chatBuilder.createTextMessage({
    uName: '测试用户',
    uId: '0',
    facePicture: 'https://static.hdslb.com/images/member/noface.gif',
    facePictureX: '40',  // 头像宽度px
    facePictureY: '50',  // 头像高度px
    identityTitle: 'moderator',
    privilegeLevel: '1',
    fanMedalName: '粉丝勋章', // 粉丝勋章名称
    fanMedalLevel: '24', // 粉丝勋章等级
    fanMedalColorStart: '#3FB4F699', // 粉丝勋章开始颜色
    fanMedalColorEnd: '#3FB4F699', // 粉丝勋章结束颜色
    fanMedalColorBorder: '#3FB4F699', // 粉丝勋章边框颜色
    fanMedalColorText: '#FFFFFF', // 粉丝勋章文本色
    fanMedalColorLevel: '#3FB4F6E6', // 粉丝勋章等级颜色
    fanMedalTextSize: '20',
    fleetBadge: 'https://blc.huixinghao.cn/static/img/icons/guard-level-1.png',
    messageData: [
        {type: 'text', color: '#1565c0', text: '@用户  '},
        { type: 'text', text: '这是一条测试消息' },
        { type: 'emoji', alt: '[比心]', src: 'https://static.hdslb.com/images/member/noface.gif' },
        {type: 'image',alt: '[比心]',width: '16px',height: '16px', src: 'https://static.hdslb.com/images/member/noface.gif'},
        {type: 'image',alt: '[比心]',width: '16px',height: '16px', src: 'https://static.hdslb.com/images/member/noface.gif'},
        { type: 'text', text: '测试消息' }
    ],
    messageTextSize: '40',
    sendTime: '00:00',
    timeTextSize: '10',
    isAdmin: true,  // 是否管理员
    isFanGroup: true, // 是否有粉丝勋章或者是否有本直播间的粉丝勋章
    lineBreakDisplay: true,
    isTimestampDisplay: true,
});

// 创建付费消息
const paidMessage = chatBuilder.createPaidMessage({
    uName: '付费用户', // 昵称
    uId: '0',
    facePicture: 'https://static.hdslb.com/images/member/noface.gif', // 头像位置
    facePictureX: '40',  // 头像宽度px
    facePictureY: '40',  // 头像高度px
    sendTime: '14:11', // 时间
    price: '30.00', // 显示金额（元）
    priceLevel: '30',  // 金额等级
    messagePrimaryColor: 'rgba(29,233,182,1)', // 文字区域颜色
    messageSecondaryColor: 'rgba(0,191,165,1)', // 头像昵称金额区域颜色
    messageData: '这是一条付费消息', // 文字内容
    showOnlyHeader: false, // 是否不显示文字区域
});

// 创建会员消息
const membershipMessage = chatBuilder.createMembershipMessage({
    uName: '新舰长用户名', // 昵称
    uId: '0', // id
    facePicture: 'https://static.hdslb.com/images/member/noface.gif',  // 头像
    facePictureX: '40',  // 头像宽度px
    facePictureY: '40',  // 头像高度px
    sendTime: '14:11', // 时间
    messageData: '提督上任', // 文字内容
    fleetBadge: 'https://blc.huixinghao.cn/static/img/icons/guard-level-2.png',  // 舰队徽章
    membershipHeaderColor: "#820f9d",  // 上层颜色
    identityTitle: 'owner', // 身份头衔：管理员 moderator，船员 member，主播 owner，普通为空
    privilegeLevel: '2', // 特权级别 1,2,3,0
    fleetTitle: '提督',  // 舰队称号
});

// 添加到DOM
itemContainer.appendChild(ordinaryMessage);
itemContainer.appendChild(paidMessage);
itemContainer.appendChild(membershipMessage);

scrollableContainer.scrollTop = scrollableContainer.scrollHeight;



class DanmuWebSocketClient {
    constructor() {
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.reconnectInterval = 3000; // 3秒
        this.reconnectTimer = null;
        this.maxMessages = 200; // 默认最大保留消息数

        // 页面加载后自动连接
        setTimeout(() => {
            this.connect();
        }, 1000);
    }

    // 添加清理函数
    cleanupOldMessages(maxCount = null) {
        if (maxCount !== null) {
            this.maxMessages = maxCount;
        }

        const currentMessageCount = itemContainer.children.length;

        if (currentMessageCount > this.maxMessages) {
            const messagesToRemove = currentMessageCount - this.maxMessages;

            // 移除最旧的消息（前面的消息）
            for (let i = 0; i < messagesToRemove; i++) {
                if (itemContainer.firstChild) {
                    itemContainer.removeChild(itemContainer.firstChild);
                }
            }

            console.log(`清理了 ${messagesToRemove} 条旧消息，当前保留 ${this.maxMessages} 条消息`);
        }
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
            case 'cleanup': // 添加清理消息类型
                this.cleanupOldMessages(data.maxCount);
                break;

            case 'user_toast_v2':
                this.addMembershipMessage(data);
                break;

            case 'gift':
            case 'red_pocket_v2':
            case 'super_chat':
            case 'super_chat_jpn':
                this.addGiftMessage(data);
                break;

            case 'red_pocket_winners':
            case 'live_start':
            case 'interact':
            case 'danmu':
            case 'system':
                this.addDanmuMessage(data);
                // 每次添加新消息后检查是否超过限制
                if (itemContainer.children.length > this.maxMessages * 1.2) {
                    this.cleanupOldMessages();
                }
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
            case 'red_pocket_winners':
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
                    isTimestampDisplay: data.isTimestampDisplay,
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

        switch(data.type) {
            case 'super_chat':
            case 'super_chat_jpn':
            case 'red_pocket_v2':
            case 'gift':
                const giftMessageInfo = {
                    uName: data.uName, // 昵称
                    uId: data.uId,
                    facePicture: data.facePicture, // 头像位置
                    facePictureX: data.facePictureX,  // 头像宽度px
                    facePictureY: data.facePictureY,  // 头像高度px
                    sendTime: time, // 时间
                    price: data.price, // 显示金额（元）
                    priceLevel: data.priceLevel,  // 金额等级
                    messagePrimaryColor: data.messagePrimaryColor, // 文字区域颜色
                    messageSecondaryColor: data.messageSecondaryColor, // 头像昵称金额区域颜色
                    messageData: data.messageData, // 文字内容
                    tickerMessage: `CN¥${data.price}`,
                    showOnlyHeader: data.showOnlyHeader, // 是否不显示文字区域
                    countdownDuration: 20000, // 毫秒
                }
                console.log('礼物消息:', giftMessageInfo);
                // 创建付费消息
                itemContainer.appendChild(chatBuilder.createPaidMessage(giftMessageInfo));
                tickerContainer.appendChild(manager.createTicker(giftMessageInfo).getElement());
                break;
        }
        this.scrollToBottom();
    }

    // 舰长消息
    addMembershipMessage(data) {
        const time = new Date(data.timestamp * 1000).toLocaleTimeString();
        let membershipMessage

        switch(data.type) {
            case 'user_toast_v2':
                const membershipMessageInfo = {
                    uName: data.uName,
                    uId: data.uId,
                    facePicture: data.facePicture,
                    facePictureX: data.facePictureX,
                    facePictureY: data.facePictureY,
                    sendTime: time,
                    messageData: data.messageData,
                    fleetBadge: data.fleetBadge,
                    membershipHeaderColor: data.membershipHeaderColor,
                    identityTitle: data.identityTitle,
                    privilegeLevel: data.privilegeLevel,
                    fleetTitle: data.fleetTitle,
                }
                // 创建付费消息
                membershipMessage = chatBuilder.createMembershipMessage(membershipMessageInfo);
                console.log('舰长消息:', membershipMessageInfo);
                break;
        }
        itemContainer.appendChild(membershipMessage);
        this.scrollToBottom();
    }

    scrollToBottom() {
        scrollableContainer.scrollTop = scrollableContainer.scrollHeight;
    }
}

// 初始化客户端
document.addEventListener('DOMContentLoaded', () => {
    new DanmuWebSocketClient();
});

