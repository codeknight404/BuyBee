BuyBee: E-Commerce Web Application

🚀 Overview

BuyBee is a feature-rich e-commerce web application built using Python, Flask, and MySQL. It provides a robust, full-stack solution for online retail, supporting secure user authentication (customer and admin), dynamic product catalog browsing, shopping cart management, and order processing. It’s designed to be a solid foundation for any modern e-commerce platform.

🛠️ Installation and Setup

Follow these steps to get BuyBee running locally.

Prerequisites

Python 3.8+

MySQL Server (version 5.7+)

Steps

Environment Setup

a. Virtual Environment: Create and activate a Python virtual environment to manage dependencies:

# Create the environment
python3 -m venv venv

# Activate the environment (Linux/macOS)
source venv/bin/activate
# Activate the environment (Windows)
.\venv\Scripts\activate


b. Install Dependencies: Install all required Python packages (as listed in requirements.txt):

pip install -r requirements.txt 

Also here's a ".env" file with all access variables so please set your host, user and passowrd accordingly!


3. Initialize database Schema and values:

Run the necessary migrations or schema creation queries

create database ecommerce_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    role ENUM('admin', 'customer') DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    image VARCHAR(255), -- Filename for the product image
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE cart_items (
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    -- Composite primary key ensures a user can only have one entry per product
    PRIMARY KEY (user_id, product_id), 
    
    -- Foreign keys ensure data integrity
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

NOTE: for admin account

INSERT INTO users (username, password_hash, email, role) VALUES 
('admin_user', 'pbkdf2:sha256:260000$x36JMtQbLDAxcpgs$46159e0c0ebd4a45b1049f6336964b0e7bb3c99d96012a90fff896067d37cf4c', 'admin@example.com', 'admin');  

 here password='admin'

INSERT INTO products (name, description, price, stock, image) VALUES 
('IPhone 17 (Mist Blue)', 'The IPhone 17 redefines innovation with its stunning 6.3-inch Super Retina XDR display, powered by the lightning-fast A19 Bionic chip. Its dual 48MP Fusion cameras capture breathtaking photos and ultra-steady 4K videos, while the new 18MP front camera brings clarity to every selfie. Crafted with Ceramic Shield 2 and aerospace-grade materials, it\'s built to last and look premium. With up to 30 hours of battery life and five elegant colors, the IPhone 17 is where power meets perfection.', 89999.00, 5, 'Screenshot_2025-10-11_172119.png'),
('Microsoft New Surface Pro (11th Edition)', 'Introducing the Microsoft Surface Pro (11th Edition), the ultimate flexible 2-in-1 Copilot+ PC. Powered by the efficient Qualcomm Snapdragon X Elite/Plus or Intel Core Ultra processors with a powerful NPU, it delivers lightning-fast AI-accelerated performance. Enjoy a stunning 13-inch PixelSense Flow display with an optional, vibrant OLED panel and up to a 120 Hz dynamic refresh rate. Its ultra-portable design and long battery life make it perfect for working anywhere, transforming effortlessly from a tablet to a full-powered laptop experience.', 159990.00, 5, '61FQxxg3HHL._SL1500_.jpg'),
('Dyson V8 Absolute Cord-Free Vacuum Cleaner', 'Dyson V8 Absolute is a versatile and powerful cord-free stick vacuum cleaner engineered for whole-home deep cleaning on various floor types, including carpets and hard floors. It is designed to be lightweight, easy to maneuver, and converts quickly to a handheld vacuum for comprehensive cleaning.', 31999.00, 22, '410Uiqgx4-L._SL1200_.jpg'),
('EDGE Titan Metal Ladies Allure Quartz Analog', 'Titan EDGE Metal Ladies Allure is a beautifully designed, ultra-slim analog quartz watch for women. Its most striking feature is its sleek profile, with the case having an impressive thickness of just 4 mm. The round dial is crafted from a rich Mother-of-Pearl, which is complemented by applied 3D indices and protected by a scratch-resistant Sapphire Crystal glass. The watch is built with a durable stainless steel case and strap, often featuring elegant finishes like Rose Gold or Blue. As part of the renowned Titan Edge collection, it is the perfect accessory for modern women seeking a blend of minimal elegance, precision timekeeping, and sophistication.', 15125.00, 31, '716Nrs4odrL._SL1500_.jpg'),
('AVITO Luxury Perfume | BRISE D\' AVRIL', 'A sophisticated and premium Eau de Parfum for men, BRISE D\' AVRIL from AVITO Luxury Perfume offers a complex, long-lasting scent journey. It belongs to the Woody, Oriental, and Floral fragrance family. Top Notes: Green Rose, Balsamic, Musky. Heart Notes (Mid): Wood, Citrus, Aromatic, Fresh Spicy. Base Notes: Earthy, Amber, Patchouli, Lavender. The overall aroma is a daring and memorable blend, weaving together bold freshness with a deep allure through its aromatic, spicy, balsamic, amber, and patchouli elements. It is designed to enhance confidence and sophistication for the modern man.', 1449.00, 15, '61yYQqFMIbL._SL1500_.jpg'),
('Sony PlayStation5 Gaming Console (Slim)', 'The Sony PlayStation 5 redefines next-gen entertainment with lightning-fast load times, breathtaking graphics, and an ultra-immersive gameplay experience. Powered by the custom AMD Ryzen Zen 2 processor and RDNA 2 GPU, the PS5 delivers up to 4K gaming at 120 FPS with stunning ray-traced visuals and realistic lighting.', 49990.00, 13, '51ljnEaW0pL._SL1000_.jpg'),
('Apple 2025 MacBook Air', 'Apple 2025 MacBook Air redefines portability and performance with a sleek, ultra-thin design built from durable recycled aluminum. Powered by Apple\'s latest M4 chip, it delivers exceptional speed, efficiency, and battery life—making it perfect for students, creators, and professionals on the go. Its Liquid Retina display brings stunning color accuracy and brightness, ideal for creative work and immersive viewing. With silent fanless operation, all-day battery life of up to 18 hours, and macOS optimized for AI-powered productivity, the 2025 MacBook Air combines elegance, power, and sustainability like never before. Whether you\'re editing videos, coding, or multitasking, it ensures a smooth and effortless experience in a beautifully minimalist form.', 110990.00, 6, '711NKCLZfaL._SL1500_.jpg'),
('Nintendo Switch 2', 'The Nintendo Switch 2 is Nintendo\'s next-generation hybrid gaming console, combining powerful new hardware with the signature versatility that lets you play anywhere—handheld, tabletop, or on the TV. Featuring a vibrant 7.9-inch 1080p LCD display with up to 120 Hz refresh rate, the Switch 2 delivers smoother gameplay and richer visuals whether you\'re battling on the go or docked in 4K resolution. Powered by an upgraded custom NVIDIA processor, it offers faster load times, enhanced graphics, and seamless backward compatibility with most Switch titles. The redesigned Joy-Con 2 controllers attach magnetically and feature improved ergonomics and precision, while dual USB-C ports, better speakers, and a sturdier adjustable stand make it more practical than ever. With expanded 256 GB storage, built-in voice and video chat, and support for enhanced "Switch 2 Edition" games, Nintendo\'s 2025 flagship console takes hybrid gaming to an entirely new level—fun, flexible, and future-ready.', 52990.00, 35, '61zYEkSE2rL.jpg'),
('Intel® Core™ i9-14900KF', 'The Intel Core i9-14900KF is a blazing-fast 14th-generation desktop processor built on Intel\'s "Raptor Lake Refresh" architecture. It packs a total of 24 cores—divided into 8 Performance (P) cores and 16 Efficient (E) cores—and supports 32 threads, giving it ample power for gaming, content creation, and heavy multitasking. At its peak, the chip can boost its P-cores up to 6.0 GHz under the right thermal conditions, thanks to Intel\'s Thermal Velocity Boost and Turbo technologies.', 55999.00, 4, '51GS4uZQiSL.jpg'),
('ASUS NVIDIA GeForce RTX 5090 Video Card 32GB GDDR7 PCI Express 5.0 / TUF-RTX5090-32G-GAMING', 'The ASUS TUF Gaming GeForce RTX 5090 32GB GDDR7 is a flagship, high-end graphics card built for extreme 4K gaming, AI workloads, and content creation. It\'s based on NVIDIA\'s Blackwell architecture, boasting 32 GB of ultra-fast GDDR7 memory on a generous 512-bit interface, which yields memory bandwidth in the multi-terabyte per second range.', 496913.00, 1, '81BE1H1w23L._SL1500_.jpg'),
('Samsung 34-inch(86.8cm) Ultra WQHD 2K Odyssey OLED G8 Gaming', 'The Samsung Odyssey OLED G8 (34-inch Ultra WQHD) is a next-generation ultrawide gaming display combining high performance and breathtaking visuals. Its QD-OLED curved panel renders true blacks and vivid colors with a static contrast ratio of ~1,000,000:1, while delivering crisp detail at 3440 × 1440 resolution (Ultra WQHD / 21:9). With a blazing 175 Hz refresh rate and an incredibly low 0.03 ms (GtG) response time, it ensures ultra-smooth motion and minimal blur even in fast-paced gaming scenes. The 1800R curvature wraps subtly around your field of view, enhancing immersion and easing fatigue during long sessions.', 95580.00, 1, '81eLDCu76cL._SL1500_.jpg');

4. Start Web APP in Flask Server:

Open Terminal

and open the "ecommerce_app" folder as a directory in terminal

run the following command:

flask run

Now wait until you see localhost server domain link in your terminal window.

Visit the URL to navigate to the BuyBee ecommerce web app.

5. In case of Admin privileges, login in to admin account, and visit product page and in address bar add "/admin" after "/products" to access the Admin Dashboard Panel and use its feature.


Happy Hacking :D