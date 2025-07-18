-- Database: cultural_corpus_platform
-- Designed for a robust, scalable, and multimodal cultural data collection.

-- -----------------------------------------------------
-- Table users
-- Stores information about contributors to the platform.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- Store hashed passwords, never plain text
    full_name VARCHAR(255) NULL,
    bio TEXT NULL,
    country VARCHAR(100) NULL,
    region VARCHAR(100) NULL, -- e.g., state, province
    city VARCHAR(100) NULL,
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_admin BOOLEAN DEFAULT FALSE, -- True for administrators/curators
    is_active BOOLEAN DEFAULT TRUE, -- Account status
    -- Privacy considerations: User can opt-out of public display of their details
    display_publicly BOOLEAN DEFAULT TRUE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table corpus_categories
-- Defines predefined categories for cultural artifacts to ensure standardization.
-- Supports hierarchical categories.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS corpus_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NULL,
    parent_category_id INT NULL, -- For hierarchical categories (e.g., 'Textile' -> 'Embroidery')
    CONSTRAINT fk_parent_category
        FOREIGN KEY (parent_category_id)
        REFERENCES corpus_categories (category_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Insert some initial categories (examples for demonstration)
INSERT INTO corpus_categories (category_name, description, parent_category_id) VALUES
('Household Object', 'Everyday items found in traditional homes.', NULL),
('Agricultural Tool', 'Tools used in farming practices.', NULL),
('Festival Artifact', 'Items specifically used in cultural festivals and celebrations.', NULL),
('Textile', 'Fabric-based items, including clothing, weaves, and embroidery.', NULL),
('Art Form', 'Various forms of visual and performing arts.', NULL),
('Music', 'Musical instruments, traditional songs, and compositions.', NULL),
('Oral Tradition', 'Folktales, proverbs, historical narratives passed down verbally.', NULL),
('Embroidery', 'Textile decorated with needlework.', (SELECT category_id FROM corpus_categories WHERE category_name = 'Textile')),
('Sculpture', 'Three-dimensional art forms.', (SELECT category_id FROM corpus_categories WHERE category_name = 'Art Form'));

-- -----------------------------------------------------
-- Table cultural_items
-- Core table for storing metadata about each cultural item.
-- Includes fields for title, descriptions, geocoordinates, and links to contributor/category.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cultural_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description_en TEXT NULL, -- English description of the item
    description_te TEXT NULL, -- Telugu description (example for a regional language)
    -- Add more description_xx columns for other specific regional languages as needed,
    -- or consider the localization_strings table for more dynamic multilingual support.
    contributor_id INT NOT NULL, -- Foreign Key to the users table
    category_id INT NOT NULL, -- Foreign Key to the corpus_categories table
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_approved BOOLEAN DEFAULT FALSE, -- Status for moderation/curation workflow
    reviewer_id INT NULL, -- Foreign Key to users table (if an admin reviewed it)
    review_date TIMESTAMP NULL,
    rejection_reason TEXT NULL, -- If the item was rejected during review
    latitude DECIMAL(10, 8) NULL, -- Geocoordinates: Latitude (e.g., 17.38500000)
    longitude DECIMAL(11, 8) NULL, -- Geocoordinates: Longitude (e.g., 78.48670000)
    location_name VARCHAR(500) NULL, -- Human-readable location string (e.g., "Hyderabad, Telangana, India")
    CONSTRAINT fk_contributor
        FOREIGN KEY (contributor_id)
        REFERENCES users (user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE, -- Prevent deleting a user if they have submitted cultural items
    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
        REFERENCES corpus_categories (category_id)
        ON DELETE RESTRICT ON UPDATE CASCADE, -- Prevent deleting a category if cultural items are linked to it
    CONSTRAINT fk_reviewer
        FOREIGN KEY (reviewer_id)
        REFERENCES users (user_id)
        ON DELETE SET NULL ON UPDATE CASCADE -- If a reviewer user is deleted, set their review_id to NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table item_media
-- Stores paths and specific metadata for images, audio, and video files
-- associated with a cultural item. A single cultural item can have multiple media files.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS item_media (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL, -- Foreign Key to cultural_items table
    media_type ENUM('image', 'audio', 'video') NOT NULL, -- Type of media file
    file_path VARCHAR(1000) NOT NULL, -- URL or path to the stored file (e.g., S3 URL, local server path)
    thumbnail_path VARCHAR(1000) NULL, -- URL or path to a thumbnail/preview image/video frame
    description TEXT NULL, -- Specific description for this particular media file (optional)
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_size_kb INT NULL, -- Size of the file in kilobytes
    duration_seconds INT NULL, -- Duration for audio/video files in seconds
    dimensions VARCHAR(50) NULL, -- Dimensions for images/video (e.g., "1920x1080" or "1080x720")
    CONSTRAINT fk_item_media
        FOREIGN KEY (item_id)
        REFERENCES cultural_items (item_id)
        ON DELETE CASCADE ON UPDATE CASCADE -- If a cultural item is deleted, all its associated media records are automatically deleted
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table tags
-- Stores unique tags that can be applied to cultural items for flexible categorization
-- and improved searchability.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(255) UNIQUE NOT NULL -- Unique name for each tag (e.g., "ancient", "folk art", "Hyderabad")
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table item_tags
-- Junction table for a Many-to-Many relationship between cultural_items and tags.
-- Allows a cultural item to have multiple tags and a tag to be applied to multiple items.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS item_tags (
    item_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (item_id, tag_id), -- Composite primary key to ensure uniqueness
    CONSTRAINT fk_item_tags_item
        FOREIGN KEY (item_id)
        REFERENCES cultural_items (item_id)
        ON DELETE CASCADE ON UPDATE CASCADE, -- If an item is deleted, remove its tag associations
    CONSTRAINT fk_item_tags_tag
        FOREIGN KEY (tag_id)
        REFERENCES tags (tag_id)
        ON DELETE CASCADE ON UPDATE CASCADE -- If a tag is deleted, remove its item associations
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table comments
-- Allows users (contributors or admins) to add comments or notes to cultural items.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL, -- Foreign Key to cultural_items table
    user_id INT NOT NULL, -- Foreign Key to users table (the user who made the comment)
    comment_text TEXT NOT NULL,
    comment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_moderated BOOLEAN DEFAULT FALSE, -- For moderation of comments
    CONSTRAINT fk_comment_item
        FOREIGN KEY (item_id)
        REFERENCES cultural_items (item_id)
        ON DELETE CASCADE ON UPDATE CASCADE, -- If the item is deleted, its comments are deleted
    CONSTRAINT fk_comment_user
        FOREIGN KEY (user_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE ON UPDATE CASCADE -- If the user is deleted, their comments are deleted
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table localization_strings (Optional, for advanced multilingual support)
-- This table is useful if you need to support a large number of languages dynamically
-- for various text fields (titles, descriptions, category names, etc.).
-- Instead of adding description_xx columns directly to cultural_items,
-- you would store a string_key in cultural_items and look up the translated text here.
-- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS localization_strings (
--     string_key VARCHAR(255) PRIMARY KEY, -- A unique identifier for a translatable string (e.g., 'item_title_123', 'category_name_5')
--     language_code VARCHAR(10) NOT NULL, -- e.g., 'en', 'te', 'hi', 'fr'
--     translated_text TEXT NOT NULL,
--     UNIQUE (string_key, language_code) -- Ensures only one translation per key per language
-- ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- If using localization_strings, cultural_items might look like:
-- title_key VARCHAR(255) NOT NULL,
-- description_key VARCHAR(255) NULL,
-- And corpus_categories might have category_name_key VARCHAR(255) NOT NULL,

-- -----------------------------------------------------
-- Indexes (for performance optimization)
-- These indexes will speed up common queries and foreign key lookups.
-- -----------------------------------------------------
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_cultural_items_title ON cultural_items (title);
CREATE INDEX idx_cultural_items_contributor_id ON cultural_items (contributor_id);
CREATE INDEX idx_cultural_items_category_id ON cultural_items (category_id);
CREATE INDEX idx_cultural_items_submission_date ON cultural_items (submission_date);
CREATE INDEX idx_cultural_items_is_approved ON cultural_items (is_approved); -- For moderation queues
CREATE INDEX idx_cultural_items_geocoordinates ON cultural_items (latitude, longitude); -- For spatial queries
CREATE INDEX idx_item_media_item_id ON item_media (item_id);
CREATE INDEX idx_item_media_type ON item_media (media_type);
CREATE INDEX idx_tags_tag_name ON tags (tag_name);
CREATE INDEX idx_comments_item_id ON comments (item_id);
CREATE INDEX idx_comments_user_id ON comments (user_id); 