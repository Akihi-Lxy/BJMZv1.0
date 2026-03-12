// ========== DOM加载完成后执行 ==========
document.addEventListener('DOMContentLoaded', function() {
    initBannerSlider();
    initNavigation();
    initScrollEffects();
    initContactForm();
    initBackToTop();
});

// ========== Banner轮播 ==========
function initBannerSlider() {
    const slides = document.querySelectorAll('.banner-slide');
    const dots = document.querySelectorAll('.banner-dots .dot');
    const prevBtn = document.querySelector('.banner-arrows .prev');
    const nextBtn = document.querySelector('.banner-arrows .next');
    let currentIndex = 0;
    let autoSlideInterval;

    // 显示指定幻灯片
    function showSlide(index) {
        // 处理边界
        if (index >= slides.length) index = 0;
        if (index < 0) index = slides.length - 1;

        // 移除所有active状态
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));

        // 添加当前active状态
        slides[index].classList.add('active');
        dots[index].classList.add('active');

        currentIndex = index;
    }

    // 下一张
    function nextSlide() {
        showSlide(currentIndex + 1);
    }

    // 上一张
    function prevSlide() {
        showSlide(currentIndex - 1);
    }

    // 开始自动播放
    function startAutoSlide() {
        autoSlideInterval = setInterval(nextSlide, 5000);
    }

    // 停止自动播放
    function stopAutoSlide() {
        clearInterval(autoSlideInterval);
    }

    // 绑定事件
    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            stopAutoSlide();
            prevSlide();
            startAutoSlide();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            stopAutoSlide();
            nextSlide();
            startAutoSlide();
        });
    }

    // 点击指示器
    dots.forEach((dot, index) => {
        dot.addEventListener('click', function() {
            stopAutoSlide();
            showSlide(index);
            startAutoSlide();
        });
    });

    // 启动自动播放
    startAutoSlide();

    // 鼠标悬停时暂停
    const banner = document.querySelector('.banner');
    if (banner) {
        banner.addEventListener('mouseenter', stopAutoSlide);
        banner.addEventListener('mouseleave', startAutoSlide);
    }
}

// ========== 导航功能 ==========
function initNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-menu a');

    // 移动端菜单切换
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    // 点击导航链接关闭菜单
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');

            // 更新active状态
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // 滚动时更新导航高亮
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('section[id]');
        const scrollPos = window.scrollY + 100;

        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');

            if (scrollPos >= top && scrollPos < top + height) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    });
}

// ========== 滚动效果 ==========
function initScrollEffects() {
    // 导航栏滚动效果
    const header = document.querySelector('.header');
    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.scrollY;

        if (currentScroll > 50) {
            header.style.boxShadow = '0 2px 30px rgba(0, 0, 0, 0.15)';
        } else {
            header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        }

        lastScroll = currentScroll;
    });

    // 元素入场动画
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // 观察需要动画的元素
    const animateElements = document.querySelectorAll('.product-card, .service-card, .contact-card, .info-item');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// ========== 联系表单 ==========
function initContactForm() {
    const form = document.getElementById('contactForm');

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // 获取表单数据
            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });

            // 简单验证
            if (!data.name || !data.phone || !data.message) {
                alert('请填写完整信息！');
                return;
            }

            // 验证手机号
            const phoneRegex = /^1[3-9]\d{9}$/;
            if (!phoneRegex.test(data.phone)) {
                alert('请输入正确的手机号码！');
                return;
            }

            // 模拟提交
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = '提交中...';
            submitBtn.disabled = true;

            setTimeout(function() {
                alert('感谢您的留言，我们会尽快与您联系！');
                form.reset();
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 1500);
        });
    }
}

// ========== 返回顶部 ==========
function initBackToTop() {
    const backToTop = document.querySelector('.back-to-top');

    if (backToTop) {
        // 滚动显示/隐藏
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTop.classList.add('show');
            } else {
                backToTop.classList.remove('show');
            }
        });

        // 点击返回顶部
        backToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// ========== 平滑滚动 ==========
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);

        if (targetElement) {
            const headerHeight = document.querySelector('.header').offsetHeight;
            const targetPosition = targetElement.offsetTop - headerHeight;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ========== 图片懒加载 ==========
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// ========== 数字动画 ==========
function animateNumbers() {
    const numbers = document.querySelectorAll('.number-animate');

    numbers.forEach(num => {
        const target = parseInt(num.getAttribute('data-target'));
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const updateNumber = () => {
            current += step;
            if (current < target) {
                num.textContent = Math.floor(current);
                requestAnimationFrame(updateNumber);
            } else {
                num.textContent = target;
            }
        };

        updateNumber();
    });
}

// ========== 控制台欢迎信息 ==========
console.log('%c欢迎访问北京梦织家居有限公司官网！', 'color: #667eea; font-size: 20px; font-weight: bold;');
console.log('%cBeijing Mengzhi Home Co.,Ltd.', 'color: #764ba2; font-size: 14px;');
console.log('%c专业高端毛巾制造商 | OEM/ODM服务', 'color: #333; font-size: 12px;');
