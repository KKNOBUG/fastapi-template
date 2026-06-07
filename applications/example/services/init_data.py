# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : fastapi-template
@Module  : init_data.py
@DateTime: 2025/6/7
"""
from decimal import Decimal

from applications.example.models.example_model import Category, Product
from configure import LOGGER


async def init_example_data():
    """初始化示例数据"""

    # 检查是否已有数据
    category_count = await Category.filter().count()
    if category_count > 0:
        LOGGER.info("示例数据已存在，跳过初始化")
        return

    LOGGER.info("开始初始化示例数据...")

    # ========== 创建分类 ==========
    categories_data = [
        {
            "name": "电子产品",
            "code": "ELECTRONICS",
            "description": "手机、电脑、平板等电子设备",
            "sort_order": 1,
            "state": 0
        },
        {
            "name": "服装鞋帽",
            "code": "CLOTHING",
            "description": "男装、女装、童装、鞋靴",
            "sort_order": 2,
            "state": 0
        },
        {
            "name": "食品饮料",
            "code": "FOOD",
            "description": "零食、饮料、生鲜",
            "sort_order": 3,
            "state": 0
        },
        {
            "name": "家居用品",
            "code": "HOME",
            "description": "家具、装饰、厨具",
            "sort_order": 4,
            "state": 0
        },
        {
            "name": "图书文具",
            "code": "BOOKS",
            "description": "图书、文具、办公用品",
            "sort_order": 5,
            "state": 0
        }
    ]

    created_categories = []
    for cat_data in categories_data:
        try:
            category = await Category.create(**cat_data)
            created_categories.append(category)
            LOGGER.info(f"创建分类: {category.name} (ID: {category.id})")
        except Exception as e:
            LOGGER.error(f"创建分类失败 {cat_data['name']}: {e}")

    if not created_categories:
        LOGGER.error("没有成功创建任何分类，跳过后续数据初始化")
        return

    # ========== 创建商品 ==========
    electronics_id = created_categories[0].id
    clothing_id = created_categories[1].id
    food_id = created_categories[2].id
    home_id = created_categories[3].id
    books_id = created_categories[4].id

    products_data = [
        # 电子产品
        {
            "name": "iPhone 15 Pro",
            "code": "IPHONE15PRO",
            "description": "苹果最新旗舰手机，钛金属设计",
            "price": Decimal("8999.00"),
            "stock": 100,
            "category_id": electronics_id,
            "is_featured": True,
            "tags": ["手机", "苹果", "旗舰"],
            "state": 0
        },
        {
            "name": "MacBook Pro 16",
            "code": "MACBOOKPRO16",
            "description": "专业级笔记本电脑，M3 Pro芯片",
            "price": Decimal("19999.00"),
            "stock": 50,
            "category_id": electronics_id,
            "is_featured": True,
            "tags": ["笔记本", "苹果", "专业"],
            "state": 0
        },
        {
            "name": "AirPods Pro 2",
            "code": "AIRPODSPRO2",
            "description": "主动降噪无线耳机",
            "price": Decimal("1899.00"),
            "stock": 200,
            "category_id": electronics_id,
            "is_featured": False,
            "tags": ["耳机", "无线", "降噪"],
            "state": 0
        },
        {
            "name": "iPad Air 5",
            "code": "IPADAIR5",
            "description": "轻薄便携平板电脑",
            "price": Decimal("4799.00"),
            "stock": 80,
            "category_id": electronics_id,
            "is_featured": False,
            "tags": ["平板", "苹果", "轻薄"],
            "state": 0
        },
        {
            "name": "华为 Mate 60 Pro",
            "code": "MATE60PRO",
            "description": "华为旗舰手机，卫星通信",
            "price": Decimal("6999.00"),
            "stock": 150,
            "category_id": electronics_id,
            "is_featured": True,
            "tags": ["手机", "华为", "卫星通信"],
            "state": 0
        },
        # 服装鞋帽
        {
            "name": "Nike Air Max 90",
            "code": "NIKEAM90",
            "description": "经典气垫运动鞋",
            "price": Decimal("899.00"),
            "stock": 300,
            "category_id": clothing_id,
            "is_featured": True,
            "tags": ["运动鞋", "Nike", "经典"],
            "state": 0
        },
        {
            "name": "优衣库羽绒服",
            "code": "UNIQLOJACKET",
            "description": "轻薄保暖羽绒服",
            "price": Decimal("599.00"),
            "stock": 500,
            "category_id": clothing_id,
            "is_featured": False,
            "tags": ["羽绒服", "保暖", "轻薄"],
            "state": 0
        },
        {
            "name": "Adidas Ultra Boost",
            "code": "ADIDASUB",
            "description": "专业跑步鞋，Boost科技",
            "price": Decimal("1299.00"),
            "stock": 200,
            "category_id": clothing_id,
            "is_featured": True,
            "tags": ["跑步鞋", "Adidas", "Boost"],
            "state": 0
        },
        # 食品饮料
        {
            "name": "三只松鼠坚果礼盒",
            "code": "SQSWGIFT",
            "description": "精选坚果大礼包",
            "price": Decimal("168.00"),
            "stock": 1000,
            "category_id": food_id,
            "is_featured": True,
            "tags": ["坚果", "礼盒", "零食"],
            "state": 0
        },
        {
            "name": "可口可乐 330ml*24",
            "code": "COCACOLA24",
            "description": "经典碳酸饮料整箱",
            "price": Decimal("59.90"),
            "stock": 2000,
            "category_id": food_id,
            "is_featured": False,
            "tags": ["饮料", "可乐", "整箱"],
            "state": 0
        },
        {
            "name": "费列罗巧克力 48粒",
            "code": "FERRERO48",
            "description": "意大利进口巧克力",
            "price": Decimal("158.00"),
            "stock": 800,
            "category_id": food_id,
            "is_featured": True,
            "tags": ["巧克力", "进口", "礼品"],
            "state": 0
        },
        # 家居用品
        {
            "name": "宜家台灯",
            "code": "IKEALAMP",
            "description": "简约设计LED台灯",
            "price": Decimal("129.00"),
            "stock": 400,
            "category_id": home_id,
            "is_featured": False,
            "tags": ["台灯", "LED", "简约"],
            "state": 0
        },
        {
            "name": "小米空气净化器",
            "code": "MIAIRPURIFIER",
            "description": "智能空气净化，除甲醛",
            "price": Decimal("899.00"),
            "stock": 150,
            "category_id": home_id,
            "is_featured": True,
            "tags": ["净化器", "智能", "除甲醛"],
            "state": 0
        },
        {
            "name": "无印良品收纳盒",
            "code": "MUJIBOX",
            "description": "简约收纳盒套装",
            "price": Decimal("79.00"),
            "stock": 600,
            "category_id": home_id,
            "is_featured": False,
            "tags": ["收纳", "简约", "套装"],
            "state": 0
        },
        # 图书文具
        {
            "name": "Python编程从入门到实践",
            "code": "PYTHONBOOK",
            "description": "Python入门经典教材",
            "price": Decimal("89.00"),
            "stock": 300,
            "category_id": books_id,
            "is_featured": True,
            "tags": ["Python", "编程", "入门"],
            "state": 0
        },
        {
            "name": "晨光文具套装",
            "code": "MGBOX",
            "description": "学生文具大礼包",
            "price": Decimal("49.90"),
            "stock": 1000,
            "category_id": books_id,
            "is_featured": False,
            "tags": ["文具", "学生", "套装"],
            "state": 0
        },
        {
            "name": "人类简史",
            "code": "SAPIENS",
            "description": "尤瓦尔·赫拉利著",
            "price": Decimal("68.00"),
            "stock": 500,
            "category_id": books_id,
            "is_featured": True,
            "tags": ["历史", "畅销书", "人文"],
            "state": 0
        }
    ]

    created_products = []
    for prod_data in products_data:
        try:
            product = await Product.create(**prod_data)
            created_products.append(product)
            LOGGER.info(f"创建商品: {product.name} (ID: {product.id})")
        except Exception as e:
            LOGGER.error(f"创建商品失败 {prod_data['name']}: {e}")

    LOGGER.info(f"示例数据初始化完成: {len(created_categories)} 个分类, {len(created_products)} 个商品")


if __name__ == "__main__":
    import asyncio

    asyncio.run(init_example_data())
