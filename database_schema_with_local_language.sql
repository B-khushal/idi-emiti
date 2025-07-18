-- Database: cultural_corpus_platform
-- Enhanced schema with local language and dialect support

-- -----------------------------------------------------
-- Table users
-- Stores information about contributors to the platform.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NULL,
    bio TEXT NULL,
    country VARCHAR(100) NULL,
    region VARCHAR(100) NULL,
    city VARCHAR(100) NULL,
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    display_publicly BOOLEAN DEFAULT TRUE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table corpus_categories
-- Defines predefined categories for cultural artifacts.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS corpus_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NULL,
    parent_category_id INT NULL,
    CONSTRAINT fk_parent_category
        FOREIGN KEY (parent_category_id)
        REFERENCES corpus_categories (category_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table cultural_items
-- Core table for storing metadata about each cultural item.
-- Enhanced with local language and dialect fields.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cultural_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description_en TEXT NULL,
    description_te TEXT NULL,
    contributor_id INT NOT NULL,
    category_id INT NOT NULL,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_approved BOOLEAN DEFAULT FALSE,
    reviewer_id INT NULL,
    review_date TIMESTAMP NULL,
    rejection_reason TEXT NULL,
    latitude DECIMAL(10, 8) NULL,
    longitude DECIMAL(11, 8) NULL,
    location_name VARCHAR(500) NULL,
    
    -- Local Language and Dialect Information
    local_language_name VARCHAR(500) NULL, -- Name in local language
    dialect_regional_variation VARCHAR(255) NULL, -- e.g., "Telugu (Hyderabad)", "Bengali (Kolkata)"
    pronunciation_guide VARCHAR(500) NULL, -- Pronunciation in English letters
    cultural_context VARCHAR(500) NULL, -- When and how the object is used
    local_language_audio_path VARCHAR(1000) NULL, -- Path to audio recording of pronunciation
    
    CONSTRAINT fk_contributor
        FOREIGN KEY (contributor_id)
        REFERENCES users (user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
        REFERENCES corpus_categories (category_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_reviewer
        FOREIGN KEY (reviewer_id)
        REFERENCES users (user_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table item_media
-- Stores paths and metadata for media files.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS item_media (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    media_type ENUM('image', 'audio', 'video') NOT NULL,
    file_path VARCHAR(1000) NOT NULL,
    thumbnail_path VARCHAR(1000) NULL,
    description TEXT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_size_kb INT NULL,
    duration_seconds INT NULL,
    dimensions VARCHAR(50) NULL,
    CONSTRAINT fk_item_media
        FOREIGN KEY (item_id)
        REFERENCES cultural_items (item_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table tags
-- Stores unique tags for categorization.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(255) UNIQUE NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table item_tags
-- Junction table for Many-to-Many relationship between cultural_items and tags.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS item_tags (
    item_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (item_id, tag_id),
    CONSTRAINT fk_item_tags_item
        FOREIGN KEY (item_id)
        REFERENCES cultural_items (item_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_item_tags_tag
        FOREIGN KEY (tag_id)
        REFERENCES tags (tag_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table comments
-- Allows users to add comments to cultural items.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text TEXT NOT NULL,
    comment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_moderated BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_comment_item
        FOREIGN KEY (item_id)
        REFERENCES cultural_items (item_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_comment_user
        FOREIGN KEY (user_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table local_languages
-- Stores information about different local languages and dialects.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS local_languages (
    language_id INT AUTO_INCREMENT PRIMARY KEY,
    language_name VARCHAR(255) NOT NULL,
    dialect_name VARCHAR(255) NULL,
    region VARCHAR(255) NULL,
    country VARCHAR(255) NULL,
    script_name VARCHAR(255) NULL, -- e.g., "Devanagari", "Telugu script"
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Indexes for performance optimization
-- -----------------------------------------------------
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_cultural_items_title ON cultural_items (title);
CREATE INDEX idx_cultural_items_contributor_id ON cultural_items (contributor_id);
CREATE INDEX idx_cultural_items_category_id ON cultural_items (category_id);
CREATE INDEX idx_cultural_items_submission_date ON cultural_items (submission_date);
CREATE INDEX idx_cultural_items_is_approved ON cultural_items (is_approved);
CREATE INDEX idx_cultural_items_geocoordinates ON cultural_items (latitude, longitude);
CREATE INDEX idx_cultural_items_local_language ON cultural_items (local_language_name);
CREATE INDEX idx_cultural_items_dialect ON cultural_items (dialect_regional_variation);
CREATE INDEX idx_item_media_item_id ON item_media (item_id);
CREATE INDEX idx_item_media_type ON item_media (media_type);
CREATE INDEX idx_tags_tag_name ON tags (tag_name);
CREATE INDEX idx_comments_item_id ON comments (item_id);
CREATE INDEX idx_comments_user_id ON comments (user_id);
CREATE INDEX idx_local_languages_name ON local_languages (language_name);
CREATE INDEX idx_local_languages_dialect ON local_languages (dialect_name); 