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
            onRemove: null,
            onUpdate: null,

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

    // 预设模板方法
    static createSmallAmount(amount, duration = 10000) {
        return new PaidMessageTicker({
            width: '106px',
            primaryColor: 'rgb(29, 233, 182)',
            secondaryColor: 'rgb(0, 191, 165)',
            text: `CN¥${amount}`,
            countdownDuration: duration
        });
    }

    static createMediumAmount(amount, duration = 10000) {
        return new PaidMessageTicker({
            width: '94px',
            primaryColor: 'rgb(233, 30, 99)',
            secondaryColor: 'rgb(194, 24, 91)',
            text: `CN¥${amount}`,
            countdownDuration: duration
        });
    }

    static createLargeAmount(amount, duration = 10000) {
        return new PaidMessageTicker({
            width: '106px',
            primaryColor: 'rgb(230, 33, 23)',
            secondaryColor: 'rgb(208, 0, 0)',
            text: `CN¥${amount}`,
            countdownDuration: duration
        });
    }

    static createMembership(duration = 10000) {
        return new PaidMessageTicker({
            width: '72px',
            primaryColor: 'rgb(15, 157, 88)',
            secondaryColor: 'rgb(11, 128, 67)',
            text: '会员',
            countdownDuration: duration
        });
    }

    static createOrangeAmount(amount, duration = 10000) {
        return new PaidMessageTicker({
            width: '94px',
            primaryColor: 'rgb(245, 124, 0)',
            secondaryColor: 'rgb(230, 81, 0)',
            text: `CN¥${amount}`,
            countdownDuration: duration
        });
    }

    static createYellowAmount(amount, duration = 10000) {
        return new PaidMessageTicker({
            width: '106px',
            primaryColor: 'rgb(255, 202, 40)',
            secondaryColor: 'rgb(255, 179, 0)',
            text: `CN¥${amount}`,
            countdownDuration: duration
        });
    }
}

// 管理器类，用于管理多个付费消息
class PaidMessageTickerManager {
    constructor() {
        this.tickers = new Set();
        this.itemsContainer = document.querySelector('.style-scope.yt-live-chat-ticker-renderer#items');
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
        this.itemsContainer.appendChild(ticker.getElement());
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

// 初始化管理器
const manager = new PaidMessageTickerManager();

// 添加事件监听器
document.getElementById('add-small').addEventListener('click', () => {
    manager.createTicker({
        width: '106px',
        primaryColor: 'rgb(29, 233, 182)',
        secondaryColor: 'rgb(0, 191, 165)',
        text: 'CN¥39.00',
        countdownDuration: 8000
    });
});

document.getElementById('add-medium').addEventListener('click', () => {
    manager.createTicker({
        width: '94px',
        primaryColor: 'rgb(233, 30, 99)',
        secondaryColor: 'rgb(194, 24, 91)',
        text: 'CN¥500',
        countdownDuration: 10000
    });
});

document.getElementById('add-large').addEventListener('click', () => {
    manager.createTicker({
        width: '106px',
        primaryColor: 'rgb(230, 33, 23)',
        secondaryColor: 'rgb(208, 0, 0)',
        text: 'CN¥1,000',
        countdownDuration: 12000
    });
});

document.getElementById('add-membership').addEventListener('click', () => {
    manager.createTicker({
        width: '72px',
        primaryColor: 'rgb(15, 157, 88)',
        secondaryColor: 'rgb(11, 128, 67)',
        text: '会员',
        countdownDuration: 15000
    });
});

document.getElementById('add-orange').addEventListener('click', () => {
    manager.createTicker({
        width: '94px',
        primaryColor: 'rgb(245, 124, 0)',
        secondaryColor: 'rgb(230, 81, 0)',
        text: 'CN¥200',
        countdownDuration: 9000
    });
});

document.getElementById('add-yellow').addEventListener('click', () => {
    manager.createTicker({
        width: '106px',
        primaryColor: 'rgb(255, 202, 40)',
        secondaryColor: 'rgb(255, 179, 0)',
        text: 'CN¥50.00',
        countdownDuration: 7000
    });
});

document.getElementById('add-random').addEventListener('click', () => {
    const types = [
        () => manager.createTicker({
            width: '106px',
            primaryColor: 'rgb(29, 233, 182)',
            secondaryColor: 'rgb(0, 191, 165)',
            text: 'CN¥39.00',
            countdownDuration: 8000
        }),
        () => manager.createTicker({
            width: '94px',
            primaryColor: 'rgb(233, 30, 99)',
            secondaryColor: 'rgb(194, 24, 91)',
            text: 'CN¥500',
            countdownDuration: 10000
        }),
        () => manager.createTicker({
            width: '106px',
            primaryColor: 'rgb(230, 33, 23)',
            secondaryColor: 'rgb(208, 0, 0)',
            text: 'CN¥1,000',
            countdownDuration: 12000
        }),
        () => manager.createTicker({
            width: '72px',
            primaryColor: 'rgb(15, 157, 88)',
            secondaryColor: 'rgb(11, 128, 67)',
            text: '会员',
            countdownDuration: 15000
        })
    ];

    const randomType = types[Math.floor(Math.random() * types.length)];
    randomType();
});

document.getElementById('clear-all').addEventListener('click', () => {
    manager.removeAll();
});

// 初始添加一些示例消息
setTimeout(() => {
    manager.createTicker({
        width: '106px',
        primaryColor: 'rgb(29, 233, 182)',
        secondaryColor: 'rgb(0, 191, 165)',
        text: 'CN¥39.00',
        countdownDuration: 8000
    });
}, 500);

setTimeout(() => {
    manager.createTicker({
        width: '94px',
        primaryColor: 'rgb(233, 30, 99)',
        secondaryColor: 'rgb(194, 24, 91)',
        text: 'CN¥500',
        countdownDuration: 10000
    });
}, 1500);

setTimeout(() => {
    manager.createTicker({
        width: '106px',
        primaryColor: 'rgb(230, 33, 23)',
        secondaryColor: 'rgb(208, 0, 0)',
        text: 'CN¥1,000',
        countdownDuration: 12000
    });
}, 2500);
