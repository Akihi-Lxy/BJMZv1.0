"""
北京梦织家居有限公司官网后端服务器
Beijing Mengzhi Home Co.,Ltd. Official Website Backend Server
"""

from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from functools import wraps

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 配置
app.secret_key = 'mengzhi-home-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# 管理员账号
ADMIN_CREDENTIALS = {
    'username': 'zhangmengke',
    'password': '123456'
}

# 数据文件路径
DATA_DIR = 'data'
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')
SITE_IMAGES_FILE = os.path.join(DATA_DIR, 'site-images.json')
SITE_CONTENT_FILE = os.path.join(DATA_DIR, 'site-content.json')
MESSAGES_FILE = os.path.join(DATA_DIR, 'messages.json')

# 确保目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# 初始化产品数据
if not os.path.exists(PRODUCTS_FILE):
    default_products = [
        {
            'id': 1,
            'name': 'Premium Towel Series',
            'description': 'Premium quality materials, soft and comfortable',
            'image': 'images/cf03.jpg',
            'createTime': datetime.now().isoformat()
        },
        {
            'id': 2,
            'name': 'Bath Towel Series',
            'description': 'Highly absorbent and durable',
            'image': 'images/cf03 (1).jpg',
            'createTime': datetime.now().isoformat()
        },
        {
            'id': 3,
            'name': 'Custom Towels',
            'description': 'OEM/ODM customization services available',
            'image': 'images/cf2.jpg',
            'createTime': datetime.now().isoformat()
        }
    ]
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_products, f, ensure_ascii=False, indent=2)

# 初始化网站图片配置
if not os.path.exists(SITE_IMAGES_FILE):
    default_site_images = {
        'logo': 'images/logo.png',
        'about_image': 'images/cf2.jpg',
        'banners': [
            {
                'id': 1,
                'title': 'Professional High-End Towel Manufacturer',
                'subtitle': 'Beijing Mengzhi Home Co.,Ltd.',
                'buttonText': 'View Products',
                'buttonLink': '#products',
                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'image': ''
            },
            {
                'id': 2,
                'title': 'OEM/ODM Customization Services',
                'subtitle': 'Printing, Embroidery, Labels, Packaging and More',
                'buttonText': 'Learn More',
                'buttonLink': '#services',
                'background': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                'image': ''
            },
            {
                'id': 3,
                'title': 'Quality Assurance & Integrity First',
                'subtitle': 'Free Samples · Fast Delivery · Excellent Service',
                'buttonText': 'Contact Us',
                'buttonLink': '#contact',
                'background': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                'image': ''
            }
        ]
    }
    with open(SITE_IMAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_site_images, f, ensure_ascii=False, indent=2)

# 初始化网站内容配置
if not os.path.exists(SITE_CONTENT_FILE):
    default_site_content = {
        # 导航栏
        'nav_home': 'Home',
        'nav_about': 'About Us',
        'nav_products': 'Products',
        'nav_services': 'Services',
        'nav_contact': 'Contact',
        
        # 关于我们区域
        'about_title': 'About Us',
        'about_company_name': 'Beijing Mengzhi Home Co.,Ltd.',
        'about_subtitle': 'Professional Towel Wholesaler',
        'about_para1': 'Beijing Mengzhi Home Co.,Ltd. mainly produces various high-end towels, bath towel series products. We can display your brand logo and customized patterns on towels through printing, embroidery, washing labels, and packaging.',
        'about_para2': 'We support OEM and ODM services, free samples, fast express delivery, visualized production processes, a comprehensive after-sales service system, and competitive prices.',
        'about_para3': 'Beijing Mengzhi Home Co.,Ltd. values credibility, abides by contracts, and ensures product quality, winning the trust of customers. The company fully follows customer needs, continuously innovates products and improves services. We look forward to a pleasant cooperation with you.',
        'about_business_type': 'Business Type',
        'about_business_value': 'Textile Wholesaler',
        'about_legal_rep': 'Legal Representative',
        'about_legal_value': 'Zhang Mengqiang',
        'about_credit_code': 'Credit Code',
        'about_credit_value': '91110112MADN22Q97H',
        
        # 产品展示区域
        'products_title': 'Our Products',
        'products_subtitle': 'High-quality towel series to meet your various needs',
        
        # 服务优势区域
        'services_title': 'Our Services',
        'service1_title': 'OEM/ODM Services',
        'service1_desc': 'Private label manufacturing and custom sample production to meet different customer needs',
        'service2_title': 'Free Samples',
        'service2_desc': 'Free samples provided so you can verify quality before placing orders',
        'service3_title': 'Fast Delivery',
        'service3_desc': 'Efficient logistics system ensures products reach customers quickly',
        'service4_title': 'Visual Production',
        'service4_desc': 'Transparent production process, track your order status anytime',
        'service5_title': 'After-Sales Support',
        'service5_desc': 'Professional after-sales team to solve any issues promptly',
        'service6_title': 'Competitive Pricing',
        'service6_desc': 'Competitive pricing system to create greater value for you',
        
        # 定制服务区域
        'custom_title': 'Customization Services',
        'custom_subtitle': 'Multiple customization options to make your brand unique',
        'custom_printing': 'Printing',
        'custom_embroidery': 'Embroidery',
        'custom_labels': 'Washing Labels',
        'custom_packaging': 'Packaging',
        
        # 联系我们区域
        'contact_title': 'Contact Us',
        'contact_subtitle': 'Looking forward to cooperating with you, feel free to contact us',
        'contact_address_label': 'Address',
        'contact_address_value': 'A650, 1F, No.47 Yuqiao North Lane, Tongzhou District, Beijing, China',
        'contact_phone_label': 'Phone',
        'contact_phone_value': '+86 17601607071',
        'contact_email_label': 'Email',
        'contact_email_value': '17601607071@163.com',
        'contact_legal_label': 'Legal Representative',
        'contact_legal_value': 'Zhang Mengqiang',
        'contact_form_name': 'Your Name',
        'contact_form_phone': 'Phone Number',
        'contact_form_email': 'Email Address',
        'contact_form_message': 'Your Message...',
        'contact_form_submit': 'Send Message',
        
        # 页脚
        'footer_company': 'Beijing Mengzhi Home Co.,Ltd.',
        'footer_tagline': 'Professional Towel Wholesaler',
        'footer_quick_links': 'Quick Links',
        'footer_contact_info': 'Contact Info',
        'footer_company_info': 'Company Info',
        'footer_credit_label': 'Credit Code',
        'footer_copyright': '© 2024 Beijing Mengzhi Home Co.,Ltd. All Rights Reserved',
        'footer_slogan': 'Credibility · Integrity · Quality',
        
        # 其他产品页
        'other_page_title': 'Other Product Series',
        'other_page_subtitle': 'Beijing Mengzhi Home · More Quality Products Coming Soon',
        'other_coming_title': 'New Products Coming Soon',
        'other_coming_desc': 'We are preparing more quality product series, including bedding, curtains, carpets and other home textiles. Stay tuned!',
        'other_notify_btn': 'Notify Me When Available',
        'other_upcoming_title': 'Upcoming Product Series',
        'other_cat1_name': 'Bedding Sets',
        'other_cat1_desc': 'Bedsheets, Duvet Covers, Pillowcases',
        'other_cat2_name': 'Curtain Series',
        'other_cat2_desc': 'Blackout Curtains, Decorative Curtains',
        'other_cat3_name': 'Carpets & Rugs',
        'other_cat3_desc': 'Living Room Rugs, Bathroom Mats',
        'other_cat4_name': 'Home Apparel',
        'other_cat4_desc': 'Bathrobes, Pajama Series',
        'other_back_link': 'Back to Products'
    }
    with open(SITE_CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_site_content, f, ensure_ascii=False, indent=2)


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_products():
    """加载产品数据"""
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []


def save_products(products):
    """保存产品数据"""
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)


def load_site_images():
    """加载网站图片配置"""
    try:
        with open(SITE_IMAGES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            'logo': 'images/logo.png',
            'about_image': 'images/cf2.jpg',
            'banners': []
        }


def save_site_images(images):
    """保存网站图片配置"""
    with open(SITE_IMAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(images, f, ensure_ascii=False, indent=2)


def load_site_content():
    """加载网站内容配置"""
    try:
        with open(SITE_CONTENT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}


def save_site_content(content):
    """保存网站内容配置"""
    with open(SITE_CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)


def load_messages():
    """加载留言数据"""
    try:
        with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []


def save_messages(messages):
    """保存留言数据"""
    try:
        # 确保data目录存在
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存留言失败: {e}")
        return False


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'success': False, 'message': '请先登录'}), 401
        return f(*args, **kwargs)
    return decorated_function


# ========== 静态文件路由 ==========

@app.route('/')
def index():
    """首页"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """静态文件服务"""
    # uploads 文件由专门的 serve_uploads 路由处理
    if filename.startswith('uploads/'):
        # 提取 uploads/ 后的文件名
        upload_filename = filename.replace('uploads/', '', 1)
        return send_from_directory(app.config['UPLOAD_FOLDER'], upload_filename)
    if filename.endswith('.html') or filename.endswith('.css') or filename.endswith('.js'):
        return send_from_directory('.', filename)
    return send_from_directory('.', filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    """图片文件服务"""
    return send_from_directory('images', filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    """CSS文件服务"""
    return send_from_directory('css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    """JS文件服务"""
    return send_from_directory('js', filename)

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    """上传文件服务"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ========== API 路由 ==========

@app.route('/api/login', methods=['POST'])
def login():
    """管理员登录"""
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
        session['logged_in'] = True
        session['username'] = username
        return jsonify({
            'success': True,
            'message': '登录成功',
            'username': username
        })
    else:
        return jsonify({
            'success': False,
            'message': '用户名或密码错误'
        }), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    """退出登录"""
    session.clear()
    return jsonify({
        'success': True,
        'message': '已退出登录'
    })


@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    """检查登录状态"""
    if session.get('logged_in'):
        return jsonify({
            'isLoggedIn': True,
            'username': session.get('username')
        })
    return jsonify({'isLoggedIn': False})


@app.route('/api/products', methods=['GET'])
def get_products():
    """获取产品列表"""
    products = load_products()
    return jsonify({
        'success': True,
        'products': products
    })


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """获取单个产品详情"""
    products = load_products()
    
    for product in products:
        if product['id'] == product_id:
            return jsonify({
                'success': True,
                'product': product
            })
    
    return jsonify({
        'success': False,
        'message': '产品不存在'
    }), 404


@app.route('/api/products', methods=['POST'])
@login_required
def add_product():
    """添加产品"""
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    
    if not name or not description:
        return jsonify({
            'success': False,
            'message': '请填写产品名称和描述'
        }), 400
    
    if 'image' not in request.files:
        return jsonify({
            'success': False,
            'message': '请上传产品图片'
        }), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({
            'success': False,
            'message': '请选择图片文件'
        }), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'message': '只支持 JPG、PNG、GIF、WEBP 格式的图片'
        }), 400
    
    # 保存图片
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f'product-{timestamp}-{filename}'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    
    # 添加产品
    products = load_products()
    new_product = {
        'id': int(datetime.now().timestamp() * 1000),
        'name': name,
        'description': description,
        'image': f'uploads/{unique_filename}',
        'images': [],  # 产品详情页多图
        'detail': request.form.get('detail', ''),  # 详细介绍
        'material': request.form.get('material', ''),  # 材质
        'size': request.form.get('size', ''),  # 尺寸
        'weight': request.form.get('weight', ''),  # 重量
        'moq': request.form.get('moq', ''),  # 起订量
        'highlights': json.loads(request.form.get('highlights', '[]')),  # 产品亮点
        'features': json.loads(request.form.get('features', '[]')),  # 产品特点
        'createTime': datetime.now().isoformat()
    }
    products.append(new_product)
    save_products(products)
    
    return jsonify({
        'success': True,
        'message': '产品添加成功',
        'product': new_product
    })


@app.route('/api/products/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    """更新产品"""
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    
    if not name or not description:
        return jsonify({
            'success': False,
            'message': '请填写产品名称和描述'
        }), 400
    
    products = load_products()
    product_index = None
    
    for i, p in enumerate(products):
        if p['id'] == product_id:
            product_index = i
            break
    
    if product_index is None:
        return jsonify({
            'success': False,
            'message': '产品不存在'
        }), 404
    
    # 更新产品信息
    products[product_index]['name'] = name
    products[product_index]['description'] = description
    
    # 更新详情字段 - 直接获取值
    products[product_index]['detail'] = request.form.get('detail', '')
    products[product_index]['material'] = request.form.get('material', '')
    products[product_index]['size'] = request.form.get('size', '')
    products[product_index]['weight'] = request.form.get('weight', '')
    products[product_index]['moq'] = request.form.get('moq', '')
    
    # 处理 highlights JSON
    try:
        highlights = request.form.get('highlights', '[]')
        products[product_index]['highlights'] = json.loads(highlights) if highlights else []
    except:
        products[product_index]['highlights'] = []
    
    # 处理 features JSON
    try:
        features = request.form.get('features', '[]')
        products[product_index]['features'] = json.loads(features) if features else []
    except:
        products[product_index]['features'] = []
    
    # 如果上传了新图片
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            # 删除旧图片
            old_image = products[product_index].get('image', '')
            if old_image.startswith('uploads/'):
                old_path = os.path.join('.', old_image)
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            # 保存新图片
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_filename = f'product-{timestamp}-{filename}'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            products[product_index]['image'] = f'uploads/{unique_filename}'
    
    # 处理额外图片上传
    if 'images' in request.files:
        files = request.files.getlist('images')
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
                unique_filename = f'product-detail-{timestamp}-{filename}'
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                if 'images' not in products[product_index]:
                    products[product_index]['images'] = []
                products[product_index]['images'].append(f'uploads/{unique_filename}')
    
    save_products(products)
    
    return jsonify({
        'success': True,
        'message': '产品更新成功',
        'product': products[product_index]
    })


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    """删除产品"""
    products = load_products()
    product_index = None
    
    for i, p in enumerate(products):
        if p['id'] == product_id:
            product_index = i
            break
    
    if product_index is None:
        return jsonify({
            'success': False,
            'message': '产品不存在'
        }), 404
    
    # 删除产品图片
    deleted_product = products[product_index]
    if deleted_product.get('image', '').startswith('uploads/'):
        image_path = os.path.join('.', deleted_product['image'])
        if os.path.exists(image_path):
            os.remove(image_path)
    
    # 删除产品
    products.pop(product_index)
    save_products(products)
    
    return jsonify({
        'success': True,
        'message': '产品删除成功'
    })


# ========== 网站图片管理 API ==========

@app.route('/api/site-images', methods=['GET'])
def get_site_images():
    """获取网站图片配置"""
    images = load_site_images()
    return jsonify({
        'success': True,
        'images': images
    })


@app.route('/api/site-images/logo', methods=['POST'])
@login_required
def upload_logo():
    """上传Logo图片"""
    if 'image' not in request.files:
        return jsonify({
            'success': False,
            'message': '请上传图片文件'
        }), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({
            'success': False,
            'message': '请选择图片文件'
        }), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'message': '只支持 JPG、PNG、GIF、WEBP 格式的图片'
        }), 400
    
    # 保存图片
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f'logo-{timestamp}-{filename}'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    
    # 更新配置
    site_images = load_site_images()
    old_logo = site_images.get('logo', '')
    if old_logo.startswith('uploads/'):
        old_path = os.path.join('.', old_logo)
        if os.path.exists(old_path):
            os.remove(old_path)
    
    site_images['logo'] = f'uploads/{unique_filename}'
    save_site_images(site_images)
    
    return jsonify({
        'success': True,
        'message': 'Logo更新成功',
        'logo': site_images['logo']
    })


@app.route('/api/site-images/about', methods=['POST'])
@login_required
def upload_about_image():
    """上传关于我们图片"""
    if 'image' not in request.files:
        return jsonify({
            'success': False,
            'message': '请上传图片文件'
        }), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({
            'success': False,
            'message': '请选择图片文件'
        }), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'message': '只支持 JPG、PNG、GIF、WEBP 格式的图片'
        }), 400
    
    # 保存图片
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f'about-{timestamp}-{filename}'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    
    # 更新配置
    site_images = load_site_images()
    old_image = site_images.get('about_image', '')
    if old_image.startswith('uploads/'):
        old_path = os.path.join('.', old_image)
        if os.path.exists(old_path):
            os.remove(old_path)
    
    site_images['about_image'] = f'uploads/{unique_filename}'
    save_site_images(site_images)
    
    return jsonify({
        'success': True,
        'message': '关于我们图片更新成功',
        'about_image': site_images['about_image']
    })


@app.route('/api/site-images/banners', methods=['GET'])
def get_banners():
    """获取Banner列表"""
    site_images = load_site_images()
    return jsonify({
        'success': True,
        'banners': site_images.get('banners', [])
    })


@app.route('/api/site-images/banners/<int:banner_id>', methods=['PUT'])
@login_required
def update_banner(banner_id):
    """更新Banner"""
    site_images = load_site_images()
    banners = site_images.get('banners', [])
    
    banner_index = None
    for i, b in enumerate(banners):
        if b['id'] == banner_id:
            banner_index = i
            break
    
    if banner_index is None:
        return jsonify({
            'success': False,
            'message': 'Banner不存在'
        }), 404
    
    # 更新文本信息
    banners[banner_index]['title'] = request.form.get('title', banners[banner_index]['title'])
    banners[banner_index]['subtitle'] = request.form.get('subtitle', banners[banner_index]['subtitle'])
    banners[banner_index]['buttonText'] = request.form.get('buttonText', banners[banner_index]['buttonText'])
    banners[banner_index]['buttonLink'] = request.form.get('buttonLink', banners[banner_index]['buttonLink'])
    
    # 如果上传了新图片
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            # 删除旧图片
            old_image = banners[banner_index].get('image', '')
            if old_image.startswith('uploads/'):
                old_path = os.path.join('.', old_image)
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            # 保存新图片
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_filename = f'banner-{timestamp}-{filename}'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            banners[banner_index]['image'] = f'uploads/{unique_filename}'
    
    site_images['banners'] = banners
    save_site_images(site_images)
    
    return jsonify({
        'success': True,
        'message': 'Banner更新成功',
        'banner': banners[banner_index]
    })


# ========== 网站内容管理 API ==========

@app.route('/api/site-content', methods=['GET'])
def get_site_content():
    """获取网站内容配置"""
    content = load_site_content()
    return jsonify({
        'success': True,
        'content': content
    })


@app.route('/api/site-content', methods=['POST'])
@login_required
def update_site_content():
    """更新网站内容配置"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'message': '无效的数据'
        }), 400
    
    # 加载现有配置
    content = load_site_content()
    
    # 更新配置
    for key, value in data.items():
        content[key] = value
    
    save_site_content(content)
    
    return jsonify({
        'success': True,
        'message': '内容更新成功',
        'content': content
    })


# ========== 留言管理 API ==========

@app.route('/api/messages', methods=['GET'])
@login_required
def get_messages():
    """获取留言列表"""
    messages = load_messages()
    return jsonify({
        'success': True,
        'messages': messages
    })


@app.route('/api/messages', methods=['POST'])
def submit_message():
    """提交留言（前端联系表单）"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'message': '无效的数据'
        }), 400
    
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()
    
    if not name or not phone or not message:
        return jsonify({
            'success': False,
            'message': '请填写必填项'
        }), 400
    
    messages = load_messages()
    
    # 生成新ID
    if messages:
        new_id = max([m['id'] for m in messages]) + 1
    else:
        new_id = 1
    
    new_message = {
        'id': new_id,
        'name': name,
        'phone': phone,
        'email': email,
        'message': message,
        'read': False,
        'createTime': datetime.now().isoformat()
    }
    
    messages.insert(0, new_message)
    
    if not save_messages(messages):
        return jsonify({
            'success': False,
            'message': '保存留言失败，请稍后重试'
        }), 500
    
    return jsonify({
        'success': True,
        'message': '留言提交成功'
    })


@app.route('/api/messages/<int:message_id>/read', methods=['POST'])
@login_required
def mark_message_read(message_id):
    """标记留言为已读"""
    messages = load_messages()
    
    for msg in messages:
        if msg['id'] == message_id:
            msg['read'] = True
            save_messages(messages)
            return jsonify({
                'success': True,
                'message': '已标记为已读'
            })
    
    return jsonify({
        'success': False,
        'message': '留言不存在'
    }), 404


@app.route('/api/messages/<int:message_id>', methods=['DELETE'])
@login_required
def delete_message(message_id):
    """删除留言"""
    messages = load_messages()
    
    for i, msg in enumerate(messages):
        if msg['id'] == message_id:
            messages.pop(i)
            save_messages(messages)
            return jsonify({
                'success': True,
                'message': '留言删除成功'
            })
    
    return jsonify({
        'success': False,
        'message': '留言不存在'
    }), 404


# ========== 页面路由 ==========

@app.route('/admin')
def admin():
    """管理后台页面"""
    return send_from_directory('.', 'admin.html')


@app.route('/admin/login')
def admin_login():
    """管理后台登录页面"""
    return send_from_directory('.', 'admin-login.html')


# ========== 启动服务器 ==========

if __name__ == '__main__':
    print('=' * 50)
    print('  北京梦织家居有限公司官网服务器')
    print('  Beijing Mengzhi Home Co.,Ltd.')
    print('=' * 50)
    print('  服务器启动中...')
    print('=' * 50)
    print(f'  本地访问: http://localhost:3000')
    print(f'  管理后台: http://localhost:3000/admin/login')
    print('=' * 50)
    print(f'  管理员账号: zhangmengke')
    print(f'  管理员密码: ******')
    print('=' * 50)
    print('  按 Ctrl+C 停止服务器')
    print('=' * 50)
    
    # 启动服务器，监听所有网卡
    app.run(host='0.0.0.0', port=3000, debug=True)
